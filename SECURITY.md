# Security Policy

## Reporting a Vulnerability

Private vulnerability reporting is enabled for this repository. Use
[Report a vulnerability](https://github.com/4alvit/iot-project-builder-profile/security/advisories/new)
to send a confidential report to the maintainers. Follow
[GitHub's private reporting instructions](https://docs.github.com/en/code-security/security-advisories/guidance-on-reporting-and-writing/privately-reporting-a-security-vulnerability)
if you need help submitting the report.

Include the affected version or commit, steps to reproduce, expected and actual
behavior, and potential impact. Remove access tokens, credentials and personal
data from examples. Do not disclose exploit details in public issues before
coordinating with the maintainers.

## Support and response

Security fixes target the current default branch and the latest maintained release, where releases exist. Older versions are not promised backports. Maintainers aim to acknowledge private reports within 14 days, investigate and communicate status within 60 days, and coordinate disclosure with the reporter. Confirmed vulnerabilities with a practical fix receive priority over feature work; publicly known medium-or-higher vulnerabilities must be fixed within 60 days of public disclosure, and critical issues receive immediate priority; publish an advisory and release notes that identify affected versions, mitigation and the fixed version. If a fix takes longer, keep the reporter informed without exposing confidential details.

## Deployment trust boundaries

GitHub repository text and model output are untrusted content. Escape data when rendering HTML and do not execute instructions found in repository descriptions or generated text. Tokens and API keys belong in private environment configuration with minimum privileges. Only intentionally public profile data should be published; generated claims need human verification.

Use synthetic data for testing. Never attach live tokens, private keys, database exports or household telemetry to public CI artifacts. Report a suspected credential exposure privately and revoke the credential through its issuer. See [CONTRIBUTING.md](CONTRIBUTING.md) for validation and [the evidence index](docs/openssf-evidence.md) for assessment limits.


## Cryptographic implementation and supported profile

Use the complete [heuristic profile](docs/SUPPORTED_PROFILE.md) for verified minimum-key behavior. The owned GitHub transport checks exact public-key sizes throughout the selected certificate chain before application data, in addition to CA and hostname verification. OpenSSL security level 2 alone is insufficient to prove an exact 2048-bit RSA minimum because it may accept 2047-bit moduli.

The optional Anthropic transport has a separate ordinary trust model and is not covered by that exact-key assurance. Release/profile-publication helpers have a separate [GitHub CLI profile](docs/RELEASE_TLS_PROFILE.md). Do not disable certificate verification or lower key policy to accept an obsolete endpoint. No system trust-store modification is required.

Credit vulnerability reporters in the advisory and release notes unless they request anonymity. Reproduce reports with synthetic data, assess impact, prepare and test a fix, coordinate disclosure, and record the affected and fixed versions.
