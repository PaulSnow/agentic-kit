---
slug: hissing-mule
title: Approve the prepared GitHub Pages publication permissions
status: pending
category: access
urgency: medium
blocks:
  - Publish the Starter manual and verify its live README link
filed: 2026-10-16
needed_at: now
source: docs
refs:
  - manual/github-pages.yml
  - documentation.toml
---

# Approve the prepared publication boundary

The manual and local tooling are implemented. The prepared [Pages workflow](../manual/github-pages.yml) remains inert outside `.github/workflows/`. The repository is public, its default branch is `master`, and its default workflow-token permission is read-only. The Pages configuration query returned HTTP 404; this is not evidence of a configured site or completed publication.

The exact requested authorization is to install that workflow as `.github/workflows/docs-pages.yml`, configure this repository's Pages source as GitHub Actions, establish its `github-pages` deployment environment for the configured `master` release branch, and grant only the deployment job `pages: write` and `id-token: write`. The build retains `contents: read`; the repository's default workflow permission remains read-only. No long-lived credential, other repository grant, Tailnet route, listener exposure, Funnel, ACL or HTTPS change is requested.

After approval, the agent can deliver the workflow through the normal gates, manually publish the latest validated pushed candidate, wait for the matching run, and verify the live site at the URL in `documentation.toml`. Only `.kickoff/manual` is uploaded. Continuous deployment stays off; enabling it requires a separate explicit `docs deploy continuous on` request. Manual publishing remains available with the switch off.

The live-site checks include deep pages, anchors, search, 404/assets and private-path exclusions. The README receives a live link only after those checks succeed. The prepared Linux workflow has not run; the standing Linux lane passed the five behavior proofs but lacks Cargo, so renderer provisioning there remains unverified.

Close this action only when the operator supplies the scoped permission decision. Do not infer approval from a general publication request or a presentation acknowledgment.
