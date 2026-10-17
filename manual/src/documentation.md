# Write and Publish Documentation

Write manuals in Markdown and build them with the versions in `documentation.toml`. Keep the documentation alongside the behavior it describes and update both in the same change.

## Choose the reader's task

Use tutorials for guided learning, how-to guides for a concrete task, reference for exact facts, and explanation for understanding. Give each page a primary reader need. A short reason can sit in an admonition; longer reasoning belongs on an explanation page.

Use descriptive headings, meaningful link text, and text alternatives for informative images. Keep commands copyable and provide one command per shell fence. Test executable examples through the project's native runner; `mdbook test` tests Rust snippets only.

## Edit the manual

Add a snake_case Markdown chapter under `manual/src/`, then list it in `SUMMARY.md` with a title-case label. Use two spaces to indent nested summary entries. Each prose paragraph stays on one physical line. Missing chapters fail the build instead of being created automatically.

The source boundary accepts only summary-listed chapters, `SUMMARY.md`, an optional `404.md`, and assets explicitly listed in `book.assets` in `documentation.toml`. Review each declared asset for public use; JavaScript and JSON source assets are not admitted. Raw include directives, scripts, iframes, symlinks, and unlisted source files refuse before preprocessing. These restrictions prevent the manual from importing an operational file accidentally.

Build and check:

```sh
./bin/docs build
```

Open the built book without leaving a server running:

```sh
./bin/docs
```

For HTTP review, use the foreground loopback preview:

```sh
./bin/docs serve
```

The preview serves only the checked output. It does not create network routes. For an existing approved Tailnet proxy, pass its URL with `serve --url`; the listener remains on loopback. Stop the foreground command when review is complete. A browser-open acknowledgment proves only that the browser accepted the request; inspect the rendered result separately.

## Prepare GitHub Pages

Starter installs its approved workflow at `.github/workflows/docs-pages.yml`, with read-only default permissions and Pages-write/OIDC-token permissions confined to the deployment job. Its `github-pages` environment allows only `master`. Continuous deployment stays off unless explicitly enabled. The generic recipient template remains at `manual/github-pages.yml`; installing it in another repository requires that owner's explicit approval of the permissions, publishing source and deployment environment. The command refuses until an approved workflow is installed. It never enables Pages or grants permissions itself.

The workflow uploads only fresh, validated book output. Continuous deployment defaults off. Configure `deploy.repository`, `deploy.release_branch`, `deploy.workflow`, and `deploy.url` in `documentation.toml`, and the corresponding `site-url` prefix in `manual/book.toml`. `master` is the default release branch; a project may configure `main` or another existing branch. Branch selection does not rename a repository's branch.

## Deploy manually

Commit and push the documentation with the normal repository gates. Then invoke `docs deploy` through either harness, or run:

```sh
./bin/docs deploy
```

The command requires a clean checkout on the configured release branch, a matching GitHub origin, and a local commit equal to the branch's current remote commit. It validates locally and requests the installed workflow on that exact branch. A dispatch acknowledgment is not completed publication. Wait for the matching workflow run and inspect its terminal result before checking the site.

## Control continuous deployment

After approval and workflow installation, enable deployment on release-branch pushes:

```sh
./bin/docs deploy continuous on
```

Disable it:

```sh
./bin/docs deploy continuous off
```

These commands set `DOCS_RELEASE_BRANCH` and `DOCS_CONTINUOUS` repository variables. They require GitHub variable-write authority. The off setting preserves manual deployment. A failure or absent variable is never reported as enabled or disabled successfully.

## Verify publication

```sh
./bin/docs verify
```

Then inspect the live site in a browser: open a deep page, follow an anchor, search for a known term, navigate by keyboard, inspect the 404 page and assets, and check the README's actual live link. The HTTP probe checks excluded operational paths return 403 or 404. It cannot prove perceptual quality or search interaction.
