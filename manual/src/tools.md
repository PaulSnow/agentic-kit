# Command Reference

Repository wrappers own runtime selection and checks. Run commands from the checkout; the core wrappers also resolve their own location when invoked elsewhere.

| Command | Result |
|---|---|
| `./bin/setup` | Provisions the pinned runtime and locked dependencies and probes the real tools. |
| `./bin/python` | Runs Python from the same environment used by the checks. |
| `./bin/test` | Runs the example and methodology tests. Additional arguments select focused tests. |
| `./bin/test --vital` | Runs the locally admitted fast proof families. |
| `./bin/test --changed-from REF` | Selects proof families affected by the diff, widening to full when uncertain. |
| `./bin/check all` | Runs lint, formatting verification, tests, and policy checks; captures a bound full-gate receipt. |
| `./bin/docs setup` | Uses exact installed documentation tools or installs them under ignored repository-local runtime storage. |
| `./bin/docs build` | Builds and validates the curated manual without opening a browser. |
| `./bin/docs check` | Runs the same publication-input, build, output and link checks. |
| `./bin/docs` | Builds and opens the local manual. |
| `./bin/docs serve` | Builds, opens, and serves a loopback-only foreground preview. Ctrl-C stops it. |
| `./bin/docs deploy` | Requests publication of the latest validated, clean, pushed release candidate through the approved workflow. |
| `./bin/docs deploy continuous on` | Enables push deployment for the configured release branch using repository variables. |
| `./bin/docs deploy continuous off` | Disables push deployment; manual deployment remains usable. |
| `./bin/docs verify` | Probes the configured HTTPS site, deep pages, assets, search and private-path exclusions. |
| `./bin/kickoff-config show` | Displays maintained orchestration settings. |
| `./bin/kickoff-tree-id` | Identifies the current candidate. |
| `./bin/test-governance validate` | Checks the local proof inventory and its evidence. |
| `./bin/lessons validate` | Validates the lessons ledger. |
| `./bin/lessons candidates` | Reports lessons ready for operator consideration. |
| `./bin/install-hooks` | Opts the checkout into the tracked Git hooks. |
| `./bin/check-hooks-installed` | Distinguishes not opted in from a broken hook installation. |

`bin/README.md` in the source repository is the complete deterministic-command catalog. Use a command's `--help` before selecting a less common operation.

## Runtime overrides

`TOOLCHAIN_PYTHON` is an authoritative absolute interpreter-path override for deliberate runtime testing. Invalid or failed overrides refuse; the wrapper does not silently switch to another interpreter. Normal use follows the committed managed runtime pin.

## Documentation pins

`documentation.toml` selects mdBook 0.4.50 and mdbook-admonish 1.19.0. Setup uses exact versions and Cargo's locked dependency graph. It leaves global tools unchanged. Missing Rust/Cargo is reported as a prerequisite rather than silently installing a global toolchain.
