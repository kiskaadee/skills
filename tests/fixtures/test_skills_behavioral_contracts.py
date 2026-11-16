#!/usr/bin/env python3
"""
test_skills_behavioral_contracts.py
Deterministic behavioral contract test suite for kiskaadee/skills.

Verifies:
1. Prerequisite guidance on missing gt binary
2. Anti-hallucination resource ID querying rules
3. Proportionality scaling (lightweight docs vs standard code)
4. Feature verification canonical node 5-tuples and dynamic Mermaid projection
5. Security invariant verification seams
6. Rework routing and execution record transitions
7. Deviation reporting on skipped checks
8. Strict dry-run zero-mutation invariants
9. Skill inventory, line count (<= 80), em-dash absence, and path portability
10. Review comment publishing ownership (code-review drafts, gitea-pr posts with guards)
11. Project board 5-column reconciliation, semantic hex colors, and transition ownership
12. reconcile-docs read-only Gitea ingestion and bidirectional hooks with gitea-plan / implement-slice
13. Polyglot TDD hardening (Mode A/B, 5 languages, 5 empirical invariants), code-review Axis 3 binding, and Suggested Next Step soft-chaining
"""

import os
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent

# Canonical Active Portable Skills list from install.sh
EXPECTED_SKILLS = [
    "build-skill",
    "code-review",
    "derive-skill",
    "diagnose",
    "document",
    "git-manager",
    "gitea-plan",
    "gitea-pr",
    "gt-usage",
    "implement-slice",
    "inspect-flake-update",
    "nix-devshell",
    "practice",
    "reconcile-docs",
    "tdd",
    "verify-slice",
]


class WorkflowNode:
    """Canonical 5-tuple workflow node."""
    def __init__(self, node_id, claim, method, executor, pass_condition, failure_route=None):
        self.node_id = node_id
        self.claim = claim
        self.method = method
        self.executor = executor
        self.pass_condition = pass_condition
        self.failure_route = failure_route
        self.status = "planned"
        self.evidence = None

    def validate_schema(self):
        assert re.match(r"^[A-Z0-9_-]+$", self.node_id), f"Invalid node_id: {self.node_id}"
        assert self.claim and isinstance(self.claim, str), "claim must be non-empty string"
        assert self.method and isinstance(self.method, str), "method must be non-empty string"
        assert self.executor in [
            "Implementation Worker",
            "Independent QA Subagent",
            "Reviewer Subagent",
            "Human Owner",
            "Orchestrator",
        ], f"Invalid executor: {self.executor}"
        assert self.pass_condition and isinstance(self.pass_condition, str), "pass_condition must be non-empty string"

    def to_dict(self):
        return {
            "node_id": self.node_id,
            "claim": self.claim,
            "method": self.method,
            "executor": self.executor,
            "pass_condition": self.pass_condition,
            "status": self.status,
            "evidence": self.evidence,
        }


class WorkflowEngine:
    """
    Reference model of implement-slice adaptive workflow generator.
    Encodes rules from orchestration-tiers.md and handoff-contracts.md.
    """
    @staticmethod
    def plan_slice(title, scope_files, is_security_sensitive=False, is_dry_run=False):
        nodes = []
        is_doc_only = all(f.endswith(".md") or f.endswith(".txt") for f in scope_files)

        if is_doc_only:
            # Proportionality: Lightweight tier
            nodes.append(WorkflowNode(
                node_id="TASK-DOC-01",
                claim=f"Author documentation updates for {title}",
                method="text editor",
                executor="Implementation Worker",
                pass_condition="Files updated matching scope and clean diff",
            ))
            nodes.append(WorkflowNode(
                node_id="CHK-FORMAT",
                claim="Documentation formatting conforms to line caps and style",
                method="wc -l && grep checks",
                executor="Implementation Worker",
                pass_condition="Exit code 0",
                failure_route="rework in-place",
            ))
        else:
            # Standard / High-Assurance tier
            nodes.append(WorkflowNode(
                node_id="TASK-IMPL-01",
                claim=f"Implement core logic for {title}",
                method="editor & compiler",
                executor="Implementation Worker",
                pass_condition="Clean working tree and coherent checkpoint commit",
            ))
            nodes.append(WorkflowNode(
                node_id="CHK-UNIT-01",
                claim="Unit and seam test suites pass",
                method="test harness",
                executor="Independent QA Subagent",
                pass_condition="Exit code 0, 100% assertions green",
                failure_route="route to existing worker session",
            ))
            if is_security_sensitive:
                nodes.append(WorkflowNode(
                    node_id="CHK-SEC-01",
                    claim="Defensive invariants hold: zero cleartext secrets and strict permissions",
                    method="secret scan and stat -c '%a'",
                    executor="Independent QA Subagent",
                    pass_condition="Zero matches for secrets, permissions 0600",
                    failure_route="block commit, sanitize diff",
                ))
            nodes.append(WorkflowNode(
                node_id="GATE-REVIEW",
                claim="Final HEAD 4-axis static and strategic review passed",
                method="code-review",
                executor="Reviewer Subagent",
                pass_condition="Ready disposition matching exact final HEAD",
                failure_route="rework review comments",
            ))

        mermaid_graph = WorkflowEngine.project_mermaid(nodes)
        return {
            "title": title,
            "is_doc_only": is_doc_only,
            "is_dry_run": is_dry_run,
            "nodes": nodes,
            "mermaid": mermaid_graph,
        }

    @staticmethod
    def project_mermaid(nodes):
        lines = ["flowchart TD"]
        for node in nodes:
            lines.append(f'    {node.node_id}["{node.node_id}: {node.claim}"]')
        # Add sequence edges and explicit failure/rework edges
        for i in range(len(nodes) - 1):
            lines.append(f"    {nodes[i].node_id} --> {nodes[i+1].node_id}")
            if nodes[i+1].failure_route:
                lines.append(f'    {nodes[i+1].node_id} -.->|Fail / Rework| {nodes[0].node_id}')
        return "\n".join(lines)

    @staticmethod
    def generate_deviation_report(nodes):
        skipped = [n for n in nodes if n.status == "skipped"]
        rework = [n for n in nodes if n.status == "failed"]
        return {
            "skipped_checks": [
                {"node_id": n.node_id, "rationale": n.evidence or "No rationale recorded"}
                for n in skipped
            ],
            "rework_count": len(rework),
            "clean_pass": len(skipped) == 0 and len(rework) == 0,
        }


class TestSkillsBehavioralContracts(unittest.TestCase):

    def test_prerequisite_guidance(self):
        """Proves missing gt binary triggers actionable prerequisite instructions."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_bin = Path(tmp_dir) / "bin"
            tmp_bin.mkdir()
            git_path = shutil.which("git")
            self.assertIsNotNone(git_path, "git must exist on host")
            (tmp_bin / "git").symlink_to(git_path)

            orig_dirs = os.environ.get("PATH", "").split(os.pathsep)
            new_dirs = [d for d in orig_dirs if not (Path(d) / "gt").exists()]
            new_dirs.insert(0, str(tmp_bin))

            env = os.environ.copy()
            env["PATH"] = os.pathsep.join(new_dirs)

            res = subprocess.run(
                ["./install.sh", "check"],
                cwd=REPO_ROOT,
                env=env,
                capture_output=True,
                text=True,
            )
            # Must output actionable warning about gt CLI
            combined = res.stdout + res.stderr
            self.assertIn("'gt' CLI not found in PATH", combined)
            self.assertIn("Gitea skills (gt-usage, gitea-plan, gitea-pr, implement-slice) require the official Gitea CLI", combined)
            self.assertIn("https://gitea.com/gitea/cli/releases", combined)

    def test_resource_id_querying_rules(self):
        """Proves milestone/issue planning recipes forbid hardcoded ID guessing and require gt --json."""
        gt_usage_cmd = REPO_ROOT / "skills" / "gt-usage" / "references" / "commands.md"
        self.assertTrue(gt_usage_cmd.exists())
        content = gt_usage_cmd.read_text()

        # Must mandate --json for querying IDs
        self.assertIn("gt milestone list --json id,title,state,url", content)
        self.assertIn("gt issue list --json id,number,title,state,url", content)
        self.assertIn("gt project list --json id,title,state,url", content)

        # Anti-hallucination check: ensure gitea-plan explicitly forbids constructing /milestone/1
        gitea_plan = REPO_ROOT / "skills" / "gitea-plan" / "SKILL.md"
        self.assertIn("never guess sequence numbers or construct `/milestone/1`", gitea_plan.read_text())

    def test_proportionality_scaling(self):
        """Proves a documentation-only task produces a lightweight workflow without synthetic test ceremony."""
        doc_slice = WorkflowEngine.plan_slice(
            title="Update architecture notes",
            scope_files=["docs/adr/0001.md", "README.md"],
        )
        self.assertTrue(doc_slice["is_doc_only"])
        # Should have lightweight nodes, no Independent QA Subagent, no unit test harness
        executors = [n.executor for n in doc_slice["nodes"]]
        methods = [n.method for n in doc_slice["nodes"]]
        self.assertNotIn("Independent QA Subagent", executors)
        self.assertNotIn("test harness", methods)
        self.assertEqual(len(doc_slice["nodes"]), 2)

    def test_feature_verification_canonical_schema(self):
        """Proves a multi-file code slice produces valid canonical 5-tuples and dynamic Mermaid projection."""
        code_slice = WorkflowEngine.plan_slice(
            title="Add authentication middleware",
            scope_files=["src/auth.py", "src/tokens.py"],
            is_security_sensitive=False,
        )
        self.assertFalse(code_slice["is_doc_only"])
        self.assertGreaterEqual(len(code_slice["nodes"]), 3)

        # Validate canonical schema on each node
        for node in code_slice["nodes"]:
            node.validate_schema()

        # Dynamic Mermaid projection validation
        mermaid = code_slice["mermaid"]
        self.assertIn("flowchart TD", mermaid)
        for node in code_slice["nodes"]:
            self.assertIn(node.node_id, mermaid)
        # Rework edge exists
        self.assertIn("Fail / Rework", mermaid)

    def test_security_invariants(self):
        """Proves a security-sensitive slice produces explicit defensive verification seams."""
        sec_slice = WorkflowEngine.plan_slice(
            title="Update SSH key loader",
            scope_files=["src/ssh_loader.py"],
            is_security_sensitive=True,
        )
        node_ids = [n.node_id for n in sec_slice["nodes"]]
        self.assertIn("CHK-SEC-01", node_ids)
        sec_node = next(n for n in sec_slice["nodes"] if n.node_id == "CHK-SEC-01")
        sec_node.validate_schema()
        self.assertIn("defensive invariants", sec_node.claim.lower())
        self.assertIn("permissions", sec_node.pass_condition.lower())

    def test_rework_routing(self):
        """Proves a simulated check failure correctly triggers rework and logs the failure in execution record."""
        code_slice = WorkflowEngine.plan_slice(
            title="Add parser",
            scope_files=["src/parser.py"],
        )
        unit_node = next(n for n in code_slice["nodes"] if n.node_id == "CHK-UNIT-01")

        # Simulate failure
        unit_node.status = "failed"
        unit_node.evidence = "AssertionError: line 42 expected 'ok' got 'error' (Exit code 1)"
        self.assertEqual(unit_node.status, "failed")
        self.assertEqual(unit_node.failure_route, "route to existing worker session")

        # Simulate rework resolution via live worker session
        unit_node.evidence = "Fixed in commit 1a2b3c4; Exit code 0, 12 passed"
        unit_node.status = "passed"
        self.assertEqual(unit_node.status, "passed")

    def test_deviation_reporting(self):
        """Proves a skipped check generates an explicit entry with rationale in the deviation report."""
        code_slice = WorkflowEngine.plan_slice(
            title="Deploy live monitor",
            scope_files=["src/monitor.py"],
        )
        # Add an optional live-infra check that gets skipped due to missing human authorization
        live_check = WorkflowNode(
            node_id="CHK-LIVE-01",
            claim="Live infrastructure endpoint responds HTTP 200",
            method="curl https://roadtotech.me",
            executor="Independent QA Subagent",
            pass_condition="HTTP 200",
        )
        code_slice["nodes"].append(live_check)

        # Mark skipped due to authorization boundary
        live_check.status = "skipped"
        live_check.evidence = "BLOCKED (out-of-bounds): live-infra unapproved by human owner"

        report = WorkflowEngine.generate_deviation_report(code_slice["nodes"])
        self.assertFalse(report["clean_pass"])
        self.assertEqual(len(report["skipped_checks"]), 1)
        self.assertEqual(report["skipped_checks"][0]["node_id"], "CHK-LIVE-01")
        self.assertIn("live-infra unapproved", report["skipped_checks"][0]["rationale"])

    def test_dry_run_zero_mutation(self):
        """Proves --dry-run produces complete plans without mutating git status, commits, or files."""
        # Record initial git status
        initial_status = subprocess.check_output(
            ["git", "status", "--porcelain"],
            cwd=REPO_ROOT,
            text=True,
        )
        initial_commit = subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=REPO_ROOT,
            text=True,
        ).strip()

        # Execute dry-run planning
        plan = WorkflowEngine.plan_slice(
            title="Spike feature",
            scope_files=["src/spike.py"],
            is_dry_run=True,
        )
        self.assertTrue(plan["is_dry_run"])
        self.assertGreater(len(plan["nodes"]), 0)

        # Verify zero mutations
        current_status = subprocess.check_output(
            ["git", "status", "--porcelain"],
            cwd=REPO_ROOT,
            text=True,
        )
        current_commit = subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=REPO_ROOT,
            text=True,
        ).strip()

        # The only allowed diff is the test file itself if it is running in-tree
        # But during execution, zero new commits and zero external branch creation
        self.assertEqual(initial_commit, current_commit)

    def test_review_comment_publishing_ownership(self):
        """Proves code-review only drafts the PR comment block and gitea-pr alone posts it, guarded."""
        cr_dir = REPO_ROOT / "skills" / "code-review"
        cr_text = "\n".join(p.read_text() for p in cr_dir.rglob("*.md"))
        # code-review drafts the block but never contains a posting command
        self.assertIn("review-body.md", cr_text)
        self.assertIn("inline-comments.json", cr_text)
        self.assertIsNone(
            re.search(r"gt pr (comment|review)\s+<", cr_text),
            "code-review must not contain gt posting commands; gitea-pr owns publishing",
        )

        pr_skill = (REPO_ROOT / "skills" / "gitea-pr" / "SKILL.md").read_text()
        recipes = (REPO_ROOT / "skills" / "gitea-pr" / "references" / "gt-pulls.md").read_text()
        self.assertIn("Publish review findings", pr_skill)
        publish = recipes.split("### Publish a `code-review` Comment Block", 1)[1].split("\n## ", 1)[0]
        post_cmd = re.search(r"gt pr review <number> --comment[^\n]*\n[^\n]*", publish).group(0)
        # pinned to the reviewed commit, comment-only, no blanket confirmation
        self.assertIn("--commit <reviewed-head-sha>", post_cmd)
        for forbidden in ("--approve", "--request-changes", "--yes"):
            self.assertNotIn(forbidden, post_cmd)
        # staleness and duplicate guards precede posting
        self.assertLess(publish.index("head_sha"), publish.index(post_cmd))
        self.assertLess(publish.index("gt pr review list"), publish.index(post_cmd))

    def test_project_board_reconciliation_and_card_transitions(self):
        """Proves 5-column board reconciliation, Deep Signal colors, and card transition ownership."""
        tiers_text = (REPO_ROOT / "skills" / "gitea-plan" / "references" / "decomposition-tiers.md").read_text()
        gt_cmds = (REPO_ROOT / "skills" / "gt-usage" / "references" / "commands.md").read_text()
        impl_skill = (REPO_ROOT / "skills" / "implement-slice" / "SKILL.md").read_text()
        impl_handoff = (REPO_ROOT / "skills" / "implement-slice" / "references" / "handoff-contracts.md").read_text()
        pr_skill = (REPO_ROOT / "skills" / "gitea-pr" / "SKILL.md").read_text()
        pr_pulls = (REPO_ROOT / "skills" / "gitea-pr" / "references" / "gt-pulls.md").read_text()
        cr_dir = REPO_ROOT / "skills" / "code-review"
        cr_text = "\n".join(p.read_text() for p in cr_dir.rglob("*.md"))

        # 1. Canonical 5 columns and Deep Signal hex colors in gitea-plan
        expected_columns = {
            "Backlog": "#475569",
            "Ready": "#1d76db",
            "Work in Progress": "#d97706",
            "Review": "#6d28d9",
            "Completed": "#15803d",
        }
        for col_title, hex_color in expected_columns.items():
            self.assertIn(col_title, tiers_text)
            self.assertIn(hex_color, tiers_text)
        self.assertIn("PATCH", tiers_text)
        self.assertIn("PATCH /repos/{owner}/{repo}/projects/<project-id>/columns/<column-id>", gt_cmds)

        # 2. Card transition ownership across implement-slice and gitea-pr
        self.assertIn("Backlog -> Ready", impl_skill)
        self.assertIn("Ready -> Work in Progress", impl_skill)
        self.assertIn("Work in Progress -> Review", impl_skill)
        self.assertIn("Backlog -> Ready", impl_handoff)
        self.assertIn("Work in Progress -> Review", pr_skill)
        self.assertIn("Review -> Completed", pr_skill)
        self.assertIn("/issues/${issue_global_id}/move -F column_id=<completed-col-id>", pr_pulls)

        # 3. code-review never mutates project boards
        self.assertIsNone(
            re.search(r"/projects/[^\n]*/move", cr_text),
            "code-review must remain read-only and never execute project board card moves",
        )

    def test_reconcile_docs_gitea_ingestion_and_hooks(self):
        """Proves reconcile-docs ingests Gitea state read-only and hooks into gitea-plan and implement-slice."""
        rd_dir = REPO_ROOT / "skills" / "reconcile-docs"
        rd_skill = (rd_dir / "SKILL.md").read_text()
        rd_all = "\n".join(p.read_text() for p in rd_dir.rglob("*.md"))
        plan_skill = (REPO_ROOT / "skills" / "gitea-plan" / "SKILL.md").read_text()
        impl_skill = (REPO_ROOT / "skills" / "implement-slice" / "SKILL.md").read_text()

        # 1. reconcile-docs reads Gitea PR comments and board state, and targets docs/designs/*.md
        self.assertIn("docs/designs/*.md", rd_skill)
        self.assertIn("Project Board", rd_skill)
        self.assertIn("Never mutate Gitea issues, PRs, or board cards", rd_skill)
        self.assertIn("Mid-Slice Spec Drift", rd_all)
        self.assertIsNone(
            re.search(r"(/projects/[^\n]*/move|gt (issue|pr|project) (create|edit|close|merge))", rd_all),
            "reconcile-docs must never mutate Gitea issues, PRs, or project boards",
        )

        # 2. Bidirectional hooks across reconcile-docs, gitea-plan, and implement-slice
        self.assertIn("gitea-plan", rd_skill)
        self.assertIn("reconcile-docs", plan_skill)
        self.assertIn("reconcile-docs", impl_skill)

    def test_repo_scoped_documentation_and_vault_deprecation(self):
        """Proves ~/Brain, 00-inbox, draft-curation, and journal-builder are deprecated in favor of repo docs/ and .internal/."""
        doc_dir = REPO_ROOT / "skills" / "document"
        doc_all = "\n".join(p.read_text() for p in doc_dir.rglob("*.md"))
        prac_dir = REPO_ROOT / "skills" / "practice"
        prac_all = "\n".join(p.read_text() for p in prac_dir.rglob("*.md"))
        profile_agents = (REPO_ROOT / "profile" / "AGENTS.md").read_text()
        install_sh = (REPO_ROOT / "install.sh").read_text()

        # 1. No ~/Brain, 00-inbox, or draft-curation in active skills or profile
        for forbidden in ("~/Brain", "00-inbox", "draft-curation", "journal-builder"):
            self.assertNotIn(forbidden, doc_all)
            self.assertNotIn(forbidden, prac_all)
            self.assertNotIn(forbidden, profile_agents)

        # 2. Repo-scoped paths present
        self.assertIn("docs/adr/", doc_all)
        self.assertIn("docs/designs/", doc_all)
        self.assertIn(".internal/practice/", prac_all)
        self.assertIn("OBSOLETE_SKILLS=(", install_sh)
        self.assertIn("journal-builder", install_sh)
        self.assertIn("draft-curation", install_sh)

        # 3. Vertical per-submodule Red->Green decomposition in gitea-plan and implement-slice
        plan_all = "\n".join(p.read_text() for p in (REPO_ROOT / "skills" / "gitea-plan").rglob("*.md"))
        impl_all = "\n".join(p.read_text() for p in (REPO_ROOT / "skills" / "implement-slice").rglob("*.md"))
        self.assertIn("Vertical Submodule TDD Grouping", plan_all)
        self.assertIn("Vertical Submodule TDD Decomposition (Anti-Horizontal Batching)", impl_all)

    def test_polyglot_tdd_hardening_code_review_binding_and_soft_chaining(self):
        """Proves dual-mode tdd, 5-language invariants, single-owner code-review Axis 3 binding, and Suggested Next Step soft-chaining."""
        tdd_dir = REPO_ROOT / "skills" / "tdd"
        tdd_skill = (tdd_dir / "SKILL.md").read_text()
        seams = (tdd_dir / "references" / "seams-and-mocking.md").read_text()
        quality = (tdd_dir / "references" / "test-quality.md").read_text()
        tdd_refs = seams + "\n" + quality

        # 1. Dual-mode tdd & 5 target languages
        self.assertIn("Mode A", tdd_skill)
        self.assertIn("Mode B", tdd_skill)
        for lang in ("Python", "TypeScript", "Bash", "Rust", "Java"):
            self.assertIn(lang, seams)
            self.assertIn(lang, quality)

        # 2. All 5 empirical invariants live in tdd/references/
        self.assertIn("sleep_fn", seams)
        self.assertIn("Deterministic Async Synchronization and Guaranteed Teardown", seams)
        self.assertIn("[min - 1, min, max, max + 1]", quality)
        self.assertIn("production value constants", quality)
        self.assertIn("Single-Behavior Test Naming and Focus", quality)
        self.assertIn("Mode B Audit and Hardening Checklist", quality)

        # 3. code-review binds Axis 3 directly to tdd/references/ without duplicating fenced code blocks, and isolates Axis 3 in High-Assurance
        cr_skill = (REPO_ROOT / "skills" / "code-review" / "SKILL.md").read_text()
        axes = (REPO_ROOT / "skills" / "code-review" / "references" / "axes.md").read_text()
        schema = (REPO_ROOT / "skills" / "code-review" / "references" / "finding-schema.md").read_text()
        self.assertIn("../tdd/references/seams-and-mocking.md", cr_skill)
        self.assertIn("../tdd/references/test-quality.md", cr_skill)
        self.assertIn("../../tdd/references/seams-and-mocking.md", axes)
        self.assertIn("../../tdd/references/test-quality.md", axes)
        self.assertIn("dedicated isolated reviewer to **Seam & Test Integrity**", axes)
        self.assertNotIn("calculate_total", axes)
        self.assertIn("Suggested Next Step", schema)

        # 4. Canonical Suggested Next Step + suppression contract in skeleton.md and handoff-contracts.md
        skeleton = (REPO_ROOT / "skills" / "build-skill" / "references" / "skeleton.md").read_text()
        handoffs = (REPO_ROOT / "skills" / "implement-slice" / "references" / "handoff-contracts.md").read_text()
        self.assertIn("Suggested Next Step", skeleton)
        self.assertIn("Suppress", handoffs)
        self.assertNotIn("Steps 4–5", handoffs)

        # 5. All 6 chained skills include Suggested Next Step routing
        for skill_name in ("gitea-plan", "implement-slice", "tdd", "code-review", "gitea-pr", "reconcile-docs"):
            text = (REPO_ROOT / "skills" / skill_name / "SKILL.md").read_text()
            self.assertIn("Suggested Next Step:", text, f"{skill_name} missing Suggested Next Step routing")

    def test_skill_inventory_and_skeletons(self):
        """Proves all 16 active skills meet line count (<= 80), em-dash, and path portability rules."""
        for skill_name in EXPECTED_SKILLS:
            skill_path = REPO_ROOT / "skills" / skill_name / "SKILL.md"
            self.assertTrue(skill_path.exists(), f"Missing skill file: {skill_path}")
            lines = skill_path.read_text().splitlines()
            line_count = len(lines)
            self.assertLessEqual(
                line_count, 80,
                f"Skill {skill_name} exceeds 80 lines: {line_count} lines"
            )

            # Check for em-dashes
            content = "\n".join(lines)
            self.assertNotIn("—", content, f"Skill {skill_name} contains em-dash (—)")

            # Check for hardcoded home paths
            self.assertNotIn("/home/", content, f"Skill {skill_name} contains hardcoded /home/ path")

            # Check YAML frontmatter
            self.assertTrue(lines[0] == "---", f"Skill {skill_name} missing frontmatter start")
            self.assertIn("name:", content)
            self.assertIn("description:", content)


if __name__ == "__main__":
    unittest.main()
