# agentic-kit

Paul Snow's fork of Wolf McNally's [Agentic Coding Starter Kit](https://github.com/wolfmcnally/agentic-coding-starter) (MIT). This fork adds files and changes almost none of Wolf's, so his frequent changes merge cleanly. The one change to his tree is two lines in [`candidate-partition.yaml`](candidate-partition.yaml) that list `KIT.md` and `kit/**`, because his checks refuse files they cannot classify. Everything else this fork adds lives in this file and in `kit/`: the selection below, [`kit/manifest.txt`](kit/manifest.txt), and [`kit/bin/kit-install`](kit/bin/kit-install), which copies the selection into another repository. Wolf's [README](README.md) describes the full kit.

## Adopted

| Piece | Why |
|---|---|
| [`policies/docs.md`](policies/docs.md) | Third-party documents a project relies on are saved verbatim with their source and date. Drafts expire and pages change, so a decision should be re-readable against what was actually cited |
| **Rule One bundle:** [`rule-one`](.claude/skills/rule-one/SKILL.md) and its brief [`rule-one-diagnostic-learning`](briefs/rule-one-diagnostic-learning.md) | Failures and corrections are diagnosed before they are fixed, and what is learned is kept |
| **Self-improvement bundle:** [`policies/lessons.md`](policies/lessons.md), `bin/lessons`, `bin/check-catalogs`, their tests, [`sweep`](.claude/skills/sweep/SKILL.md), [`harness-self-improvement`](briefs/harness-self-improvement.md) and empty `lessons/` and `lessons-archived/` ledgers | Lessons live in a ledger inside the repo, readable by every session, machine and build driver, not only by one machine's Claude memory; `sweep` reviews them |
| [`policies/verification-discipline.md`](policies/verification-discipline.md) | Every review states what it inspected and what it could not see; an empty search is not "none found" |
| [`policies/mechanistic-vs-intelligence.md`](policies/mechanistic-vs-intelligence.md) | Deterministic scripts for repeatable work, models for judgment |
| [`policies/simplicity-and-consolidation.md`](policies/simplicity-and-consolidation.md) | Least structure for the uses you can name; one home for each piece of knowledge |
| [`plain`](.claude/skills/plain/SKILL.md) | Reports to the operator lead with the consequence |
| [`plan-reviewer`](.claude/agents/plan-reviewer.md) and [`code-critic`](.claude/agents/code-critic.md) | Independent review of a plan and of code, used in advisory mode with the same provider (Fable reviewing Opus) |

## Not adopted

- **`kickoff` and its evidence custody** (receipts, close gates, line ceilings). It is built for unattended product phases and is heavier than our projects need. We keep its outline: phase file, plan review, code critique, one gate at the end.
- **Cross-provider (Codex) review lanes and `roles`.** We use Claude only.
- **`stamp`, the mdBook manual, `treatise`, `teach` and `learn`.** Our projects already have their own specs and front pages. `learn` and `teach` remain usable from this checkout.

## Tools from Wolf used alongside

Installed separately, never vendored:

- [Drawbridge](https://github.com/wolfmcnally/drawbridge) (MIT) converts any file into a Markdown mirror with a provenance header.
- [Vellric](https://github.com/wolfmcnally/vellric) is its PDF engine. It is AGPL-3.0-only, so run it only as a separate CLI and never link it into project code.
- [Quillric](https://github.com/wolfmcnally/quillric) (MIT) turns a recording into a diarized transcript. It is paid per hour through ElevenLabs.
- [llm-usage](https://github.com/wolfmcnally/llm-usage) (MIT) shows Claude plan usage against pace. Clone it and link `llm-usage` onto `PATH`; `subscription-usage` runs it.

## Installing into a repository

```bash
./kit/bin/kit-install --dry-run <target-repo>   # what would be copied, and which references dangle
./kit/bin/kit-install <target-repo>
```

Wolf's `stamp` names some pieces as atomic bundles that must travel together, and the manifest lists every member of the two we adopt. `kit/tests/test_kit_install.py` checks this against `stamp`'s text in two ways. First, every tracked path `stamp` names in backticks, from the sentence that opens the Rule One or self-improvement bundle to the end of that paragraph, must be in the manifest; if either opening phrase disappears, the test fails and says so. Second, in every `stamp` paragraph that uses the word "atomic", any sentence that names a path the manifest installs must have every tracked path it names installed too. So an upstream change that adds a backticked member, or a new atomic sentence that touches an adopted piece, fails the kit check until the manifest follows. A member named without backticks, or one this checkout does not track, is not caught. Ledger folders are created empty, never with the template's own entries. The Codex mirrors under `.agents/` are left out of the manifest and of both checks, since this kit is Claude-only. `bin/lessons` and `bin/check-catalogs` run through `uv`.

Files land at the same repo-relative paths. The target's `.kit-version` records the upstream commit they came from: the merge base of this checkout's `HEAD` and `upstream/master`. In a checkout without `upstream/master` it records the checkout's own `HEAD` and says so. The adopted files refer to parts of the starter that were not adopted, by Markdown link or by a path in prose, and the installer lists those references. The adopting repository rewrites or drops them; it does not pull in the rest of the kit to satisfy them. A target file that already differs is not overwritten without `--force`.

After installing (not on `--dry-run`), the installer runs the target's `bin/lessons validate` and `bin/check-catalogs` and prints what they report; neither fails the install. `bin/check-catalogs` expects Wolf's `CLAUDE.md` zone markers and a `plan/INDEX.md`, and checks every Markdown link, so in a repository without those it reports errors. That is a known consequence of installing `stamp`'s self-improvement bundle whole: the checker travels with the bundle even where its catalogs do not exist. Those errors list what the adopting repository has to supply, rewrite or drop.

## Following upstream

```bash
git fetch upstream && git merge upstream/master     # only candidate-partition.yaml is shared, so this merges cleanly
git diff <old>..upstream/master -- $(grep -v '^#' kit/manifest.txt)   # what changed in the adopted pieces
```

After a merge that changes an adopted piece, re-run `kit-install` into each adopting repository and review its diff there.

## Token usage

```bash
./kit/bin/token-report --repo <repo-path> --by role --since 2026-10-20
```

[`kit/bin/token-report`](kit/bin/token-report) totals the tokens Claude Code spent on a repository, read from its session transcripts under `~/.claude/projects/`, including subagents. Each model reply is counted once. Columns separate fresh input, cache writes, cache reads and output (thinking shown as its share of output), because they are priced differently. `--by session|role|account|model` groups the rows; a subagent's role is its agent type, so the cost of `code-critic` or `plan-reviewer` shows separately. Each reply is credited to the subscription logged in when it was made: Claude Code records the organization id when a session starts and whenever the login changes. Replies from before Claude Code recorded it show as `unknown`. `--since`/`--until` bound a window and `--json` gives the rows to a script. Wolf's execution telemetry records time and review findings but not tokens, and `llm-usage` shows plan usage against pace, not the cost of one task; this fills that gap.

## Subscription limits

```bash
./kit/bin/subscription-usage
```

[`kit/bin/subscription-usage`](kit/bin/subscription-usage) shows each Claude subscription's plan windows (5-hour, 7-day, per-model) by running `llm-usage` once per subscription. `llm-usage` reads one credential per run and caches per provider, not per account, so each run gets that subscription's token and its own cache directory. The subscriptions are listed in `~/.config/agentic-kit/subscriptions.json`, which `token-report` also reads to name them. The file says where each token is, never the token:

```json
{"subscriptions": [
  {"name": "personal", "organization": "<uuid>", "config_dir": "~/.claude"},
  {"name": "work", "organization": "<uuid>", "token_command": ["secret-tool", "lookup", "service", "claude-work"]}
]}
```

A `config_dir` entry reads that Claude Code login, and reports `not-logged-in` without a request when a different subscription is logged in there. Two subscriptions that take turns in `~/.claude` can therefore only be read one at a time. To read both at once, give the second its own login (`CLAUDE_CONFIG_DIR=~/.claude-work claude`) or a long-lived token from `claude setup-token`, kept in the keyring (`token_command`) or a mode-600 file (`token_file`). A token from a command or file cannot be matched to an organization, so its entry says `unverified`. Wolf's kickoff still checks one Claude account; subscriptions are not routed per role.

## Supervising sessions

The Go supervisor for unattended Claude Code sessions, `agentd`, began here as `kit/agentd` and now lives in its own repository, [agentd-kit](https://github.com/PaulSnow/agentd-kit). It is a service for a whole machine that supervises sessions across many repositories, which does not fit a template that governs one repository.

## Testing the kit

```bash
./kit/bin/check
```

The kit's tests live in `kit/tests/`, outside Wolf's governed proof estate, so they add nothing to his ledgers and `./bin/check all` does not run them. `kit/bin/check` runs them; run it after `./bin/check all` and after every upstream merge. `kit/tests/references.txt` is the reviewed list of references that do not resolve in a fresh target; a merge that adds or drops one fails the test until the list is reviewed and updated.
