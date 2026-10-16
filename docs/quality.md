# Quality evidence and limitations

The required gate runs Ruff, formatting, strict mypy and pytest using the frozen uv lock. The application suite exercises source analysis, public GitHub scanning, heuristic/optional LLM generation, rendering and publishing helpers. Actual temporary-CA tests check the selected certificate chain and prove credentials are not sent to a rejected peer. Python assertions remain enabled.

The October 2026 application coverage measurement is about 69 percent. It is not full-source 80 percent coverage: release tooling and every supported platform branch require separate evidence. Five native macOS decoder cases skip on non-macOS systems; they run on macOS. PyGithub client construction uses the current Auth.Token interface in production and TLS tests, avoiding the deprecated positional-token API. Neither maximal warning strictness nor exhaustive test coverage is claimed.

[RC fuzzing](fuzzing.md) is source-bound; ordinary branch runs do not start mutation campaigns. No new campaign is claimed merely because normal CI is green.

The [supported profile](SUPPORTED_PROFILE.md) describes verified cryptographic boundaries. Optional Anthropic/custom template behavior does not inherit the stricter GitHub transport claim. Whole-product algorithm/credential agility, independent reproducible builds, comprehensive interface deprecation and accessibility reviews, systematic hardening and a complete security assurance case remain future work. Maintainer [continuity](../GOVERNANCE.md) is also explicitly unresolved.

Dependencies are identified by `pyproject.toml` and `uv.lock`, with standard MIT/BSD/Apache/Python-family FLOSS libraries including PyGithub, requests/urllib3, cryptography, Anthropic/httpx, Jinja, Plotly and Matplotlib. Native system frameworks on Intel macOS retain their platform terms. The project MIT license does not relicense those dependencies or generated external content. The embedded Plotly JavaScript keeps its upstream license notice.
