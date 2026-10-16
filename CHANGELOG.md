# Changelog

## Unreleased

### Fixed

- Heuristic generation no longer initializes the Anthropic client, so `--no-llm` works without provider credentials.
- Built-in HTML embeds the locked Plotly library and no longer downloads an unversioned CDN script.

### Documentation

- Define the complete supported heuristic/TLS profile and document governance, conduct and a one-year roadmap.

## [0.1.4] - 2026-10-14

### Changed

- Validate each public release candidate with bounded, network-isolated fuzz campaigns against its exact source revision.
- Require positive engine execution counts, instrumented production code and validated seed corpora; retain source-bound reports and diagnostic evidence.
- Run deterministic seed and configuration checks in ordinary CI without starting mutation campaigns on betas.

### Upgrade

Use the existing installation procedure, preserve local configuration and keep the previous accepted package for rollback. This maintenance release updates release validation and does not change the application configuration format. Deployment and applicable device or integration acceptance remain separate from publication.

### Security

RC publication rejects absent or invalid source-bound fuzz reports. The fuzz runner bounds corpus paths, file types and size. No application vulnerability or new target-device acceptance is claimed by these tooling changes.

## [0.1.3]

### Fixed

Load built-in profile templates from memory so Markdown and HTML rendering works when the installed Python package is read-only. Existing templates in a supplied template directory or the package's template directory retain priority; missing templates use the built-in defaults without writing files there.

### Upgrade

No profile data or output format migration is needed. Only the chosen output directory needs to be writable. Callers that supply a custom template directory should place their overrides there explicitly; the renderer no longer creates default template files in that directory.

### Security

Rendering no longer requires write access to installed application files. HTML autoescaping remains enabled for both built-in and custom templates. This release fixes an installation compatibility defect; no remotely exploitable vulnerability is claimed.

## [0.1.2]

### Changed

Document the public-repository scanner and JSON/HTML/Markdown profile generation interfaces, contributor tests, private security reports and OpenSSF evidence. Publish source-bound release notes alongside the existing build provenance.

### Upgrade

This change does not migrate profile data or change output formats. Use the documented locked dependency installation, restrict GitHub tokens to the intended public repository access, and review generated profiles before publication.

### Security

No application vulnerability is claimed fixed by this documentation update. Release publication now fails closed when the reviewed source is missing unambiguous upgrade and security notes.
