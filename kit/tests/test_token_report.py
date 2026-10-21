"""Behavioral tests for kit/bin/token-report (fork-specific; see KIT.md)."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

TOKEN_REPORT = Path(__file__).resolve().parents[1] / "bin" / "token-report"
REPO = Path("/work/repo")
SESSION = "11111111-1111-1111-1111-111111111111"


def reply(
    message_id: str,
    *,
    cwd: Path = REPO,
    session: str = SESSION,
    time: str = "2026-10-20T12:00:00Z",
    model: str = "claude-opus-5-5",
    tokens: tuple[int, int, int, int, int] = (1, 10, 100, 20, 5),
) -> dict:
    fresh, write, read, output, thinking = tokens
    return {
        "type": "assistant",
        "cwd": str(cwd),
        "sessionId": session,
        "timestamp": time,
        "requestId": f"req_{message_id}",
        "message": {
            "id": message_id,
            "model": model,
            "usage": {
                "input_tokens": fresh,
                "cache_creation_input_tokens": write,
                "cache_read_input_tokens": read,
                "output_tokens": output,
                "output_tokens_details": {"thinking_tokens": thinking},
            },
        },
    }


def write_lines(path: Path, records: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [json.dumps(r) for r in records] + [
        '{"type": "user", "message": {"content": "hi"}}'
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def project_dir(root: Path, repo: Path = REPO) -> Path:
    return root / str(repo).replace("/", "-")


def run(root: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            str(TOKEN_REPORT),
            "--projects-root",
            str(root),
            "--repo",
            str(REPO),
            "--subscriptions",
            str(root / "no-subscriptions.json"),
            "--json",
            *arguments,
        ],
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )


def report(root: Path, *arguments: str) -> dict:
    result = run(root, *arguments)
    assert result.returncode == 0, result.stderr
    return json.loads(result.stdout)


def test_counts_each_reply_once_across_repeated_lines(tmp_path: Path) -> None:
    one = reply("msg_1")
    write_lines(
        project_dir(tmp_path) / f"{SESSION}.jsonl", [one, one, one, reply("msg_2")]
    )

    data = report(tmp_path)

    assert data["total"] == {
        "input": 2,
        "cache_write": 20,
        "cache_read": 200,
        "output": 40,
        "thinking": 10,
        "replies": 2,
    }


def test_attributes_subagents_to_their_role(tmp_path: Path) -> None:
    project = project_dir(tmp_path)
    write_lines(project / f"{SESSION}.jsonl", [reply("msg_main")])
    agent = project / SESSION / "subagents" / "agent-a1.jsonl"
    write_lines(
        agent, [reply("msg_sub", model="claude-sonnet-5-5", tokens=(0, 0, 0, 7, 0))]
    )
    agent.with_suffix(".meta.json").write_text(
        '{"agentType": "code-critic"}', encoding="utf-8"
    )
    write_lines(project / SESSION / "subagents" / "agent-a2.jsonl", [reply("msg_bare")])

    data = report(tmp_path, "--by", "role")

    rows = {(r["role"], r["model"]): r["output"] for r in data["rows"]}
    assert {r["account"] for r in data["rows"]} == {"unknown"}
    assert rows == {
        ("code-critic", "claude-sonnet-5-5"): 7,
        ("main", "claude-opus-5-5"): 20,
        ("subagent", "claude-opus-5-5"): 20,
    }


def test_counts_only_sessions_inside_the_repo(tmp_path: Path) -> None:
    write_lines(
        project_dir(tmp_path) / f"{SESSION}.jsonl",
        [
            reply("msg_in"),
            reply("msg_sub", cwd=REPO / "lib"),
            reply("msg_out", cwd=Path("/work")),
        ],
    )
    sibling = Path("/work/repo-other")
    write_lines(
        project_dir(tmp_path, sibling) / "s.jsonl", [reply("msg_sibling", cwd=sibling)]
    )
    write_lines(
        project_dir(tmp_path) / "synthetic.jsonl",
        [reply("msg_syn", model="<synthetic>")],
    )

    data = report(tmp_path)

    assert data["total"]["replies"] == 2


def test_filters_by_time_window_and_session(tmp_path: Path) -> None:
    other = "22222222-2222-2222-2222-222222222222"
    write_lines(
        project_dir(tmp_path) / f"{SESSION}.jsonl",
        [
            reply("msg_early", time="2026-10-19T23:59:59Z"),
            reply("msg_in", time="2026-10-20T00:00:00Z"),
            reply("msg_late", time="2026-10-21T00:00:00Z"),
            reply("msg_other", session=other, time="2026-10-20T06:00:00Z"),
        ],
    )

    window = report(tmp_path, "--since", "2026-10-20", "--until", "2026-10-21")
    session = report(tmp_path, "--session", other)

    assert window["total"]["replies"] == 2
    assert [r["session"] for r in session["rows"]] == [other]


def test_text_table_ends_with_total(tmp_path: Path) -> None:
    write_lines(
        project_dir(tmp_path) / f"{SESSION}.jsonl",
        [reply("msg_1", tokens=(0, 0, 1234, 0, 0))],
    )

    result = subprocess.run(
        [
            str(TOKEN_REPORT),
            "--projects-root",
            str(tmp_path),
            "--repo",
            str(REPO),
            "--by",
            "model",
        ],
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    lines = result.stdout.splitlines()
    assert lines[0].split()[:4] == ["model", "input", "cache_write", "cache_read"]
    assert lines[-1].split()[:4] == ["total", "0", "0", "1,234"]


def test_rejects_malformed_time(tmp_path: Path) -> None:
    result = run(tmp_path, "--since", "yesterday")

    assert result.returncode == 2
    assert "bad time" in result.stderr


def login(organization: str, time: str, session: str = SESSION) -> dict:
    return {
        "type": "attachment",
        "cwd": str(REPO),
        "sessionId": session,
        "timestamp": time,
        "attachment": {"type": "credential_org", "organizationUuid": organization},
    }


def test_credits_each_reply_to_the_subscription_logged_in_then(tmp_path: Path) -> None:
    personal = "aaaaaaaa-0000-0000-0000-000000000000"
    work = "bbbbbbbb-1111-1111-1111-111111111111"
    project = project_dir(tmp_path)
    write_lines(
        project / f"{SESSION}.jsonl",
        [
            reply("msg_before", time="2026-10-20T09:00:00Z"),
            login(personal, "2026-10-20T10:00:00Z"),
            reply("msg_personal", time="2026-10-20T10:00:00Z"),
            login(work, "2026-10-20T11:00:00Z"),
            reply("msg_work", time="2026-10-20T11:30:00Z"),
        ],
    )
    write_lines(
        project / SESSION / "subagents" / "agent-a1.jsonl",
        [reply("msg_sub", time="2026-10-20T10:30:00Z", tokens=(0, 0, 0, 3, 0))],
    )
    names = tmp_path / "subscriptions.json"
    names.write_text(
        json.dumps({"subscriptions": [{"name": "work", "organization": work}]}),
        encoding="utf-8",
    )

    data = report(tmp_path, "--by", "account", "--subscriptions", str(names))

    rows = {r["account"]: (r["output"], r["replies"]) for r in data["rows"]}
    assert rows == {"aaaaaaaa": (23, 2), "work": (20, 1), "unknown": (20, 1)}
