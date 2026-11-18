# Documentation

A generator that turns public repository evidence into a single dated IoT
engineering profile page, with its own release and quality records.

## The profile

- [IoT Engineering Profile: 4alvit](4alvit_profile.md) — the generated profile as published.
- [Profile experience template](profile-template.md) — the HTML, CSS and JavaScript every generated profile shares.
- [Supported heuristic and cryptographic profile](SUPPORTED_PROFILE.md) — what the complete heuristic mode scans and generates.
- [Profile refresh runbook](profile-refresh.md) — how a new dated analysis replaces the public page.
- [Profile preview](images/README.md) — the actual rendered image the README uses.

## Quality

- [Quality evidence and limitations](quality.md) — what the required gate runs and what the application suite exercises.
- [OpenSSF Best Practices evidence](openssf-evidence.md) — the evidence index behind the self-assessment.

## Release operation

- [CI and release operations](release-workflow.md) — `.release-policy.json` and the required status.
- [CI orchestration](CI-ORCHESTRATION.md) — how quality gate and release pipeline divide the events.
- [Project release packaging and versions](release-packaging.md) — the installable source tarball as the only payload.
- [Version plans and manifest synchronization](VERSIONING.md) — the versioning opt-in.
- [Release helper TLS profile](RELEASE_TLS_PROFILE.md) — the qualified `gh` transport profile.
- [TLS certificate key policy](tls-policy.md) — the verification applied to owned HTTPS clients.
- [Release-candidate fuzz testing](fuzzing.md) — the illustrated RC fuzzing process.
- [Fuzzing release candidates](rc-fuzzing.md) — the reusable bounded fuzz workflow.
- [Release read recovery and rerun validation](release-read-safety.md) — the two fixes carried from the shared toolkit.
- [Early final-build runner check](runner-preflight.md) — why the check runs before the final build.
