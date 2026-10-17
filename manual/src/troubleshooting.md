# Resolve Problems

## Setup or runtime refuses

Read the complete diagnostic. Check the committed runtime pin, manifest, lockfile and real dependency probe together. A bad explicit runtime override is authoritative and must be corrected; adding a fallback would conceal the problem.

An agent sandbox may block an otherwise working host tool's cache, managed runtime or network access. Distinguish a permission refusal from a missing dependency. Use a supported authorized execution route; do not weaken the check or claim the dependency is broken from a failed sandbox probe alone.

## A documentation tool version differs

Run `./bin/docs setup`. It uses exact installed versions when available and otherwise installs the selected version locally. It does not upgrade other projects' global tools. Re-pin the renderer, plugin and generated plugin CSS together when deliberately changing versions, then rerun the manual's checks.

## A chapter or link is missing

Read the named page and destination. Add the intended chapter to `SUMMARY.md`, or correct the link or anchor. The build does not silently create an empty page. The generated-output check includes print and search, where omitted or private text can otherwise survive unnoticed.

## A gate fails

The phase remains open. Diagnose the earliest meaningful divergence, correct the cause, and renew evidence bound to the changed candidate. A hook refusal caused by a safe defect in the agent's own work is work to finish. An unresolved refusal parks delivery. Never disable the hook or retry unchanged input.

## Another session changed the checkout

Treat unexpected paths as shared work. Stage only attributable paths. If a shared file's hunks cannot be assigned safely, park delivery. A pathspec on `git commit` uses working-tree content and can defeat a staged hunk partition; commit a partitioned index without a pathspec.

## Pages is unavailable

A missing workflow or permission is a publication boundary, not evidence of successful deployment. Finish the local manual and prepare the exact requested change for approval. Keep continuous deployment off unless the operator enables it. Manual publication remains independent of that switch.

## Human review is pending

Say exactly which criteria remain. A passing build is evidence of the automated checks, not a substitute for the operator's demo, visual judgment, or custody decision. Use `demo` for a visible step-by-step review and `ask` when the operator wants open decisions collected together.
