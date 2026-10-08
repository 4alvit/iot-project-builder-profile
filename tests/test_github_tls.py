"""Exercise the owned PyGithub requester, without contacting GitHub."""

import socket
import ssl
from collections import deque
from http.server import HTTPServer
from pathlib import Path
from typing import Any, cast
from unittest.mock import patch

import pytest
import requests
from github import Github
from github.Requester import HTTPSRequestsConnectionClass

from iot_profile_builder.github_tls import enforce_github_tls
from iot_profile_builder.models import ScanConfig
from iot_profile_builder.scanner.github_scanner import GitHubScanner
from tests.test_tls_policy import CHAIN_CASES, calibrate, peer, proxy
from tests.test_tls_policy import chains as chains
from tests.test_tls_policy import clean_environment as clean_environment


@pytest.mark.parametrize("version", [ssl.TLSVersion.TLSv1_2, ssl.TLSVersion.TLSv1_3])
@pytest.mark.parametrize("case", [*CHAIN_CASES, "untrusted", "wrong-host"])
def test_actual_scanner_rejects_weak_chain_before_auth(
    chains: dict[str, tuple[Path, Path, Path]],
    monkeypatch: pytest.MonkeyPatch,
    version: ssl.TLSVersion,
    case: str,
) -> None:
    chain = chains.get(case, chains["strong"])
    calibrate(chain, version)
    ca = chains["strong-ec"][2] if case == "untrusted" else chain[2]
    monkeypatch.setenv("REQUESTS_CA_BUNDLE", str(ca))
    with peer(chain, version, response_body=b'{"login":"synthetic","id":1}') as (port, seen):
        host = "127.0.0.1" if case == "wrong-host" else "localhost"

        def client(token: str) -> Github:
            return Github(token, base_url=f"https://{host}:{port}", retry=0)

        with patch("iot_profile_builder.scanner.github_scanner.Github", client):
            if case.startswith("strong"):
                scanner = GitHubScanner(ScanConfig("synthetic", token="synthetic-secret"))
                try:
                    assert scanner.user.login == "synthetic"
                finally:
                    scanner.client.close()
            else:
                with pytest.raises(requests.exceptions.SSLError):
                    GitHubScanner(ScanConfig("synthetic", token="synthetic-secret"))
    assert bool(seen["application_bytes"]) == case.startswith("strong")
    if case.startswith("strong"):
        assert b"Authorization: token synthetic-secret" in seen["application_bytes"]


def test_unrelated_clients_and_requester_class_are_unchanged() -> None:
    with Github() as owned, Github() as unrelated:
        enforce_github_tls(owned)
        assert (
            vars(unrelated)["_Github__requester"]._Requester__connectionClass
            is HTTPSRequestsConnectionClass
        )
        assert (
            vars(unrelated)["_Github__requester"]._Requester__httpsConnectionClass
            is HTTPSRequestsConnectionClass
        )
        assert (
            vars(owned)["_Github__requester"]._Requester__connectionClass
            is not HTTPSRequestsConnectionClass
        )
        assert (
            vars(owned)["_Github__requester"]._Requester__httpsConnectionClass
            is vars(owned)["_Github__requester"]._Requester__connectionClass
        )


@pytest.mark.parametrize(
    "field,value",
    [
        ("_Requester__connection", object()),
        ("_Requester__custom_connections", deque([object()])),
        ("_Requester__verify", False),
        ("_Requester__connectionClass", object()),
    ],
)
def test_unknown_or_used_layout_fails_before_mutation(field: str, value: object) -> None:
    client = Github()
    state = vars(vars(client)["_Github__requester"])
    previous = state[field]
    state[field] = value
    before = state.copy()
    try:
        with pytest.raises(RuntimeError):
            enforce_github_tls(client)
        assert state == before
    finally:
        state[field] = previous
        client.close()


@pytest.mark.parametrize("case", ["strong", "weak-2047-root"])
@pytest.mark.parametrize("encrypted_proxy", [False, True])
def test_github_proxy_tunnel(
    chains: dict[str, tuple[Path, Path, Path]],
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    case: str,
    encrypted_proxy: bool,
) -> None:
    roots = tmp_path / "roots.pem"
    roots.write_bytes(chains["strong"][2].read_bytes() + chains[case][2].read_bytes())
    monkeypatch.setenv("REQUESTS_CA_BUNDLE", str(roots))
    with (
        peer(
            chains[case], ssl.TLSVersion.TLSv1_3, response_body=b'{"login":"synthetic","id":1}'
        ) as (port, seen),
        proxy(port, chains["strong"] if encrypted_proxy else None) as (proxy_port, messages),
    ):
        scheme = "https" if encrypted_proxy else "http"
        monkeypatch.setenv("HTTPS_PROXY", f"{scheme}://localhost:{proxy_port}")
        with enforce_github_tls(Github(base_url=f"https://localhost:{port}", retry=0)) as client:
            if case == "strong":
                assert client.get_user("synthetic").login == "synthetic"
            else:
                with pytest.raises((requests.exceptions.SSLError, requests.exceptions.ProxyError)):
                    client.get_user("synthetic")
    assert len(messages) == 1
    assert bool(seen["application_bytes"]) == (case == "strong")


def test_weak_proxy_receives_no_connect_or_credentials(
    chains: dict[str, tuple[Path, Path, Path]], monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("REQUESTS_CA_BUNDLE", str(chains["weak-2047-root"][2]))
    with proxy(1, chains["weak-2047-root"]) as (port, messages):
        monkeypatch.setenv("HTTPS_PROXY", f"https://synthetic:secret@localhost:{port}")
        with (
            enforce_github_tls(Github(base_url="https://localhost:1", retry=0)) as client,
            pytest.raises(requests.exceptions.ProxyError),
        ):
            client.get_user("synthetic")
    assert messages == []


def test_unknown_pygithub_version_refused_before_mutation(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("iot_profile_builder.github_tls.version", lambda _: "2.11.0")
    with Github() as client:
        before = vars(vars(client)["_Github__requester"]).copy()
        with pytest.raises(RuntimeError, match="2.10.0"):
            enforce_github_tls(client)
        assert vars(vars(client)["_Github__requester"]) == before


def test_custom_url_connections_are_also_guarded(
    chains: dict[str, tuple[Path, Path, Path]], monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("REQUESTS_CA_BUNDLE", str(chains["weak-2047-root"][2]))
    original_resolve = socket.getaddrinfo

    def resolve(host: str, *args: Any, **kwargs: Any) -> Any:
        return original_resolve("127.0.0.1" if host == "sub.localhost" else host, *args, **kwargs)

    monkeypatch.setattr(socket, "getaddrinfo", resolve)
    with (
        peer(chains["weak-2047-root"], ssl.TLSVersion.TLSv1_3) as (port, observed),
        enforce_github_tls(Github(base_url="https://localhost:1", retry=0)) as client,
        pytest.raises(requests.exceptions.SSLError),
    ):
        vars(client)["_Github__requester"].requestJsonAndCheck(
            "GET", f"https://sub.localhost:{port}/custom"
        )
    assert observed["application_bytes"] == b""


def test_retry_pagination_and_auth_use_real_pygithub(
    chains: dict[str, tuple[Path, Path, Path]], monkeypatch: pytest.MonkeyPatch
) -> None:
    import json
    import threading
    from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

    from urllib3.util.retry import Retry

    received = []

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, _format: str, *_args: object) -> None:
            pass

        def do_GET(self) -> None:
            received.append((self.path, self.headers.get("Authorization")))
            payload: dict[str, Any] | list[dict[str, Any]]
            if len(received) == 1:
                status, payload = 503, {"message": "synthetic retry"}
            elif len(received) == 2:
                status, payload = 200, {"login": "synthetic", "id": 1}
            else:
                status = 200
                payload = [
                    {"id": len(received), "name": "first" if len(received) == 3 else "second"}
                ]
            body = json.dumps(payload).encode()
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            if len(received) == 3:
                self.send_header(
                    "Link",
                    f"<https://localhost:{cast(HTTPServer, self.server).server_port}"
                    + '/users/synthetic/repos?page=2>; rel="next"',
                )
            self.end_headers()
            self.wfile.write(body)

    monkeypatch.setenv("REQUESTS_CA_BUNDLE", str(chains["strong"][2]))
    with ThreadingHTTPServer(("127.0.0.1", 0), Handler) as server:
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(*chains["strong"][:2])
        server.socket = context.wrap_socket(server.socket, server_side=True)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            retry = Retry(total=1, status_forcelist=[503], backoff_factor=0)
            with enforce_github_tls(
                Github(
                    "synthetic-secret",
                    base_url=f"https://localhost:{server.server_port}",
                    retry=retry,
                    seconds_between_requests=0,
                )
            ) as client:
                repos = list(client.get_user("synthetic").get_repos())
                assert [repo.name for repo in repos] == ["first", "second"]
        finally:
            server.shutdown()
            thread.join(5)
            assert not thread.is_alive()
    assert [path for path, _ in received] == [
        "/users/synthetic",
        "/users/synthetic",
        "/users/synthetic/repos",
        "/users/synthetic/repos?page=2",
    ]
    assert all(auth == "token synthetic-secret" for _, auth in received)
