#!/usr/bin/env python3
"""
Deterministic GitHub PR review payload builder for the code-review skill.

Parses unified PR diffs and paginated prior GitHub reviews/comments to:
- Enforce duplicate (head_sha, verdict) skipping (exit 2)
- Enforce the 3-rework-cycle cap before human escalation (exit 1)
- Compute monotonic per-PR CR-XX finding IDs outside LLM context
- Anchor valid (path, line, side) findings as inline comments and move
  out-of-hunk, missing-file, or cross-file findings into the review body
- Render optional collapsible RV-* runtime checks and triage closure summaries
- Stamp cr-review-meta and emit GitHub POST /pulls/{n}/reviews JSON to stdout
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

VALID_VERDICTS = ("ready", "needs_rework")
VALID_SIDES = ("LEFT", "RIGHT")
MAX_REWORK_CYCLES = 3

META_RE = re.compile(
    r"<!--\s*cr-review-meta:\s*max_id=(\d+)\s+head_sha=(\S+)\s+verdict=(ready|needs_rework)\s*-->"
)
CR_HEADING_RE = re.compile(r"^###\s+CR-(\d+)\b", re.MULTILINE)
HUNK_RE = re.compile(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@")


def fail(message: str, code: int = 1) -> None:
    """Write error message to stderr and exit with the given code."""
    print(f"build_review: {message}", file=sys.stderr)
    sys.exit(code)


def load_json_file(path_str: str, label: str) -> Any:
    """Load and parse a UTF-8 JSON file, exiting 1 on I/O or decode failure."""
    path = Path(path_str)
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as exc:
        fail(f"cannot read {label} file '{path_str}': {exc}")
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON in {label} file '{path_str}': {exc}")


def flatten_paginated(data: Any, label: str) -> list[dict[str, Any]]:
    """Flatten gh api --paginate --slurp ([[...]]) or flat ([...]) JSON lists."""
    if not isinstance(data, list):
        fail(f"{label} must be a JSON array")
    items: list[dict[str, Any]] = []
    for entry in data:
        if isinstance(entry, list):
            for sub in entry:
                if not isinstance(sub, dict):
                    fail(f"{label} nested page contains non-object entry")
                items.append(sub)
        elif isinstance(entry, dict):
            items.append(entry)
        else:
            fail(f"{label} contains non-object entry")
    return items


def _strip_diff_prefix(path_token: str, prefix: str) -> str:
    """Strip git diff a/ or b/ prefix and optional surrounding quotes."""
    token = path_token.strip()
    if token.startswith('"') and token.endswith('"') and len(token) >= 2:
        token = token[1:-1]
    if token.startswith(prefix):
        return token[len(prefix):]
    return token


def parse_diff_hunks(diff_text: str) -> tuple[dict[str, set[int]], dict[str, set[int]]]:
    """
    Parse unified diff text into valid inline anchor line sets per file.

    Returns (left_lines, right_lines) where:
    - left_lines[path] holds deleted line numbers valid for side="LEFT"
    - right_lines[path] holds added/modified/context line numbers valid for side="RIGHT"
    """
    left_lines: dict[str, set[int]] = {}
    right_lines: dict[str, set[int]] = {}

    old_path: str | None = None
    current_path: str | None = None
    in_hunk = False
    old_line = 0
    new_line = 0
    old_remaining = 0
    new_remaining = 0

    for raw_line in diff_text.splitlines():
        if in_hunk and (old_remaining > 0 or new_remaining > 0):
            if raw_line.startswith("\\"):
                continue
            if raw_line.startswith("-"):
                if current_path is not None:
                    left_lines.setdefault(current_path, set()).add(old_line)
                old_line += 1
                old_remaining = max(0, old_remaining - 1)
                continue
            if raw_line.startswith("+"):
                if current_path is not None:
                    right_lines.setdefault(current_path, set()).add(new_line)
                new_line += 1
                new_remaining = max(0, new_remaining - 1)
                continue
            if raw_line.startswith(" ") or raw_line == "":
                if current_path is not None:
                    right_lines.setdefault(current_path, set()).add(new_line)
                old_line += 1
                new_line += 1
                old_remaining = max(0, old_remaining - 1)
                new_remaining = max(0, new_remaining - 1)
                continue
            # Unexpected non-hunk line ends the current hunk.
            in_hunk = False

        if raw_line.startswith("diff --git "):
            in_hunk = False
            old_path = None
            current_path = None
            continue

        if raw_line.startswith("--- "):
            in_hunk = False
            token = raw_line[4:].split("\t", 1)[0].strip()
            old_path = None if token == "/dev/null" else _strip_diff_prefix(token, "a/")
            continue

        if raw_line.startswith("+++ "):
            in_hunk = False
            token = raw_line[4:].split("\t", 1)[0].strip()
            if token == "/dev/null":
                current_path = old_path
            else:
                current_path = _strip_diff_prefix(token, "b/")
            continue

        match = HUNK_RE.match(raw_line)
        if match:
            old_line = int(match.group(1))
            old_remaining = int(match.group(2)) if match.group(2) is not None else 1
            new_line = int(match.group(3))
            new_remaining = int(match.group(4)) if match.group(4) is not None else 1
            in_hunk = True

    return left_lines, right_lines


def inspect_history(
    reviews: list[dict[str, Any]],
    comments: list[dict[str, Any]],
) -> tuple[int, set[tuple[str, str]], int]:
    """
    Scan prior reviews and inline comments for monotonic max_id,
    prior (head_sha, verdict) pairs, and needs_rework cycle count.
    """
    max_id = 0
    seen_sha_verdicts: set[tuple[str, str]] = set()
    needs_rework_count = 0

    for review in reviews:
        body = review.get("body") or ""
        if not isinstance(body, str):
            continue
        for m in META_RE.finditer(body):
            meta_max = int(m.group(1))
            meta_sha = m.group(2)
            meta_verdict = m.group(3)
            if meta_max > max_id:
                max_id = meta_max
            seen_sha_verdicts.add((meta_sha, meta_verdict))
            if meta_verdict == "needs_rework":
                needs_rework_count += 1
        for m in CR_HEADING_RE.finditer(body):
            cid = int(m.group(1))
            if cid > max_id:
                max_id = cid

    for comment in comments:
        body = comment.get("body") or ""
        if not isinstance(body, str):
            continue
        for m in META_RE.finditer(body):
            meta_max = int(m.group(1))
            if meta_max > max_id:
                max_id = meta_max
        for m in CR_HEADING_RE.finditer(body):
            cid = int(m.group(1))
            if cid > max_id:
                max_id = cid

    return max_id, seen_sha_verdicts, needs_rework_count


def validate_input(data: Any) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], dict[str, str]]:
    """Validate input JSON schema and return (findings, rv_checks, triage_closures, meta_fields)."""
    if not isinstance(data, dict):
        fail("input JSON root must be an object")
    if "findings" not in data or not isinstance(data["findings"], list):
        fail("input JSON must include a 'findings' array")

    findings: list[dict[str, Any]] = []
    for idx, item in enumerate(data["findings"]):
        if not isinstance(item, dict):
            fail(f"findings[{idx}] must be an object")
        for req in ("severity", "title", "body"):
            val = item.get(req)
            if not isinstance(val, str) or not val.strip():
                fail(f"findings[{idx}] missing required non-empty string field '{req}'")
        path_val = item.get("path")
        if path_val is not None and not isinstance(path_val, str):
            fail(f"findings[{idx}].path must be a string or null")
        line_val = item.get("line")
        if line_val is not None:
            if isinstance(line_val, bool) or not isinstance(line_val, int) or line_val <= 0:
                fail(f"findings[{idx}].line must be a positive integer or null")
        side_val = item.get("side")
        if side_val is not None and side_val not in VALID_SIDES:
            fail(f"findings[{idx}].side must be 'LEFT', 'RIGHT', or null")
        findings.append(item)

    rv_checks = data.get("rv_checks", [])
    if not isinstance(rv_checks, list):
        fail("input JSON 'rv_checks' must be an array when provided")
    for idx, chk in enumerate(rv_checks):
        if not isinstance(chk, dict):
            fail(f"rv_checks[{idx}] must be an object")

    triage_closures = data.get("triage_closures", [])
    if not isinstance(triage_closures, list):
        fail("input JSON 'triage_closures' must be an array when provided")
    for idx, cls_item in enumerate(triage_closures):
        if not isinstance(cls_item, dict):
            fail(f"triage_closures[{idx}] must be an object")

    meta_fields: dict[str, str] = {}
    for key in ("summary", "base_ref", "head_ref", "covered_state", "tier"):
        val = data.get(key)
        if isinstance(val, str) and val.strip():
            meta_fields[key] = val.strip()

    return findings, rv_checks, triage_closures, meta_fields


def format_cr_id(num: int) -> str:
    """Format numeric finding ID as CR-01..CR-99, CR-100, etc."""
    return f"CR-{num:02d}"


def format_finding_block(cr_id: str, finding: dict[str, Any], include_location: bool) -> str:
    """Render a finding with a canonical ### CR-NN heading."""
    title = finding["title"].strip()
    severity = finding["severity"].strip()
    axis = finding.get("axis")
    meta_parts = [f"**Severity:** {severity}"]
    if isinstance(axis, str) and axis.strip():
        meta_parts.append(f"**Axis:** {axis.strip()}")
    if include_location:
        path_val = finding.get("path")
        line_val = finding.get("line")
        side_val = finding.get("side")
        if isinstance(path_val, str) and path_val.strip():
            loc = f"`{path_val.strip()}`"
            if line_val is not None:
                loc += f":L{line_val}"
            if side_val:
                loc += f" ({side_val})"
            meta_parts.append(f"**Location:** {loc}")
        else:
            meta_parts.append("**Location:** Cross-file / General")

    lines = [
        f"### {cr_id}: {title}",
        "",
        " | ".join(meta_parts),
        "",
        finding["body"].strip(),
    ]
    return "\n".join(lines)


def format_triage_summary(closures: list[dict[str, Any]]) -> str:
    """Render Exit B / Exit C triage closure summary."""
    lines = ["### Triage Summary", ""]
    for item in closures:
        cid = str(item.get("id", "CR-??")).strip()
        exit_code = str(item.get("exit", "")).strip()
        resolution = str(item.get("resolution", "")).strip()
        exit_label = f"Exit {exit_code}" if exit_code and not exit_code.lower().startswith("exit") else exit_code
        if exit_label:
            lines.append(f"- **{cid}** ({exit_label}): {resolution}")
        else:
            lines.append(f"- **{cid}**: {resolution}")
    return "\n".join(lines)


def format_rv_checks(rv_checks: list[dict[str, Any]]) -> str:
    """Render collapsible RV-* executable runtime checks block."""
    lines = [
        "<details>",
        "<summary>Executable Runtime Checks (RV-*)</summary>",
        "",
    ]
    for idx, chk in enumerate(rv_checks, start=1):
        chk_id = str(chk.get("id") or f"RV-{idx:02d}").strip()
        purpose = str(chk.get("purpose") or "Runtime verification check").strip()
        scope = str(chk.get("scope") or "local").strip()
        pass_cond = str(chk.get("pass_condition") or "").strip()
        fail_sig = str(chk.get("fail_signal") or "").strip()
        command = str(chk.get("command") or "").strip()

        lines.append(f"#### {chk_id}: {purpose}")
        lines.append(f"- **Scope:** `{scope}`")
        if pass_cond:
            lines.append(f"- **Pass Condition:** {pass_cond}")
        if fail_sig:
            lines.append(f"- **Failure Signal:** {fail_sig}")
        if command:
            lines.append("```sh")
            lines.append(command)
            lines.append("```")
        lines.append("")

    lines.append("</details>")
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    """Build CLI argument parser."""
    parser = argparse.ArgumentParser(
        description="Build a validated GitHub PR review JSON payload with monotonic CR-XX IDs."
    )
    parser.add_argument("--input", required=True, help="Path to findings JSON input file")
    parser.add_argument("--diff", required=True, help="Path to unified PR diff file")
    parser.add_argument("--reviews", required=True, help="Path to prior PR reviews JSON file")
    parser.add_argument("--comments", required=True, help="Path to prior PR inline comments JSON file")
    parser.add_argument("--head-sha", required=True, help="Reviewed PR head commit SHA")
    parser.add_argument("--verdict", required=True, help="Review verdict: ready or needs_rework")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    head_sha = args.head_sha.strip()
    if not head_sha:
        fail("--head-sha must be a non-empty string")
    if args.verdict not in VALID_VERDICTS:
        fail(f"invalid --verdict '{args.verdict}'; expected one of: {', '.join(VALID_VERDICTS)}")

    input_data = load_json_file(args.input, "input")
    reviews_raw = load_json_file(args.reviews, "reviews")
    comments_raw = load_json_file(args.comments, "comments")

    try:
        diff_text = Path(args.diff).read_text(encoding="utf-8")
    except OSError as exc:
        fail(f"cannot read diff file '{args.diff}': {exc}")

    findings, rv_checks, triage_closures, meta_fields = validate_input(input_data)
    reviews = flatten_paginated(reviews_raw, "reviews")
    comments = flatten_paginated(comments_raw, "comments")

    max_id, seen_sha_verdicts, needs_rework_count = inspect_history(reviews, comments)

    if (head_sha, args.verdict) in seen_sha_verdicts:
        fail(
            f"duplicate review skipped: (head_sha={head_sha}, verdict={args.verdict}) already exists",
            code=2,
        )

    if args.verdict == "needs_rework" and needs_rework_count >= MAX_REWORK_CYCLES:
        fail(
            f"3-rework-cycle cap reached ({needs_rework_count} prior needs_rework reviews); escalate to human owner",
            code=1,
        )

    left_lines, right_lines = parse_diff_hunks(diff_text)

    inline_comments: list[dict[str, Any]] = []
    unanchored_blocks: list[str] = []

    current_id = max_id
    for finding in findings:
        current_id += 1
        cr_id = format_cr_id(current_id)

        path_val = finding.get("path")
        line_val = finding.get("line")
        side_val = finding.get("side") or "RIGHT"

        anchored = False
        if isinstance(path_val, str) and path_val.strip() and isinstance(line_val, int):
            norm_path = path_val.strip()
            if side_val == "LEFT" and line_val in left_lines.get(norm_path, set()):
                anchored = True
            elif side_val == "RIGHT" and line_val in right_lines.get(norm_path, set()):
                anchored = True

        if anchored:
            inline_comments.append(
                {
                    "path": path_val.strip(),
                    "line": line_val,
                    "side": side_val,
                    "body": format_finding_block(cr_id, finding, include_location=False),
                }
            )
        else:
            unanchored_blocks.append(format_finding_block(cr_id, finding, include_location=True))

    short_sha = head_sha[:7]
    body_sections: list[str] = []

    header_line = f"**Code review @ `{short_sha}`**: `{args.verdict}`"
    if "base_ref" in meta_fields and "head_ref" in meta_fields:
        header_line = (
            f"**Code review @ `{short_sha}`** "
            f"(`{meta_fields['base_ref']}`..`{meta_fields['head_ref']}`): `{args.verdict}`"
        )
    body_sections.append(header_line)

    meta_notes: list[str] = []
    if "covered_state" in meta_fields:
        meta_notes.append(f"Covered state: `{meta_fields['covered_state']}`.")
    if "tier" in meta_fields:
        meta_notes.append(f"Tier: `{meta_fields['tier']}`.")
    meta_notes.append("Static provenance only; merge authority stays with the owner.")
    body_sections.append(" ".join(meta_notes))

    if "summary" in meta_fields:
        body_sections.append(meta_fields["summary"])
    elif not findings:
        body_sections.append("No new findings.")

    if unanchored_blocks:
        body_sections.append("### Findings (Unanchored / Cross-File)\n\n" + "\n\n".join(unanchored_blocks))

    if triage_closures:
        body_sections.append(format_triage_summary(triage_closures))

    if rv_checks:
        body_sections.append(format_rv_checks(rv_checks))

    body_sections.append(
        f"<!-- cr-review-meta: max_id={current_id:02d} head_sha={head_sha} verdict={args.verdict} -->"
    )

    payload = {
        "commit_id": head_sha,
        "event": "COMMENT",
        "body": "\n\n".join(body_sections),
        "comments": inline_comments,
    }
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
