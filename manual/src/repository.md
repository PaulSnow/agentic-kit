# Repository Map

| Surface | Owns |
|---|---|
| `CLAUDE.md`, with `AGENTS.md` pointing to it | Agent instructions, hard rules, project context, and authority catalogs. |
| `briefs/` | Intent, design rationale, research, and methodology explanations. |
| `policies/` | Binding rules. Policies override implementation and plans. |
| `docs/` | Third-party reference text, pinned with source, version/date, retrieval date and redistribution basis. |
| `manual/` | The curated first-party user manual and its mdBook configuration/theme. |
| `documentation.toml` | Pinned documentation tools, local preview port, publication repository and release branch. |
| `plan/INDEX.md` | The only phase-status ledger. |
| `plan/` phase files | Dependencies, scope, executable acceptance and user demos. |
| `project/` | The isolated example deliverable, runtime pin, manifest, lockfile and tests. |
| `lib/agentic_starter/` | Shared deterministic methodology machinery. |
| `bin/` | Setup, checks, evidence and other deterministic commands. |
| `.claude/skills/`, `.claude/agents/` | Canonical procedures and role definitions. |
| `.agents/skills/`, `.codex/agents/` | Thin harness discovery mirrors. |
| `tests/` | Independent proofs and recipient-local proof governance. |
| `LOG.md` | Append-only activity history. |
| `user-actions/`, `lessons/` | Open human-only actions and provisional learning, with separate archive directories. |
| `.kickoff/` | Ignored runtime state, full-gate receipts, documentation tools and build output. |

Briefs explain decisions; policies prescribe behavior; plans refine the work. Pinned sources supply external authority. The manual is a reader-facing guide to the current system and does not replace those authorities.

## Preserve the boundary

The example deliverable does not reach into the parent repository. Its own source, tests, dependency metadata and runtime form an isolated package. The methodology machinery lives outside that package.

The public site is built only from the manual's curated chapters and declared theme. Logs, evidence, internal planning queues, host configuration and third-party reference archives are outside its publication input.
