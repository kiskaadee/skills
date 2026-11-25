#!/usr/bin/env python3
"""
test_skills_behavioral_contracts.py
Deterministic behavioral contract test suite for kiskaadee/skills.

Verifies:
1. Anti-hallucination resource ID querying rules (projects dynamic GraphQL/REST + gt-usage --json)
2. Review comment publishing ownership (code-review via build_review.py; implement read-only on reviews)
3. Project board 5-column reconciliation, fixed GitHub color enums, and transition ownership
4. reconcile-docs read-only GitHub ingestion and bidirectional hooks with projects / implement
5. Repo-scoped documentation boundaries and vault deprecation
6. Polyglot TDD hardening (Mode A/B, 5 languages, 5 empirical invariants) and code-review Axis 3 binding
7. Suggested Next Step soft-chaining and delegated footer suppression
8. Subagent provenance output-slot guards for High-Assurance code-review and projects reproducibility audit
9. Core GitHub delivery skill contracts (projects, implement, code-review, verify)
10. Isolated install.sh check exit codes and repo-scoped dangling-symlink pruning
11. Skill inventory, line count (<= 80), em-dash absence, and path portability
"""

import os
import re
import subprocess
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent

# Canonical Active Portable Skills list from install.sh (sorted)
EXPECTED_SKILLS = [
    "build-skill",
    "code-review",
    "derive-skill",
    "diagnose",
    "document",
    "git-manager",
    "gt-usage",
    "implement",
    "inspect-flake-update",
    "nix-devshell",
    "practice",
    "projects",
    "reconcile-docs",
    "tdd",
    "verify",
]

RETIRED_LEGACY_SKILLS = [
    "gitea-plan",
    "gitea-pr",
    "implement-slice",
    "verify-slice",
]


class TestSkillsBehavioralContracts(unittest.TestCase):

    def test_resource_id_querying_rules(self):
        """Proves planning recipes forbid hardcoded ID guessing and require dynamic queries."""
        gt_usage_cmd = REPO_ROOT / "skills" / "gt-usage" / "references" / "commands.md"
        self.assertTrue(gt_usage_cmd.exists())
        gt_content = gt_usage_cmd.read_text()

        # Standalone gt-usage still mandates --json for querying IDs
        self.assertIn("gt milestone list --json id,title,state,url", gt_content)
        self.assertIn("gt issue list --json id,number,title,state,url", gt_content)
        self.assertIn("gt project list --json id,title,state,url", gt_content)

        # Anti-hallucination check: projects explicitly forbids guessing IDs or constructing /milestone/1
        projects_skill = (REPO_ROOT / "skills" / "projects" / "SKILL.md").read_text()
        projects_v2 = (REPO_ROOT / "skills" / "projects" / "references" / "github-projects-v2.md").read_text()
        self.assertIn("Resolve all IDs dynamically", projects_skill)
        self.assertIn("/milestone/1", projects_skill)
        self.assertIn("Never hardcode or guess IDs", projects_v2)
        self.assertIn("gh api repos/{owner}/{repo}/milestones", projects_v2)

    def test_review_comment_publishing_ownership(self):
        """Proves code-review owns guarded GitHub PR review publishing and implement never publishes reviews."""
        cr_dir = REPO_ROOT / "skills" / "code-review"
        cr_skill = (cr_dir / "SKILL.md").read_text()
        cr_schema = (cr_dir / "references" / "finding-schema.md").read_text()
        cr_text = "\n".join(p.read_text() for p in cr_dir.rglob("*.md"))

        self.assertIn("build_review.py", cr_skill)
        self.assertIn("Pending Triage", cr_text)
        self.assertIn("Exit A", cr_schema)
        self.assertIn("Exit B", cr_schema)
        self.assertIn("Exit C", cr_schema)
        self.assertNotIn("Accepted Trade-off", cr_text)
        self.assertIn("read-only regarding the codebase", cr_schema)
        self.assertIn('"event": "COMMENT"', cr_schema)
        self.assertIn('"commit_id": "<head_sha>"', cr_schema)
        self.assertIn("Never emit `APPROVE` or `REQUEST_CHANGES`", cr_schema)
        self.assertIn("no open PR was found", cr_skill)

        # implement never publishes PR reviews or inline review comments
        impl_skill = (REPO_ROOT / "skills" / "implement" / "SKILL.md").read_text()
        impl_pr = (REPO_ROOT / "skills" / "implement" / "references" / "pr-and-drift.md").read_text()
        self.assertIn("never publish PR review comments", impl_skill)
        self.assertIn("`code-review` is the sole owner of PR review publishing", impl_pr)

    def test_project_board_reconciliation_and_card_transitions(self):
        """Proves 5-column GitHub Projects v2 board schema, fixed color enums, and transition ownership."""
        contract_text = (REPO_ROOT / "skills" / "projects" / "references" / "planning-contract.md").read_text()
        v2_text = (REPO_ROOT / "skills" / "projects" / "references" / "github-projects-v2.md").read_text()
        impl_skill = (REPO_ROOT / "skills" / "implement" / "SKILL.md").read_text()
        impl_pr = (REPO_ROOT / "skills" / "implement" / "references" / "pr-and-drift.md").read_text()
        verify_skill = (REPO_ROOT / "skills" / "verify" / "SKILL.md").read_text()
        verify_closeout = (REPO_ROOT / "skills" / "verify" / "references" / "closeout-and-abort.md").read_text()
        cr_dir = REPO_ROOT / "skills" / "code-review"
        cr_text = "\n".join(p.read_text() for p in cr_dir.rglob("*.md"))

        # 1. Canonical 5 columns and fixed GitHub color enums in projects (no hex colors)
        expected_columns = {
            "Backlog": "GRAY",
            "Ready": "BLUE",
            "Work in Progress": "YELLOW",
            "Review": "PURPLE",
            "Completed": "GREEN",
        }
        for col_title, color_enum in expected_columns.items():
            self.assertIn(col_title, contract_text)
            self.assertIn(color_enum, contract_text)
            self.assertIn(col_title, v2_text)
            self.assertIn(color_enum, v2_text)
        self.assertIsNone(
            re.search(r"#[0-9a-fA-F]{6}\b", contract_text + "\n" + v2_text),
            "projects must use GitHub color enums rather than Gitea #RRGGBB hex colors",
        )

        # 2. Card transition ownership across implement and verify
        self.assertIn("Ready -> Work in Progress", impl_skill)
        self.assertIn("keep the\n   board card in `Work in Progress`", impl_skill)
        self.assertIn("Never\n  move the card to `Review` here", impl_pr)
        self.assertIn("Work in Progress -> Review", verify_skill)
        self.assertIn("Review -> Completed", verify_skill)
        self.assertIn("Review -> Work in Progress", verify_skill)
        self.assertIn("updateProjectV2ItemFieldValue", verify_closeout)

        # 3. code-review never mutates project boards
        self.assertIsNone(
            re.search(r"(updateProjectV2ItemFieldValue|/projects/[^\n]*/move)", cr_text),
            "code-review must remain read-only and never execute project board card moves",
        )

    def test_reconcile_docs_github_ingestion_and_hooks(self):
        """Proves reconcile-docs ingests GitHub state read-only and hooks into projects and implement."""
        rd_dir = REPO_ROOT / "skills" / "reconcile-docs"
        rd_skill = (rd_dir / "SKILL.md").read_text()
        rd_all = "\n".join(p.read_text() for p in rd_dir.rglob("*.md"))
        projects_skill = (REPO_ROOT / "skills" / "projects" / "SKILL.md").read_text()
        verify_skill = (REPO_ROOT / "skills" / "verify" / "SKILL.md").read_text()

        # 1. reconcile-docs reads GitHub PRs, milestones, and board state read-only, targeting docs/designs/*.md
        self.assertIn("docs/designs/*.md", rd_skill)
        self.assertIn("Project Board", rd_skill)
        self.assertIn("gh repo view --json url", rd_skill)
        self.assertIn("gh pr list --state merged", rd_skill)
        self.assertIn("Never mutate GitHub issues, PRs, or board cards", rd_skill)
        self.assertIn("Mid-Slice Spec Drift", rd_all)
        self.assertIsNone(
            re.search(r"(updateProjectV2ItemFieldValue|gh (issue|pr) (create|edit|close|merge))", rd_all),
            "reconcile-docs must never mutate GitHub issues, PRs, or project boards",
        )

        # 2. Bidirectional hooks across reconcile-docs, projects, implement, and verify
        self.assertIn("projects", rd_skill)
        self.assertIn("implement", rd_skill)
        self.assertIn("reconcile-docs", projects_skill)
        self.assertIn("reconcile-docs", verify_skill)

    def test_repo_scoped_documentation_and_vault_deprecation(self):
        """Proves ~/Brain, 00-inbox, draft-curation, and journal-builder are deprecated in favor of repo docs/ and .internal/."""
        doc_all = "\n".join(p.read_text() for p in (REPO_ROOT / "skills" / "document").rglob("*.md"))
        prac_all = "\n".join(p.read_text() for p in (REPO_ROOT / "skills" / "practice").rglob("*.md"))
        projects_all = "\n".join(p.read_text() for p in (REPO_ROOT / "skills" / "projects").rglob("*.md"))
        impl_all = "\n".join(p.read_text() for p in (REPO_ROOT / "skills" / "implement").rglob("*.md"))
        profile_agents = (REPO_ROOT / "profile" / "AGENTS.md").read_text()
        install_sh = (REPO_ROOT / "install.sh").read_text()

        # 1. No ~/Brain, 00-inbox, draft-curation, or journal-builder in active skills or profile
        for forbidden in ("~/Brain", "00-inbox", "draft-curation", "journal-builder"):
            self.assertNotIn(forbidden, doc_all)
            self.assertNotIn(forbidden, prac_all)
            self.assertNotIn(forbidden, projects_all)
            self.assertNotIn(forbidden, impl_all)
            self.assertNotIn(forbidden, profile_agents)

        # 2. Repo-scoped paths present
        self.assertIn("docs/adr/", doc_all)
        self.assertIn("docs/designs/", doc_all)
        self.assertIn(".internal/practice/", prac_all)
        self.assertIn("docs/designs/*.md", projects_all)
        self.assertIn(".internal/", projects_all)
        self.assertIn("docs/designs/*.md", impl_all)
        self.assertIn(".internal/", impl_all)
        self.assertIn("OBSOLETE_SKILLS=(", install_sh)
        self.assertIn("journal-builder", install_sh)
        self.assertIn("draft-curation", install_sh)

        # 3. Vertical Submodule TDD Grouping in projects
        self.assertIn("Vertical Submodule TDD Grouping", projects_all)

    def test_tdd_supports_dual_mode_with_mode_b_gates(self):
        """Proves tdd supports Mode A and Mode B with production-signature Your call and sensitivity Done when gates."""
        tdd_skill = (REPO_ROOT / "skills" / "tdd" / "SKILL.md").read_text()
        self.assertIn("Mode A", tdd_skill)
        self.assertIn("Mode B", tdd_skill)
        self.assertIn("Mode B production signature widening", tdd_skill)
        self.assertIn("observed failing under fault/boundary check", tdd_skill)

    def test_tdd_references_cover_five_target_languages(self):
        """Proves tdd seam and quality references cover Python, TypeScript, Bash, Rust, and Java."""
        tdd_dir = REPO_ROOT / "skills" / "tdd"
        seams = (tdd_dir / "references" / "seams-and-mocking.md").read_text()
        quality = (tdd_dir / "references" / "test-quality.md").read_text()
        for lang in ("Python", "TypeScript", "Bash", "Rust", "Java"):
            self.assertIn(lang, seams)
            self.assertIn(lang, quality)

    def test_tdd_references_document_five_empirical_invariants(self):
        """Proves tdd references codify injected timing, deterministic waits/teardown, BVA bounds, constant bans, and naming."""
        tdd_dir = REPO_ROOT / "skills" / "tdd"
        seams = (tdd_dir / "references" / "seams-and-mocking.md").read_text()
        quality = (tdd_dir / "references" / "test-quality.md").read_text()
        self.assertIn("sleep_fn", seams)
        self.assertIn("Deterministic Async Synchronization and Guaranteed Teardown", seams)
        self.assertIn("[min - 1, min, max, max + 1]", quality)
        self.assertIn("[min - 1, min]", quality)
        self.assertIn("[max, max + 1]", quality)
        self.assertIn("production value constants", quality)
        self.assertIn("Single-Behavior Test Naming and Focus", quality)
        self.assertIn("Mode B Audit and Hardening Checklist", quality)

    def test_code_review_binds_axis_3_to_tdd_references(self):
        """Proves code-review links Axis 3 to tdd/references/, isolates Axis 3 in High-Assurance, and avoids fenced-block duplication."""
        cr_skill = (REPO_ROOT / "skills" / "code-review" / "SKILL.md").read_text()
        axes = (REPO_ROOT / "skills" / "code-review" / "references" / "axes.md").read_text()
        schema = (REPO_ROOT / "skills" / "code-review" / "references" / "finding-schema.md").read_text()
        self.assertIn("../tdd/references/seams-and-mocking.md", cr_skill)
        self.assertIn("../tdd/references/test-quality.md", cr_skill)
        self.assertIn("../../tdd/references/seams-and-mocking.md", axes)
        self.assertIn("../../tdd/references/test-quality.md", axes)
        self.assertIn("dedicated isolated reviewer to **Seam & Test Integrity**", axes)
        self.assertNotIn("```", axes)
        self.assertIn("Suggested Next Step", schema)

    def test_skeleton_defines_suggested_next_step_suppression(self):
        """Proves skeleton.md owns Suggested Next Step suppression and implement enforces it on delegated workers."""
        skeleton = (REPO_ROOT / "skills" / "build-skill" / "references" / "skeleton.md").read_text()
        impl_skill = (REPO_ROOT / "skills" / "implement" / "SKILL.md").read_text()
        impl_roles = (REPO_ROOT / "skills" / "implement" / "references" / "decomposition-and-roles.md").read_text()
        self.assertIn("Suggested Next Step", skeleton)
        self.assertIn("Delegated subagent runs omit that footer", skeleton)
        self.assertIn("suppress\n  when delegated", impl_skill)
        self.assertIn("Suppress any standalone `Suggested Next Step:` footer", impl_roles)

    def test_chained_skills_include_suggested_next_step_routing(self):
        """Proves all 6 chained skills include Suggested Next Step routing and valid relative markdown links."""
        link_re = re.compile(r"\]\(([^)#]+\.md)(?:#[^)]+)?\)")
        for skill_name in ("projects", "implement", "tdd", "code-review", "verify", "reconcile-docs"):
            skill_path = REPO_ROOT / "skills" / skill_name / "SKILL.md"
            text = skill_path.read_text()
            self.assertIn("Suggested Next Step:", text, f"{skill_name} missing Suggested Next Step routing")
            for rel_link in link_re.findall(text):
                resolved = (skill_path.parent / rel_link).resolve()
                self.assertTrue(resolved.exists(), f"{skill_name} has broken relative link: {rel_link} -> {resolved}")

    def test_subagent_provenance_output_slot_guards(self):
        """Proves High-Assurance code-review and Medium/Large projects require subagent provenance slots in output templates."""
        cr_skill = (REPO_ROOT / "skills" / "code-review" / "SKILL.md").read_text()
        cr_schema = (REPO_ROOT / "skills" / "code-review" / "references" / "finding-schema.md").read_text()
        projects_skill = (REPO_ROOT / "skills" / "projects" / "SKILL.md").read_text()
        projects_tiers = (REPO_ROOT / "skills" / "projects" / "references" / "tiers-and-audit.md").read_text()

        self.assertIn("record\n   both subagent IDs in `Execution Mode`", cr_skill)
        self.assertIn("Dedicated Axis 3 Tests subagent `<id>`", cr_schema)
        self.assertIn("### Reproducibility Audit:", projects_skill)
        self.assertIn("### Reproducibility Audit:", projects_tiers)

    def test_projects_contract_and_dynamic_graphql_state_machine(self):
        """Proves projects defines state-free project_number contract and dynamic owner.projectV2 / issue.projectItems queries."""
        contract = (REPO_ROOT / "skills" / "projects" / "references" / "planning-contract.md").read_text()
        v2 = (REPO_ROOT / "skills" / "projects" / "references" / "github-projects-v2.md").read_text()

        self.assertIn("project_number: <int>", contract)
        self.assertIn("Zero brittle Node IDs", contract)
        self.assertIn("gh repo view --json url", contract)
        self.assertIn("owner.projectV2(number: $project_number)", v2)
        self.assertIn("addProjectV2ItemById", v2)
        self.assertIn("issue.projectItems", v2)
        self.assertIn("updateProjectV2ItemFieldValue", v2)
        self.assertIn("DATE", v2)

    def test_implement_preflight_checkpointing_and_timeout_wrapper(self):
        """Proves implement defines preflight classifications, --dry-run, git-common-dir checkpointing without tuxedo, and setsid timeout."""
        preflight = (REPO_ROOT / "skills" / "implement" / "references" / "preflight.md").read_text()
        roles = (REPO_ROOT / "skills" / "implement" / "references" / "decomposition-and-roles.md").read_text()

        for classification in (
            "CLEAN_BASE",
            "EXISTING_SLICE_BRANCH",
            "ADOPTABLE_DIFF",
            "CONFLICTING_STATE",
            "WRONG_BASE",
        ):
            self.assertIn(classification, preflight)

        self.assertIn("--dry-run", preflight)
        self.assertIn("zero mutations", preflight)
        self.assertIn("git rev-parse --git-common-dir", preflight)
        self.assertIn("implement-state/${branch_slug}.txt", preflight)
        self.assertIn("Never\n  invoke `tuxedo`", preflight)

        self.assertIn("setsid timeout -k 10 <N>s <cmd> < /dev/null", roles)
        self.assertIn("CI=true", roles)
        self.assertIn("GIT_TERMINAL_PROMPT=0", roles)
        self.assertIn("PAGER=cat", roles)
        for timeout_tier in ("60s", "180s", "600s"):
            self.assertIn(timeout_tier, roles)

    def test_code_review_build_review_and_metadata_contract(self):
        """Proves code-review integrates build_review.py, monotonic CR-XX, cr-review-meta verdict, RV-* body checks, and local no-PR notice."""
        build_script = REPO_ROOT / "skills" / "code-review" / "scripts" / "build_review.py"
        self.assertTrue(build_script.exists(), "build_review.py must exist under skills/code-review/scripts/")

        cr_skill = (REPO_ROOT / "skills" / "code-review" / "SKILL.md").read_text()
        cr_schema = (REPO_ROOT / "skills" / "code-review" / "references" / "finding-schema.md").read_text()

        self.assertIn("skills/code-review/scripts/build_review.py", cr_skill)
        self.assertIn("cr-review-meta: max_id=NN head_sha=<sha> verdict=ready|needs_rework", cr_schema)
        self.assertIn("CR-01", cr_schema)
        self.assertIn("RV-*", cr_schema)
        self.assertIn("3-rework-cycle cap", cr_schema)
        self.assertIn("No open GitHub PR found; findings reported locally.", cr_schema)

    def test_verify_three_phase_flow_and_zero_todo_txt(self):
        """Proves verify defines 3-phase flow, zero todo.txt responsibility, gh pr ready -> Review, and post-merge Completed."""
        verify_skill = (REPO_ROOT / "skills" / "verify" / "SKILL.md").read_text()
        qa = (REPO_ROOT / "skills" / "verify" / "references" / "qa-dispositions.md").read_text()
        closeout = (REPO_ROOT / "skills" / "verify" / "references" / "closeout-and-abort.md").read_text()

        self.assertIn("Phase 1: Read-Only Runtime QA and CI", verify_skill)
        self.assertIn("Phase 2: Promotion", verify_skill)
        self.assertIn("Phase 3: Human Merge Gate and Closeout", verify_skill)
        self.assertIn("zero\n`todo.txt` cleanup responsibility", verify_skill)
        self.assertIn("Zero `todo.txt` responsibility", closeout)

        self.assertIn("cr-review-meta", qa)
        self.assertIn("verdict=ready", qa)
        self.assertIn("gh pr checks", qa)
        for disposition in (
            "PASS",
            "FAIL",
            "BLOCKED (env/fixture)",
            "BLOCKED (out-of-bounds)",
            "INCONCLUSIVE",
        ):
            self.assertIn(disposition, qa)

        self.assertIn("gh pr ready", closeout)
        self.assertIn("Work in Progress -> Review", closeout)
        self.assertIn("Review -> Completed", closeout)
        self.assertIn("gh pr ready --undo", closeout)
        self.assertIn("gh pr close", closeout)

    def test_install_sh_check_exit_codes_and_dangling_symlink_pruning(self):
        """Proves install.sh check exits 1 on missing/obsolete skills, exits 0 when clean, and prunes only repo-scoped dangling symlinks."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            target_skills = tmp_path / "skills"
            target_agents = tmp_path / "agents"
            target_profile = tmp_path / "AGENTS.md"
            target_skills.mkdir()
            target_agents.mkdir()

            env = os.environ.copy()
            env["PROFILE_TARGET"] = str(target_profile)
            env["AGENTS_DIR_TARGET"] = str(target_agents)

            # 1. Empty target must fail check with exit 1
            res_empty = subprocess.run(
                ["./install.sh", "--target", str(target_skills), "check"],
                cwd=REPO_ROOT,
                env=env,
                capture_output=True,
                text=True,
            )
            self.assertEqual(res_empty.returncode, 1, res_empty.stdout + res_empty.stderr)
            self.assertIn("[MISSING]", res_empty.stdout)

            # 2. Install into isolated temp dir must succeed (exit 0), then check must exit 0
            res_install = subprocess.run(
                ["./install.sh", "--target", str(target_skills)],
                cwd=REPO_ROOT,
                env=env,
                capture_output=True,
                text=True,
            )
            self.assertEqual(res_install.returncode, 0, res_install.stdout + res_install.stderr)

            res_clean = subprocess.run(
                ["./install.sh", "--target", str(target_skills), "check"],
                cwd=REPO_ROOT,
                env=env,
                capture_output=True,
                text=True,
            )
            self.assertEqual(res_clean.returncode, 0, res_clean.stdout + res_clean.stderr)
            self.assertIn("All active skills are present.", res_clean.stdout)

            # 3. Adding an obsolete legacy skill must cause check to exit 1
            obsolete_link = target_skills / "gitea-plan"
            obsolete_link.symlink_to(REPO_ROOT / "skills" / "gitea-plan")
            res_obs = subprocess.run(
                ["./install.sh", "--target", str(target_skills), "check"],
                cwd=REPO_ROOT,
                env=env,
                capture_output=True,
                text=True,
            )
            self.assertEqual(res_obs.returncode, 1, res_obs.stdout + res_obs.stderr)
            self.assertIn("[OBSOLETE PRESENT] gitea-plan", res_obs.stdout)

            # 4. Repo-scoped dangling symlink is pruned on install; unrelated dangling symlink is preserved
            repo_dangling = target_skills / "stale-repo-skill"
            repo_dangling.symlink_to(REPO_ROOT / "skills" / "nonexistent-deleted-skill")
            unrelated_dangling = target_skills / "external-skill"
            unrelated_dangling.symlink_to(Path("/tmp/nonexistent-unrelated-skill-target"))

            res_reinstall = subprocess.run(
                ["./install.sh", "--target", str(target_skills)],
                cwd=REPO_ROOT,
                env=env,
                capture_output=True,
                text=True,
            )
            self.assertEqual(res_reinstall.returncode, 0, res_reinstall.stdout + res_reinstall.stderr)
            self.assertFalse(obsolete_link.is_symlink(), "Obsolete skill symlink should be backed up and removed")
            self.assertFalse(repo_dangling.is_symlink(), "Repo-scoped dangling symlink should be pruned")
            self.assertTrue(unrelated_dangling.is_symlink(), "Unrelated external symlink must be preserved")

            # 5. Clean check passes again after reinstall
            res_post = subprocess.run(
                ["./install.sh", "--target", str(target_skills), "check"],
                cwd=REPO_ROOT,
                env=env,
                capture_output=True,
                text=True,
            )
            self.assertEqual(res_post.returncode, 0, res_post.stdout + res_post.stderr)

    def test_skill_inventory_and_skeletons(self):
        """Proves all 15 active skills meet line count (<= 80), em-dash, and path portability rules, and legacy skills are retired."""
        install_sh = (REPO_ROOT / "install.sh").read_text()

        # Verify ACTIVE_PORTABLE_SKILLS matches EXPECTED_SKILLS exactly
        active_match = re.search(r"ACTIVE_PORTABLE_SKILLS=\(([^)]*)\)", install_sh)
        self.assertIsNotNone(active_match, "ACTIVE_PORTABLE_SKILLS missing from install.sh")
        active_skills = active_match.group(1).split()
        self.assertEqual(active_skills, EXPECTED_SKILLS)

        # Verify all 4 retired legacy skills appear in OBSOLETE_SKILLS and are absent from skills/
        obsolete_match = re.search(r"OBSOLETE_SKILLS=\(([^)]*)\)", install_sh)
        self.assertIsNotNone(obsolete_match, "OBSOLETE_SKILLS missing from install.sh")
        obsolete_skills = obsolete_match.group(1).split()
        for retired in RETIRED_LEGACY_SKILLS:
            self.assertIn(retired, obsolete_skills, f"{retired} must be listed in OBSOLETE_SKILLS")
            self.assertFalse(
                (REPO_ROOT / "skills" / retired).exists(),
                f"Retired legacy skill directory still exists: skills/{retired}",
            )

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
