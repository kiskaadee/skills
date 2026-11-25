#!/usr/bin/env python3
"""
Unit tests for skills/code-review/scripts/build_review.py.

Covers:
1. --paginate --slurp JSON flattening ([[...]] and [...]) for --reviews and --comments
2. Unified diff hunk parsing and validation (LEFT deleted, RIGHT added/modified/context)
3. Out-of-hunk, missing-file, and cross-file findings routed to review body
4. Monotonic max_id extraction from cr-review-meta and ### CR-NN headings across reviews/comments
5. Collapsible RV-* block from rv_checks[] and Triage Summary from triage_closures[]
6. Duplicate (head_sha, verdict) exits 2; ready superseding needs_rework on same head_sha exits 0
7. 3-rework-cycle cap exits 1 on 4th needs_rework, allows ready
8. Invalid JSON, invalid verdict, and missing required fields exit 1
"""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPT = REPO_ROOT / "skills" / "code-review" / "scripts" / "build_review.py"

SAMPLE_DIFF = """diff --git a/src/app.py b/src/app.py
index 1111111..2222222 100644
--- a/src/app.py
+++ b/src/app.py
@@ -10,4 +10,5 @@ def process(data):
     x = 1
-    old_call(data)
+    new_call(data)
+    extra_check(data)
     return x
diff --git a/src/removed.py b/src/removed.py
deleted file mode 100644
index 3333333..0000000
--- a/src/removed.py
+++ /dev/null
@@ -1,2 +0,0 @@
-def legacy():
-    return 0
"""


class TestBuildReview(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def _write_file(self, name, content):
        path = self.tmp / name
        if isinstance(content, str):
            path.write_text(content, encoding="utf-8")
        else:
            path.write_text(json.dumps(content), encoding="utf-8")
        return path

    def _run(self, input_data, diff_text=SAMPLE_DIFF, reviews=None, comments=None,
             head_sha="abc1234def5678", verdict="needs_rework"):
        input_path = self._write_file("input.json", input_data)
        diff_path = self._write_file("pr.diff", diff_text)
        reviews_path = self._write_file("reviews.json", [] if reviews is None else reviews)
        comments_path = self._write_file("comments.json", [] if comments is None else comments)
        return subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--input", str(input_path),
                "--diff", str(diff_path),
                "--reviews", str(reviews_path),
                "--comments", str(comments_path),
                "--head-sha", head_sha,
                "--verdict", verdict,
            ],
            capture_output=True,
            text=True,
        )

    def test_valid_anchored_left_and_right_findings_emit_inline_comments(self):
        payload_in = {
            "findings": [
                {
                    "path": "src/app.py",
                    "line": 11,
                    "side": "LEFT",
                    "severity": "High",
                    "axis": "Defensive Invariants",
                    "title": "Deleted validation call",
                    "body": "Removing old_call drops input validation.",
                },
                {
                    "path": "src/app.py",
                    "line": 12,
                    "side": "RIGHT",
                    "severity": "Medium",
                    "title": "Unbounded check",
                    "body": "extra_check lacks timeout.",
                },
                {
                    "path": "src/app.py",
                    "line": 10,
                    "side": "RIGHT",
                    "severity": "Low",
                    "title": "Context line anchor",
                    "body": "Context line inside hunk is valid on RIGHT.",
                },
                {
                    "path": "src/removed.py",
                    "line": 1,
                    "side": "LEFT",
                    "severity": "Medium",
                    "title": "Deleted file line anchor",
                    "body": "Deleted file line 1 is valid on LEFT.",
                },
            ]
        }
        res = self._run(payload_in, head_sha="deadbeef0011", verdict="needs_rework")
        self.assertEqual(res.returncode, 0, res.stderr)
        out = json.loads(res.stdout)
        self.assertEqual(out["commit_id"], "deadbeef0011")
        self.assertEqual(out["event"], "COMMENT")
        self.assertEqual(len(out["comments"]), 4)
        self.assertEqual(out["comments"][0]["path"], "src/app.py")
        self.assertEqual(out["comments"][0]["line"], 11)
        self.assertEqual(out["comments"][0]["side"], "LEFT")
        self.assertTrue(out["comments"][0]["body"].startswith("### CR-01:"))
        self.assertEqual(out["comments"][1]["side"], "RIGHT")
        self.assertTrue(out["comments"][1]["body"].startswith("### CR-02:"))
        self.assertTrue(out["comments"][2]["body"].startswith("### CR-03:"))
        self.assertEqual(out["comments"][3]["path"], "src/removed.py")
        self.assertEqual(out["comments"][3]["side"], "LEFT")
        self.assertTrue(out["comments"][3]["body"].startswith("### CR-04:"))
        self.assertNotIn("### Findings (Unanchored / Cross-File)", out["body"])
        self.assertIn(
            "<!-- cr-review-meta: max_id=04 head_sha=deadbeef0011 verdict=needs_rework -->",
            out["body"],
        )

    def test_unanchored_out_of_hunk_missing_file_and_cross_file_move_to_body(self):
        payload_in = {
            "findings": [
                {
                    "path": "src/app.py",
                    "line": 99,
                    "side": "RIGHT",
                    "severity": "Medium",
                    "title": "Out of hunk line",
                    "body": "Line 99 is not in diff hunk.",
                },
                {
                    "path": "src/app.py",
                    "line": 10,
                    "side": "LEFT",
                    "severity": "Low",
                    "title": "Context line on LEFT rejected",
                    "body": "Context line is not a deleted line on LEFT.",
                },
                {
                    "path": "src/nonexistent.py",
                    "line": 5,
                    "side": "RIGHT",
                    "severity": "High",
                    "title": "Missing file",
                    "body": "File is not in diff.",
                },
                {
                    "path": None,
                    "line": None,
                    "side": None,
                    "severity": "High",
                    "title": "Cross-file architectural drift",
                    "body": "Multiple modules violate layering.",
                },
            ]
        }
        res = self._run(payload_in, head_sha="aaaa1111", verdict="needs_rework")
        self.assertEqual(res.returncode, 0, res.stderr)
        out = json.loads(res.stdout)
        self.assertEqual(out["comments"], [])
        self.assertIn("### Findings (Unanchored / Cross-File)", out["body"])
        for idx in ("### CR-01:", "### CR-02:", "### CR-03:", "### CR-04:"):
            self.assertIn(idx, out["body"])
        self.assertIn("<!-- cr-review-meta: max_id=04 head_sha=aaaa1111 verdict=needs_rework -->", out["body"])

    def test_slurp_and_flat_pagination_monotonic_max_id_and_three_digit_rollover(self):
        # Slurped nested pages for reviews: [[...], [...]]
        slurped_reviews = [
            [
                {
                    "body": "Prior review\n<!-- cr-review-meta: max_id=05 head_sha=oldsha1 verdict=needs_rework -->"
                }
            ],
            [
                {
                    "body": "### Findings (Unanchored / Cross-File)\n### CR-98: Old unanchored\nBody"
                }
            ],
        ]
        # Flat list for comments with CR-99
        flat_comments = [
            {"body": "### CR-99: Inline finding\nDetails"}
        ]
        payload_in = {
            "findings": [
                {
                    "path": "src/app.py",
                    "line": 11,
                    "side": "RIGHT",
                    "severity": "Medium",
                    "title": "Hundredth finding",
                    "body": "Should roll over to CR-100.",
                }
            ]
        }
        res = self._run(
            payload_in,
            reviews=slurped_reviews,
            comments=flat_comments,
            head_sha="newsha99",
            verdict="needs_rework",
        )
        self.assertEqual(res.returncode, 0, res.stderr)
        out = json.loads(res.stdout)
        self.assertEqual(len(out["comments"]), 1)
        self.assertTrue(out["comments"][0]["body"].startswith("### CR-100:"))
        self.assertIn(
            "<!-- cr-review-meta: max_id=100 head_sha=newsha99 verdict=needs_rework -->",
            out["body"],
        )

    def test_slurped_comments_also_flattened(self):
        slurped_comments = [
            [{"body": "### CR-03: First\nDetails"}],
            [{"body": "### CR-07: Seventh\nDetails"}],
        ]
        payload_in = {
            "findings": [
                {
                    "path": "src/app.py",
                    "line": 11,
                    "side": "RIGHT",
                    "severity": "Low",
                    "title": "Next finding",
                    "body": "Should be CR-08.",
                }
            ]
        }
        res = self._run(
            payload_in,
            reviews=[[]],
            comments=slurped_comments,
            head_sha="sha0008",
            verdict="needs_rework",
        )
        self.assertEqual(res.returncode, 0, res.stderr)
        out = json.loads(res.stdout)
        self.assertTrue(out["comments"][0]["body"].startswith("### CR-08:"))

    def test_rv_checks_collapsible_block_and_triage_closures_summary(self):
        payload_in = {
            "findings": [],
            "rv_checks": [
                {
                    "id": "RV-01",
                    "purpose": "Concurrent submission returns 409",
                    "scope": "local",
                    "pass_condition": "HTTP 409 returned",
                    "fail_signal": "FAIL if HTTP 200 or 500",
                    "command": "./scripts/check_conflict.sh",
                }
            ],
            "triage_closures": [
                {"id": "CR-01", "exit": "B", "resolution": "Promoted to #45"},
                {"id": "CR-02", "exit": "C", "resolution": "Dismissed: false positive on fixture"},
            ],
        }
        prior_reviews = [
            {
                "body": "Prior\n<!-- cr-review-meta: max_id=02 head_sha=sha_same verdict=needs_rework -->"
            }
        ]
        # ready superseding needs_rework on same head_sha must exit 0
        res = self._run(
            payload_in,
            reviews=prior_reviews,
            head_sha="sha_same",
            verdict="ready",
        )
        self.assertEqual(res.returncode, 0, res.stderr)
        out = json.loads(res.stdout)
        self.assertEqual(out["comments"], [])
        self.assertIn("<details>", out["body"])
        self.assertIn("RV-01", out["body"])
        self.assertIn("./scripts/check_conflict.sh", out["body"])
        self.assertIn("FAIL if HTTP 200 or 500", out["body"])
        self.assertIn("### Triage Summary", out["body"])
        self.assertIn("CR-01", out["body"])
        self.assertIn("Promoted to #45", out["body"])
        self.assertIn("Dismissed: false positive on fixture", out["body"])
        self.assertIn(
            "<!-- cr-review-meta: max_id=02 head_sha=sha_same verdict=ready -->",
            out["body"],
        )

    def test_duplicate_head_sha_and_verdict_exits_2_with_empty_stdout(self):
        prior_reviews = [
            [
                {
                    "body": "Already reviewed\n<!-- cr-review-meta: max_id=01 head_sha=dup1234 verdict=ready -->"
                }
            ]
        ]
        res = self._run({"findings": []}, reviews=prior_reviews, head_sha="dup1234", verdict="ready")
        self.assertEqual(res.returncode, 2)
        self.assertEqual(res.stdout.strip(), "")
        self.assertIn("duplicate", res.stderr.lower())

    def test_rework_cycle_cap_allows_third_needs_rework(self):
        prior_reviews = [
            {"body": "<!-- cr-review-meta: max_id=01 head_sha=sha1 verdict=needs_rework -->"},
            {"body": "<!-- cr-review-meta: max_id=02 head_sha=sha2 verdict=needs_rework -->"},
        ]
        res = self._run(
            {"findings": []},
            reviews=prior_reviews,
            head_sha="sha3",
            verdict="needs_rework",
        )
        self.assertEqual(res.returncode, 0, res.stderr)
        out = json.loads(res.stdout)
        self.assertIn("<!-- cr-review-meta: max_id=02 head_sha=sha3 verdict=needs_rework -->", out["body"])

    def test_rework_cycle_cap_blocks_fourth_needs_rework(self):
        prior_reviews = [
            {"body": "<!-- cr-review-meta: max_id=01 head_sha=sha1 verdict=needs_rework -->"},
            {"body": "<!-- cr-review-meta: max_id=02 head_sha=sha2 verdict=needs_rework -->"},
            {"body": "<!-- cr-review-meta: max_id=03 head_sha=sha3 verdict=needs_rework -->"},
        ]
        res_blocked = self._run(
            {"findings": []},
            reviews=prior_reviews,
            head_sha="sha4",
            verdict="needs_rework",
        )
        self.assertEqual(res_blocked.returncode, 1)
        self.assertEqual(res_blocked.stdout.strip(), "")
        self.assertIn("3-rework-cycle cap", res_blocked.stderr.lower())

    def test_rework_cycle_cap_allows_ready_after_three_reworks(self):
        prior_reviews = [
            {"body": "<!-- cr-review-meta: max_id=01 head_sha=sha1 verdict=needs_rework -->"},
            {"body": "<!-- cr-review-meta: max_id=02 head_sha=sha2 verdict=needs_rework -->"},
            {"body": "<!-- cr-review-meta: max_id=03 head_sha=sha3 verdict=needs_rework -->"},
        ]
        res_ready = self._run(
            {"findings": []},
            reviews=prior_reviews,
            head_sha="sha4",
            verdict="ready",
        )
        self.assertEqual(res_ready.returncode, 0, res_ready.stderr)
        out = json.loads(res_ready.stdout)
        self.assertIn("<!-- cr-review-meta: max_id=03 head_sha=sha4 verdict=ready -->", out["body"])

    def test_triage_closure_null_id_defaults_to_placeholder(self):
        res = self._run(
            {
                "findings": [],
                "triage_closures": [
                    {"id": None, "exit": "C", "resolution": "Dismissed: false positive"}
                ],
            },
            head_sha="nullid1",
            verdict="ready",
        )
        self.assertEqual(res.returncode, 0, res.stderr)
        out = json.loads(res.stdout)
        self.assertIn("**CR-??**", out["body"])
        self.assertNotIn("**None**", out["body"])

    def test_invalid_inputs_exit_1(self):
        cases = [
            ("invalid_json", "{not valid json", "needs_rework"),
            ("invalid_verdict", {"findings": []}, "approved"),
            ("missing_findings_key", {"rv_checks": []}, "needs_rework"),
            ("missing_title", {"findings": [{"severity": "High", "body": "Missing title"}]}, "needs_rework"),
            (
                "invalid_side",
                {
                    "findings": [
                        {
                            "path": "src/app.py",
                            "line": 11,
                            "side": "CENTER",
                            "severity": "Low",
                            "title": "Bad side",
                            "body": "Invalid side enum.",
                        }
                    ]
                },
                "needs_rework",
            ),
            (
                "non_positive_line_zero",
                {
                    "findings": [
                        {
                            "path": "src/app.py",
                            "line": 0,
                            "side": "RIGHT",
                            "severity": "Low",
                            "title": "Zero line",
                            "body": "Line 0 is invalid.",
                        }
                    ]
                },
                "needs_rework",
            ),
            (
                "boolean_line",
                {
                    "findings": [
                        {
                            "path": "src/app.py",
                            "line": True,
                            "side": "RIGHT",
                            "severity": "Low",
                            "title": "Bool line",
                            "body": "Boolean line is invalid.",
                        }
                    ]
                },
                "needs_rework",
            ),
        ]
        for label, payload, verdict in cases:
            with self.subTest(case=label):
                res = self._run(payload, verdict=verdict)
                self.assertEqual(res.returncode, 1, res.stderr)

    def test_new_file_multi_hunk_and_empty_diff_handling(self):
        new_and_multi_hunk_diff = """diff --git a/src/brand_new.py b/src/brand_new.py
new file mode 100644
index 0000000..1111111
--- /dev/null
+++ b/src/brand_new.py
@@ -0,0 +1,3 @@
+def greet(name):
+    return f"hi {name}"
+
diff --git a/src/multi.py b/src/multi.py
index 1111111..2222222 100644
--- a/src/multi.py
+++ b/src/multi.py
@@ -2,3 +2,4 @@ def first():
     a = 1
+    b = 2
     return a
@@ -20,3 +21,4 @@ def second():
     c = 3
+    d = 4
     return c
"""
        payload_in = {
            "findings": [
                {
                    "path": "src/brand_new.py",
                    "line": 2,
                    "side": "RIGHT",
                    "severity": "Medium",
                    "title": "New file anchor",
                    "body": "Newly added file line 2 anchors on RIGHT.",
                },
                {
                    "path": "src/multi.py",
                    "line": 3,
                    "side": "RIGHT",
                    "severity": "Low",
                    "title": "First hunk anchor",
                    "body": "Added line in hunk 1 anchors on RIGHT.",
                },
                {
                    "path": "src/multi.py",
                    "line": 22,
                    "side": "RIGHT",
                    "severity": "Low",
                    "title": "Second hunk anchor",
                    "body": "Added line in hunk 2 anchors on RIGHT.",
                },
                {
                    "path": "src/multi.py",
                    "line": 12,
                    "side": "RIGHT",
                    "severity": "Medium",
                    "title": "Gap between hunks",
                    "body": "Line 12 lies between hunks and must move to body.",
                },
            ]
        }
        res = self._run(
            payload_in,
            diff_text=new_and_multi_hunk_diff,
            head_sha="multi1234",
            verdict="needs_rework",
        )
        self.assertEqual(res.returncode, 0, res.stderr)
        out = json.loads(res.stdout)
        self.assertEqual(len(out["comments"]), 3)
        self.assertEqual(
            [(c["path"], c["line"], c["side"]) for c in out["comments"]],
            [
                ("src/brand_new.py", 2, "RIGHT"),
                ("src/multi.py", 3, "RIGHT"),
                ("src/multi.py", 22, "RIGHT"),
            ],
        )
        self.assertIn("### Findings (Unanchored / Cross-File)", out["body"])
        self.assertIn("### CR-04: Gap between hunks", out["body"])

        # Empty diff routes all findings to body
        empty_res = self._run(
            {
                "findings": [
                    {
                        "path": "src/brand_new.py",
                        "line": 2,
                        "side": "RIGHT",
                        "severity": "High",
                        "title": "Unanchored on empty diff",
                        "body": "Cannot anchor when diff is empty.",
                    }
                ]
            },
            diff_text="",
            head_sha="empty0000",
            verdict="needs_rework",
        )
        self.assertEqual(empty_res.returncode, 0, empty_res.stderr)
        empty_out = json.loads(empty_res.stdout)
        self.assertEqual(empty_out["comments"], [])
        self.assertIn("### Findings (Unanchored / Cross-File)", empty_out["body"])
        self.assertIn("### CR-01: Unanchored on empty diff", empty_out["body"])


if __name__ == "__main__":
    unittest.main()
