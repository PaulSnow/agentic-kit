"""Behavioral tests for kit/bin/subscription-usage (fork-specific; see KIT.md)."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path

SUBSCRIPTION_USAGE = Path(__file__).resolve().parents[1] / "bin" / "subscription-usage"
ORG_A = "aaaaaaaa-0000-0000-0000-000000000000"
ORG_B = "bbbbbbbb-0000-0000-0000-000000000000"

# Stands in for llm-usage: logs the token and cache directory it was given and
# answers like the real tool, refusing the token "revoked".
FAKE_LLM_USAGE = """\
import json, os, sys
token = os.environ.get("CLAUDE_CODE_OAUTH_TOKEN")
with open(os.environ["FAKE_CALL_LOG"], "a") as log:
    log.write(json.dumps({"token": token, "cache": os.environ.get("XDG_CACHE_HOME"),
                          "args": sys.argv[1:]}) + "\\n")
if token == "revoked":
    anthropic = {"ok": False, "error": "HTTP 401"}
else:
    anthropic = {"ok": True, "subscription": None, "windows": {"five_hour": {
        "label": "5-hour", "utilization": 12.0, "reset_seconds": 3700}}}
print(json.dumps({"anthropic": anthropic, "openai": {"ok": False}}))
sys.exit(1)
"""


def fake_program(tmp_path: Path) -> Path:
    program = tmp_path / "llm-usage"
    program.write_text(f"#!{sys.executable}\n{FAKE_LLM_USAGE}", encoding="utf-8")
    program.chmod(0o755)
    return program


def make_login(
    directory: Path, organization: str, token: str, *, expires_ms: int | None = None
) -> Path:
    directory.mkdir(parents=True)
    expires = (
        expires_ms if expires_ms is not None else int(time.time() * 1000) + 3_600_000
    )
    (directory / ".credentials.json").write_text(
        json.dumps(
            {
                "claudeAiOauth": {
                    "accessToken": token,
                    "expiresAt": expires,
                    "subscriptionType": "max",
                }
            }
        ),
        encoding="utf-8",
    )
    (directory / ".claude.json").write_text(
        json.dumps({"oauthAccount": {"organizationUuid": organization}}),
        encoding="utf-8",
    )
    return directory


def run(
    tmp_path: Path, subscriptions: list[dict], *arguments: str
) -> subprocess.CompletedProcess[str]:
    config = tmp_path / "subscriptions.json"
    config.write_text(json.dumps({"subscriptions": subscriptions}), encoding="utf-8")
    config.chmod(0o600)
    return invoke(tmp_path, config, *arguments)


def invoke(
    tmp_path: Path, config: Path, *arguments: str
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            str(SUBSCRIPTION_USAGE),
            "--config",
            str(config),
            "--llm-usage",
            str(fake_program(tmp_path)),
            "--cache-root",
            str(tmp_path / "cache"),
            *arguments,
        ],
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
        env=os.environ | {"FAKE_CALL_LOG": str(tmp_path / "calls.jsonl")},
    )


def calls(tmp_path: Path) -> list[dict]:
    log = tmp_path / "calls.jsonl"
    if not log.exists():
        return []
    return [json.loads(line) for line in log.read_text(encoding="utf-8").splitlines()]


def by_name(result: subprocess.CompletedProcess[str]) -> dict[str, dict]:
    return {r["name"]: r for r in json.loads(result.stdout)["subscriptions"]}


def test_reads_each_subscription_with_its_own_token_and_cache(tmp_path: Path) -> None:
    login = make_login(tmp_path / "claude-a", ORG_A, "token-a")
    token_file = tmp_path / "b.token"
    token_file.write_text("token-b\n", encoding="utf-8")
    token_file.chmod(0o600)

    result = run(
        tmp_path,
        [
            {"name": "a", "organization": ORG_A, "config_dir": str(login)},
            {"name": "b", "token_file": str(token_file)},
        ],
        "--json",
    )

    assert result.returncode == 0, result.stderr
    assert [(c["token"], c["cache"]) for c in calls(tmp_path)] == [
        ("token-a", str(tmp_path / "cache" / "a")),
        ("token-b", str(tmp_path / "cache" / "b")),
    ]
    reports = by_name(result)
    assert (
        reports["a"]["state"],
        reports["a"]["organization"],
        reports["a"]["plan"],
    ) == (
        "ok",
        ORG_A,
        "max",
    )
    assert (reports["b"]["state"], reports["b"]["organization"]) == ("ok", "unverified")
    assert reports["b"]["anthropic"]["windows"]["five_hour"]["utilization"] == 12.0


def test_other_subscription_logged_in_is_not_requested(tmp_path: Path) -> None:
    login = make_login(tmp_path / "claude", ORG_A, "token-a")

    result = run(
        tmp_path,
        [{"name": "b", "organization": ORG_B, "config_dir": str(login)}],
        "--json",
    )

    assert result.returncode == 1
    report = by_name(result)["b"]
    assert (report["state"], report["organization"]) == ("not-logged-in", ORG_B)
    assert "plan" not in report
    assert calls(tmp_path) == []


def test_expired_login_is_not_sent(tmp_path: Path) -> None:
    login = make_login(tmp_path / "claude", ORG_A, "token-a", expires_ms=1)

    result = run(tmp_path, [{"name": "a", "config_dir": str(login)}], "--json")

    assert result.returncode == 1
    assert by_name(result)["a"]["state"] == "expired"
    assert calls(tmp_path) == []


def test_refuses_token_file_readable_by_others(tmp_path: Path) -> None:
    token_file = tmp_path / "loose.token"
    token_file.write_text("token-x", encoding="utf-8")
    token_file.chmod(0o644)

    result = run(tmp_path, [{"name": "x", "token_file": str(token_file)}], "--json")

    assert result.returncode == 1
    assert "chmod 600" in by_name(result)["x"]["error"]
    assert calls(tmp_path) == []


def test_token_command_and_refused_reading(tmp_path: Path) -> None:
    result = run(
        tmp_path,
        [
            {"name": "good", "token_command": ["echo", "token-c"]},
            {"name": "revoked", "token_command": ["echo", "revoked"]},
            {"name": "broken", "token_command": ["false"]},
        ],
        "--json",
    )

    assert result.returncode == 1
    reports = by_name(result)
    assert reports["good"]["state"] == "ok"
    assert (reports["revoked"]["state"], reports["revoked"]["error"]) == (
        "error",
        "llm-usage: HTTP 401",
    )
    assert reports["broken"]["state"] == "error"
    assert [c["token"] for c in calls(tmp_path)] == ["token-c", "revoked"]


def test_text_report_shows_windows_and_state(tmp_path: Path) -> None:
    login = make_login(tmp_path / "claude", ORG_A, "token-a")

    result = run(
        tmp_path,
        [
            {"name": "a", "organization": ORG_A, "config_dir": str(login)},
            {"name": "b", "organization": ORG_B, "config_dir": str(login)},
        ],
        "--fresh",
    )

    assert result.returncode == 1
    assert result.stdout.splitlines() == [
        f"a  (aaaaaaaa, max, login {login})",
        "  5-hour              12%  resets in 1h 1m",
        f"b  (bbbbbbbb, plan unknown, login {login})",
        "  not-logged-in: aaaaaaaa is logged in there",
    ]
    assert calls(tmp_path)[0]["args"] == ["--json", "--fresh"]


def test_rejects_bad_configuration(tmp_path: Path) -> None:
    two_sources = run(tmp_path, [{"name": "a", "config_dir": "x", "token_file": "y"}])
    unknown = run(tmp_path, [{"name": "a", "token_file": "y"}], "--only", "zzz")

    assert two_sources.returncode == 2
    assert "exactly one of" in two_sources.stderr
    assert unknown.returncode == 2
    assert calls(tmp_path) == []


def test_refuses_config_writable_by_others(tmp_path: Path) -> None:
    config = tmp_path / "subscriptions.json"
    config.write_text(
        json.dumps({"subscriptions": [{"name": "x", "token_command": ["echo", "t"]}]}),
        encoding="utf-8",
    )
    for mode in (0o620, 0o602):
        config.chmod(mode)

        result = invoke(tmp_path, config)

        assert result.returncode == 2
        assert "writable by others" in result.stderr
    assert calls(tmp_path) == []


def test_rejects_subscription_names_outside_the_safe_set(tmp_path: Path) -> None:
    for name in ("../up", "a b", ".", "", "ok/no"):
        result = run(tmp_path, [{"name": name, "token_command": ["echo", "t"]}])

        assert result.returncode == 2, name
        assert "A-Za-z0-9_-" in result.stderr, name
    assert calls(tmp_path) == []


def test_malformed_identity_file_reports_unreadable(tmp_path: Path) -> None:
    login = make_login(tmp_path / "claude", ORG_A, "token-a")
    (login / ".claude.json").write_text("{not json", encoding="utf-8")
    other = make_login(tmp_path / "claude-list", ORG_A, "token-b")
    (other / ".claude.json").write_text("[]", encoding="utf-8")

    result = run(
        tmp_path,
        [
            {"name": "a", "organization": ORG_A, "config_dir": str(login)},
            {"name": "b", "config_dir": str(other)},
        ],
        "--json",
    )

    assert result.returncode == 1
    reports = by_name(result)
    assert reports["a"]["state"] == "unreadable"
    assert ".claude.json" in reports["a"]["error"]
    assert reports["b"]["state"] == "unreadable"
    assert calls(tmp_path) == []
