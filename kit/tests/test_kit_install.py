"""Behavioral tests for bin/kit-install (fork-specific; see KIT.md)."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
KIT_INSTALL = ROOT / "bin" / "kit-install"
REFERENCES = Path(__file__).with_name("references.txt")


def git(root: Path, *arguments: str) -> str:
    return subprocess.run(
        ["git", "-C", str(root), *arguments],
        capture_output=True,
        text=True,
        check=True,
    ).stdout


def init_repo(root: Path) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    git(root, "init", "-q")
    git(root, "config", "user.email", "fixture@example.invalid")
    git(root, "config", "user.name", "Fixture")
    return root


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def make_kit(tmp_path: Path, manifest: str) -> Path:
    """Build a committed fake kit checkout whose ROOT is its own directory."""
    kit = init_repo(tmp_path / "kit")
    (kit / "bin").mkdir()
    shutil.copy2(KIT_INSTALL, kit / "bin" / "kit-install")
    write(kit / "kit" / "manifest.txt", manifest)
    write(
        kit / "policies" / "adopted.md",
        "See [left](left.md), [kept](kept.md), [web](https://example.invalid/x) "
        "and `bin/tool` and policies/left.md.\n",
    )
    write(kit / "policies" / "kept.md", "kept\n")
    write(kit / "policies" / "left.md", "not adopted\n")
    write(kit / "bin" / "tool", "#!/bin/sh\n")
    write(kit / ".claude" / "skills" / "s" / "SKILL.md", "skill\n")
    write(kit / ".claude" / "skills" / "s" / "notes" / "extra.md", "extra\n")
    git(kit, "add", ".")
    git(kit, "commit", "-qm", "fixture")
    return kit


MANIFEST = "# comment\n\npolicies/adopted.md\npolicies/kept.md\n.claude/skills/s\n"


def run(kit_root: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [str(kit_root / "bin" / "kit-install"), *arguments],
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )


def test_installs_manifest_paths_verbatim_and_records_commit(tmp_path: Path) -> None:
    kit = make_kit(tmp_path, MANIFEST)
    target = init_repo(tmp_path / "target")

    result = run(kit, str(target))

    assert result.returncode == 0, result.stderr
    for rel in (
        "policies/adopted.md",
        "policies/kept.md",
        ".claude/skills/s/SKILL.md",
        ".claude/skills/s/notes/extra.md",
    ):
        assert (target / rel).read_bytes() == (kit / rel).read_bytes()
    assert not (target / "policies" / "left.md").exists()
    head = git(kit, "log", "-1", "--format=%H %cs").strip()
    assert (target / ".kit-version").read_text(
        encoding="utf-8"
    ) == f"agentic-kit {head}\n"


def test_reports_unresolved_links_and_prose_paths(tmp_path: Path) -> None:
    kit = make_kit(tmp_path, MANIFEST)
    target = init_repo(tmp_path / "target")

    result = run(kit, "--dry-run", str(target))

    assert result.returncode == 0, result.stderr
    lines = [line.strip() for line in result.stdout.splitlines() if " -> " in line]
    assert lines == [
        "policies/adopted.md -> bin/tool",
        "policies/adopted.md -> left.md",
        "policies/adopted.md -> policies/left.md",
    ]


def test_reference_resolves_once_target_has_it(tmp_path: Path) -> None:
    kit = make_kit(tmp_path, MANIFEST)
    target = init_repo(tmp_path / "target")
    write(target / "policies" / "left.md", "the target's own\n")
    write(target / "bin" / "tool", "#!/bin/sh\n")

    result = run(kit, "--dry-run", str(target))

    assert result.returncode == 0, result.stderr
    assert " -> " not in result.stdout


def test_dry_run_writes_nothing(tmp_path: Path) -> None:
    kit = make_kit(tmp_path, MANIFEST)
    target = init_repo(tmp_path / "target")
    before = sorted(
        p.relative_to(target) for p in target.rglob("*") if ".git" not in p.parts
    )

    result = run(kit, "--dry-run", str(target))

    assert result.returncode == 0, result.stderr
    assert "would install policies/adopted.md" in result.stdout
    after = sorted(
        p.relative_to(target) for p in target.rglob("*") if ".git" not in p.parts
    )
    assert after == before


def test_refuses_differing_file_unless_forced(tmp_path: Path) -> None:
    kit = make_kit(tmp_path, MANIFEST)
    target = init_repo(tmp_path / "target")
    write(target / "policies" / "kept.md", "local edit\n")
    write(
        target / "policies" / "adopted.md",
        (kit / "policies" / "adopted.md").read_text(),
    )

    refused = run(kit, str(target))

    assert refused.returncode == 1
    assert "policies/kept.md" in refused.stderr
    assert "policies/adopted.md" not in refused.stderr
    assert (target / "policies" / "kept.md").read_text() == "local edit\n"
    assert not (target / ".kit-version").exists()

    forced = run(kit, "--force", str(target))

    assert forced.returncode == 0, forced.stderr
    assert (target / "policies" / "kept.md").read_text() == "kept\n"


def test_refuses_target_that_is_not_a_repository(tmp_path: Path) -> None:
    kit = make_kit(tmp_path, MANIFEST)
    plain = tmp_path / "plain"
    plain.mkdir()

    result = run(kit, str(plain))

    assert result.returncode == 2
    assert "not a git repository" in result.stderr
    assert list(plain.iterdir()) == []


def test_fails_on_manifest_path_that_does_not_exist(tmp_path: Path) -> None:
    kit = make_kit(tmp_path, MANIFEST + "policies/absent.md\n")
    target = init_repo(tmp_path / "target")

    result = run(kit, str(target))

    assert result.returncode != 0
    assert "policies/absent.md" in result.stderr
    assert not (target / "policies").exists()


def test_real_manifest_references_match_reviewed_list(tmp_path: Path) -> None:
    """An upstream merge that adds or drops a cross-reference fails here until reviewed."""
    target = init_repo(tmp_path / "target")

    result = run(ROOT, "--dry-run", str(target))

    assert result.returncode == 0, result.stderr
    lines = [line.strip() for line in result.stdout.splitlines() if " -> " in line]
    assert lines == REFERENCES.read_text(encoding="utf-8").splitlines()
