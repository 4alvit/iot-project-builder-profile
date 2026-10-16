# Supported heuristic and cryptographic profile

The complete heuristic mode performs GitHub scanning, ESPHome/D-Bus source analysis, deterministic profile generation, and local Markdown, JSON and HTML output:

```sh
uv sync --locked --all-extras
uv run --locked iot-profile-builder USERNAME --no-llm --output ./profile
```

No Anthropic credential, client construction or connection is needed in this mode. The LLM client is created only when generation actually requests LLM analysis. Built-in HTML embeds the installed locked Plotly library, so opening it makes no CDN script request. Custom user templates can introduce their own external resources and must be separately reviewed. PNG export remains optional and may require extra Plotly image-export tooling; readable HTML, JSON and Markdown are the complete supported output contract.

The scanner's owned PyGithub transport enforces [the exact certificate-chain key policy](tls-policy.md), including every selected trust anchor, before requests or credentials. It requires RSA >= 2048 significant bits, EC >= 224 bits, and DSA p >= 2048/q >= 224; Ed25519 and Ed448 are supported by the general decoder. Unsupported algorithms fail closed. CA/hostname verification is retained. The real temporary-CA suite tests both TLS 1.2 and TLS 1.3, RSA-2047 trust anchors, weak leaves/intermediates, proxies and custom allowed URLs. Use supported CPython 3.11+ with the locked dependencies; Intel macOS has the documented narrower native-decoder contract.

Optional profile publication and release tooling delegate GitHub HTTPS to `gh`; use the individually verified GitHub CLI/Go versions and `GH_HOST=github.com GODEBUG=fips140=on` prefix in [the release helper profile](RELEASE_TLS_PROFILE.md). This includes `scripts/publish_profile.py`; it preserves inherited environment for `gh` subprocesses. It does not execute Git network operations. Git clone/download is performed separately by the operator's supported HTTPS client.

The optional Anthropic mode remains supported for ordinary use, but its separate httpx2/truststore transport has not established this exact minimum-key profile. It is deliberately excluded from the strict profile, not silently treated as cryptographically inapplicable. Do not claim all optional transports, warning scopes, or generated third-party templates satisfy a stronger universal property.

## Permissions and state

Scanning reads public GitHub source and does not execute it. Any token should have minimum required read access; generation writes only local report files. Publication is a separate explicit operation requiring reviewed output and repository write rights. There is no password database or TLS server in the application. Repository text and model responses are untrusted and remain escaped in HTML; only the installed Plotly library is inserted as executable JavaScript.
