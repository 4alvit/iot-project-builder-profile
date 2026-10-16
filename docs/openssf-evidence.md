# OpenSSF Best Practices evidence

This is an evidence index for the OpenSSF Best Practices Passing self-assessment. It is not an assertion that a badge has been awarded or that every criterion is satisfied. The public badge service is the authority for an awarded status.

## Project and participation

Generate engineering profiles from GitHub activity with optional language-model analysis and HTML/Markdown outputs.

The project is developed publicly in [Git](https://github.com/4alvit/iot-project-builder-profile) under the [MIT license](../LICENSE). Its source, issue tracker and pull requests are available without a paid account. [Contribution instructions](../CONTRIBUTING.md) describe reporting, changes, coding conventions, tests and review. The [security policy](../SECURITY.md) provides a confidential vulnerability-reporting path, support scope, response targets and deployment boundaries.

## User and interface documentation

- [`README.md`](../README.md)
- [`RELEASING.md`](../RELEASING.md)

## Source, testing and analysis

- [`iot_profile_builder`](../iot_profile_builder)

- [Test suite](../tests) and [CI workflows](../.github/workflows)
- [Local CI entry point](../scripts/ci.sh)
- [CodeQL analysis](../.github/workflows/codeql.yml)
- [Dependency update configuration](../.github/dependabot.yml)

The gate runs Ruff, formatting, mypy, test-readiness checks and the application test suite. Tests cover data processing, rendering and publication helpers. Use mocked GitHub/LLM responses; do not publish an output or contact a paid provider as part of a unit test.

CI results are evidence for the tested revision and environment, not proof of safe production or hardware operation. Check the current default-branch runs and unresolved security findings before answering the analysis criteria. Fuzzing, coverage completeness and independent penetration testing must be supported by actual runs; ordinary unit tests must not be presented as those activities.

## Changes and releases

Follow `RELEASING.md`. Release notes should identify output/schema changes, publication behavior and security fixes. Publishing a package or source release does not authorize publishing a user profile. The [release policy](../.release-policy.json) records automation behavior. A new release must identify its source revision and explain notable changes; security fixes must identify relevant advisories when known.

## Assessment evidence and limits

The maintainer confirmed secure-design/common-vulnerability knowledge and no outside GitHub bug, enhancement or vulnerability reports in the preceding 12 months. The public GitHub issue inventory and advisory inventory were empty on 16 October 2026. Private vulnerability reporting was verified enabled. These statements do not imply a third-party audit.

The current [quality evidence](quality.md), [complete supported profile](SUPPORTED_PROFILE.md), [governance](../GOVERNANCE.md), [conduct policy](../CODE_OF_CONDUCT.md) and [roadmap](../ROADMAP.md) describe source-specific scope and limitations. Follow actual current CI results and the official badge service for awarded status. The questionnaire must not infer all optional transport properties from an HTTPS URL.
