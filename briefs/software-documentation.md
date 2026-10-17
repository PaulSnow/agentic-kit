---
title: Reader-Centered Software Documentation
date: 2026-10-16
status: methodology
scope: Markdown/mdBook manual baseline, reader needs, tested tool pins and publication boundary.
---

# Reader-Centered Software Documentation

Markdown source beside the software and a reproducible mdBook build give the project a reviewable user manual. The manual explains current behavior and operation. Repository history, planning, evidence and private configuration remain separate.

## Reader needs and maintained source

Diátaxis identifies tutorials, how-to guides, reference and explanation as distinct reader needs. Use those needs to choose a page's purpose; do not force every small manual into four mostly empty directories. Source: [Diátaxis start here](https://diataxis.fr/start-here/), As of 2026-10-16 (living-page observation; no publication date), Retrieved 2026-10-16. The upstream source repository declares CC BY-SA 4.0; this brief records the design principle in original wording and pins only the short four-kind enumeration as reference.

Write the Docs describes documentation as code through shared plain-text source, version control, review and automated tests. Updating docs alongside behavior avoids a second, detached delivery process. Source: [Docs as Code](https://www.writethedocs.org/guide/docs-as-code/), As of 2026-10-16 (living-page observation; no publication date), Retrieved 2026-10-16. The source repository's license is CC BY-NC-SA 4.0; only a minimal tool-category quotation is pinned; the guide is not mirrored because a general-purpose software template must not assume every redistribution is noncommercial.

W3C WAI recommends meaningful titles/headings/link text, useful image alternatives, and clear concise content. These are editorial acceptance criteria as well as inputs to mechanical checks. Source: [Writing for Web Accessibility](https://www.w3.org/WAI/tips/writing/), As of 2024-07-16 (the page’s minor-update date), Retrieved 2026-10-16. This brief paraphrases the principles; the local reference pin quotes three short headings.

## Renderer and sidebar choice

Use mdBook 0.4.50 with mdbook-admonish 1.19.0 and the plugin's generated CSS assets version 3.0.3. The local build and generated links/assets/anchors/search/print checks passed with this pair on 2026-10-16. The plugin reports that it was compiled against mdBook 0.4.40; its declared 0.4.x dependency is compatible with the selected renderer, and the observed warning is retained rather than hidden. A renderer or plugin repin renews the build and browser checks together.

Current official mdBook documentation advertises 0.5.4, while the selected plugin targets the 0.4 API. Retain the tested pair rather than assuming the newest renderer is compatible. Use exact Cargo versions and `--locked`; install missing binaries into repository-local ignored storage. Pin the installation compiler separately so builds do not follow a floating Rust channel. Do not change global installations.

The [versioned general configuration](../docs/mdbook-0.4.50/general.md) explains `build.create-missing=false`. The [CI excerpt](../docs/mdbook-0.4.50/ci-excerpt.md) limits mdBook's example testing claim to Rust and explains locked dependencies. The [playground excerpt](../docs/mdbook-0.4.50/playground-excerpt.md) supports disabling external Rust execution by default. The [serve excerpt](../docs/mdbook-0.4.50/serve-excerpt.md) records loopback/open options. The [admonish reproducible-build guidance](../docs/mdbook-admonish-1.19.0/reproducible-builds.md) binds plugin version and generated CSS.

Admonish supplies short titled sidebars for warnings, examples and brief reasons without breaking the reader's task flow. Its use here requires only the standard plugin and CSS; domain-specific preprocessors, analytics, graph extensions and externally hosted assets are unnecessary. The baseline keeps snake_case chapter filenames, title-case summary labels, two-space nested summary indentation, and one physical line per prose paragraph.

## First-party and third-party homes

Keep the first-party book under `manual/` and preserve `docs/` as externally authored reference pins. Preserve existing source documents and their links. The manual curates the current methodology and links to source authority; it does not concatenate the activity log or publish internal records. Derived projects replace the manual with their product's instructions and retain a brief acknowledgment/link to Starter.

## Publication and verification

GitHub custom Pages workflows require a deployment job with Pages-write and OIDC-token permissions and a Pages environment. Source: [Using custom workflows with GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages), As of 2026-10-16 (living-page observation), Retrieved 2026-10-16. The generic workflow template remains outside the executable workflow directory; each repository requires exact operator approval before installation and hosting configuration. Starter's scoped installation was approved on 2026-10-17, with a master-only deployment environment and continuous deployment off. Ordinary documentation editing and local preview require none of those grants.

Manual deployment and continuous deployment are independent controls. A manual dispatch publishes the latest validated, pushed release candidate. An explicit switch enables or disables push deployment on the configured release branch, with `master` as the default. Neither a dispatch receipt nor a successful build proves the public site works; deployment completion, live resources, search interaction, navigation, exclusions and the README URL require their own evidence.
