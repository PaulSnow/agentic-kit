# Use the Skills

Skills are repository procedures that a harness can discover and load. Canonical definitions live under `.claude/skills/`; `.agents/skills/` exposes directory symlinks for Codex. Invoke `/name` in Claude Code or `$name` in Codex.

| Skill | Use it when you want to… |
|---|---|
| `stamp` | Create a new project from this template. It is available only in Starter. |
| `methodology` | Scope a project, turn an idea into a brief, or organize a phased plan. |
| `kickoff` | Execute or resume one phase with its selected review contract and checks. |
| `demo` | Walk through an approved human demo one visible action at a time. |
| `docs` | Build and open the project's manual, preview it, or deploy through an approved Pages workflow. |
| `roles` | Inspect or change model and effort pins in `kickoff.yaml`. |
| `refactor` | Improve code structure while preserving observable behavior. |
| `mutate` | Survey whether the tests catch planted faults in disposable copies. It runs only on request. |
| `learn` | Assess practices in another repository for adoption here. |
| `teach` | Assess which practices here should move to another repository. |
| `sweep` | Review accumulated rules, skills, briefs, and lessons for maintenance. |
| `sweep-planning` | Analyze plan-review verdicts and propose improvements to the planning loop. |
| `sweep-coding` | Analyze code-review verdicts and propose improvements to the coding loop. |
| `treatise` | Produce a durable outward explanation from current repository evidence. |
| `ask` | Surface all open operator decisions in one interaction. Only the operator invokes it. |
| `plain` | Recompose a report so its consequence and required decision are clear. |
| `rule-one` | Diagnose a failure or correction and persist reusable learning at its proper authority. |

`learn`, `teach`, and the sweep skills present their judgments before applying the changes their approval contracts require. The agent normally applies `plain` and Rule One without a separate user command.

## Change role configuration

`roles` edits maintained model/effort pins while preserving unrelated configuration. It does not invoke a model. `kickoff` performs live preflight before product mutation and chooses an allowed review venue.

## Review documentation

In Claude Code:

```text
/docs
```

In Codex:

```text
$docs
```

The skill checks the local configuration, provisions only missing pinned documentation tools, builds the curated manual, validates its internal links and assets, and opens the result in a local browser. See [documentation publishing](documentation.md) for preview and deployment modes.
