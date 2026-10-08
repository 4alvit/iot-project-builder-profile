# Changelog

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
