# agentic-kit

Paul Snow's fork of Wolf McNally's [Agentic Coding Starter Kit](https://github.com/wolfmcnally/agentic-coding-starter)
(MIT). Wolf's tree is kept intact so that his daily changes merge cleanly. What this fork adds is the selection
below, [`kit/manifest.txt`](kit/manifest.txt), and [`bin/kit-install`](bin/kit-install), which copies the
selection into another repository. Wolf's [README](README.md) describes the full kit.

## Adopted

| Piece | Why |
|---|---|
| [`policies/docs.md`](policies/docs.md) | Third-party documents a project relies on are saved verbatim with their source and date. Drafts expire and pages change, so a decision should be re-readable against what was actually cited |
| [`policies/lessons.md`](policies/lessons.md) and [`rule-one`](.claude/skills/rule-one/SKILL.md) | Failures and corrections become lessons in a ledger inside the repo, readable by every session, machine and build driver, not only by one machine's Claude memory |
| [`policies/verification-discipline.md`](policies/verification-discipline.md) | Every review states what it inspected and what it could not see; an empty search is not "none found" |
| [`policies/mechanistic-vs-intelligence.md`](policies/mechanistic-vs-intelligence.md) | Deterministic scripts for repeatable work, models for judgment |
| [`policies/simplicity-and-consolidation.md`](policies/simplicity-and-consolidation.md) | Least structure for the uses you can name; one home for each piece of knowledge |
| [`plain`](.claude/skills/plain/SKILL.md) | Reports to the operator lead with the consequence |
| [`plan-reviewer`](.claude/agents/plan-reviewer.md) and [`code-critic`](.claude/agents/code-critic.md) | Independent review of a plan and of code, used in advisory mode with the same provider (Fable reviewing Opus) |

## Not adopted

- **`kickoff` and its evidence custody** (receipts, close gates, line ceilings). It is built for unattended product
  phases and is heavier than our projects need. We keep its outline: phase file, plan review, code critique, one
  gate at the end.
- **Cross-provider (Codex) review lanes and `roles`.** We use Claude only.
- **`stamp`, the mdBook manual, `treatise`, `teach` and `learn`.** Our projects already have their own specs and
  front pages. `learn` and `teach` remain usable from this checkout.

## Tools from Wolf used alongside

Installed separately, never vendored:

- [Drawbridge](https://github.com/wolfmcnally/drawbridge) (MIT) converts any file into a Markdown mirror with a provenance
  header.
- [Vellric](https://github.com/wolfmcnally/vellric) is its PDF engine. It is AGPL-3.0-only, so run it only as a
  separate CLI and never link it into project code.
- [Quillric](https://github.com/wolfmcnally/quillric) (MIT) turns a recording into a diarized transcript. It is paid
  per hour through ElevenLabs.
- [llm-usage](https://github.com/wolfmcnally/llm-usage) (MIT) shows Claude plan usage against pace. Clone it and link
  `llm-usage` onto `PATH`; `subscription-usage` runs it.

## Installing into a repository

```bash
./bin/kit-install --dry-run ~/repos/github.com/PaulSnow/<repo>   # what would be copied, and which references dangle
./bin/kit-install ~/repos/github.com/PaulSnow/<repo>
```

Files land at the same repo-relative paths. The target's `.kit-version` records the upstream commit they came
from. The adopted files refer to parts of the starter that were not adopted, by Markdown link or by a path in prose,
and the installer lists those references.
The adopting repository rewrites or drops them; it does not pull in the rest of the kit to satisfy them. A target
file that already differs is not overwritten without `--force`.

## Following upstream

```bash
git fetch upstream && git merge upstream/master     # Wolf's tree is unmodified, so this merges cleanly
git diff <old>..upstream/master -- $(grep -v '^#' kit/manifest.txt)   # what changed in the adopted pieces
```

After a merge that changes an adopted piece, re-run `kit-install` into each adopting repository and review its diff
there.

## Token usage

```bash
./kit/bin/token-report --repo ~/repos/github.com/PaulSnow/<repo> --by role --since 2026-10-20
```

[`kit/bin/token-report`](kit/bin/token-report) totals the tokens Claude Code spent on a repository, read from its
session transcripts under `~/.claude/projects/`, including subagents. Each model reply is counted once. Columns
separate fresh input, cache writes, cache reads and output (thinking shown as its share of output), because they are
priced differently. `--by session|role|account|model` groups the rows; a subagent's role is its agent type, so the
cost of `code-critic` or `plan-reviewer` shows separately. Each reply is credited to the subscription logged in when it
was made: Claude Code records the organization id when a session starts and whenever the login changes. Replies from
before Claude Code recorded it show as `unknown`. `--since`/`--until` bound a window and `--json` gives the rows to a
script. Wolf's execution telemetry records time and review findings but not tokens, and `llm-usage` shows plan usage
against pace, not the cost of one task; this fills that gap.

## Subscription limits

```bash
./kit/bin/subscription-usage
```

[`kit/bin/subscription-usage`](kit/bin/subscription-usage) shows each Claude subscription's plan windows (5-hour,
7-day, per-model) by running `llm-usage` once per subscription. `llm-usage` reads one credential per run and caches per
provider, not per account, so each run gets that subscription's token and its own cache directory. The subscriptions
are listed in `~/.config/agentic-kit/subscriptions.json`, which `token-report` also reads to name them. The file says
where each token is, never the token:

```json
{"subscriptions": [
  {"name": "personal", "organization": "<uuid>", "config_dir": "~/.claude"},
  {"name": "work", "organization": "<uuid>", "token_command": ["secret-tool", "lookup", "service", "claude-work"]}
]}
```

A `config_dir` entry reads that Claude Code login, and reports `not-logged-in` without a request when a different
subscription is logged in there. Two subscriptions that take turns in `~/.claude` can therefore only be read one at a
time. To read both at once, give the second its own login (`CLAUDE_CONFIG_DIR=~/.claude-work claude`) or a
long-lived token from `claude setup-token`, kept in the keyring (`token_command`) or a mode-600 file (`token_file`).
A token from a command or file cannot be matched to an organization, so its entry says `unverified`. Wolf's kickoff
still checks one Claude account; subscriptions are not routed per role.

## Supervising sessions

[`kit/agentd`](kit/agentd/README.md) is a Go supervisor for unattended Claude Code sessions in tmux: an append-only
event log, a session state machine driven by evidence (tmux screen, `STATUS.md`, transcript, process), and the
supervisor's policies as configuration: restart with backoff and a crash-loop breaker, bounded nudging that leaves a
session blocked on the owner alone, usage-limit waiting, the folder-trust prompt, delivery as a merge or pull request
through one allow-listed forge client, and escalation posted once per key. `agentd run --shadow` logs what it would
do without acting; `agentd status` prints the state table from the log. The owner's sessions and repositories live
outside the repository in `~/.config/agentic-kit/agentd.json`; [`agentd.example.json`](kit/agentd/agentd.example.json)
shows the shape.

```bash
cd kit/agentd && go test -race ./...
```

## Testing the kit

```bash
./bin/test kit/tests
```

The kit's tests live in `kit/tests/`, outside Wolf's governed proof estate, so they add nothing to his ledgers and
`./bin/check all` does not run them. Run them after every upstream merge. `kit/tests/references.txt` is the reviewed
list of references that do not resolve in a fresh target; a merge that adds or drops one fails the test until the
list is reviewed and updated.
