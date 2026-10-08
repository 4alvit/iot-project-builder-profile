# TLS certificate key policy

Owned TLS contexts retain CA and hostname verification and inspect the actual
verified chain, including its selected trust anchor, before application data.
RSA moduli must contain at least 2048 significant bits; EC keys need at least
224 bits; DSA requires p >= 2048 and q >= 224. Ed25519 and Ed448 are accepted.
Unknown algorithms or runtimes without an accessible verified chain fail closed.
OpenSSL security level 2 alone can accept a 2047-bit RSA modulus.

CPython 3.11 and 3.12 use the private `_sslobj.get_verified_chain` interface;
newer CPython versions may expose the public equivalent. This runtime contract
is tested rather than inferred from the Python version. Alternative Python
implementations are not implicitly supported.

The public-key decoder uses cryptography except on Intel macOS, where the
native Security framework reads key metadata without changing trust decisions.
The Intel backend accepts RSA and EC only. No system trust store is modified.

The TLS policy and Darwin metadata decoder are adapted from the MIT-licensed
victron-venus/inverter-dashboard implementation, copyright 2026 victron-venus.
The project MIT license also applies to these adaptations. This policy does
not establish the strength of inbound TLS terminators or unrelated transports.

## Client integration and compatibility

The GitHub scanner configures only its freshly created PyGithub instance. Both
the ordinary connection and PyGithub's allowed custom-URL HTTPS connections use
the policy. PyGithub is pinned to 2.10.0: an unknown version, changed requester
layout, already-used connection or disabled verification fails before the first
scanner request. Other GitHub instances and the global Requester class are not
modified. The existing authorization, retry, pagination and allowed-URL checks
remain in PyGithub. HTTP and HTTPS CONNECT proxies and Requests' CA environment
selection remain supported; SOCKS proxies are explicitly unsupported by this
adapter. An HTTPS proxy's chain is checked before CONNECT or proxy credentials.

The optional Anthropic integration is **not covered by this change**. Its
installed SDK uses httpx2 and native truststore verification, which needs a
separate verified-chain integration. Its original trust model remains unchanged;
this GitHub fix does not establish project-wide key-length compliance.

Install dependencies from the current lock: the core now directly requires
cryptography 50.0.2 on Linux, Windows and Apple Silicon. Intel macOS uses the
native RSA/EC decoder; this does not claim additional algorithms are supported
there. The Python 3.11 CI job executes real temporary-CA TLS, proxy and PyGithub tests,
while the existing full CI job remains on Python 3.12. Development tests use
cryptography-generated fixtures and therefore require an available wheel or
local build of that development dependency. The native decoder is imported
lazily, so non-macOS builds do not load Apple frameworks.

A pre-existing custom process-wide Requests/urllib3 TLS monkeypatch is outside
this transport contract. There is no option to disable ordinary certificate or
hostname verification in the scanner transport. Local reports and templates do
not require a network connection.
