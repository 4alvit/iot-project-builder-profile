"""Instance-local PyGithub transport with exact verified-chain key checks."""

from __future__ import annotations

import socket
import ssl
from collections import deque
from importlib.metadata import version
from typing import Any
from urllib.parse import urlsplit

import requests
from github import Github
from github.Requester import HTTPSRequestsConnectionClass, Requester
from requests.adapters import HTTPAdapter
from urllib3.connection import HTTPSConnection
from urllib3.connectionpool import HTTPSConnectionPool

from .tls_policy import enforce_peer_key_policy


def _context() -> ssl.SSLContext:
    # Requests supplies its chosen CA file/directory. Do not add system roots.
    return enforce_peer_key_policy(ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT))


class _Connection(HTTPSConnection):
    def connect(self) -> None:
        previous = self.ssl_context
        self.ssl_context = _context()
        try:
            super().connect()
        except Exception:
            self.close()
            raise
        finally:
            # A later reconnect must not retain previously loaded CA roots.
            self.ssl_context = previous

    def _connect_tls_proxy(self, hostname: str, sock: socket.socket) -> ssl.SSLSocket:
        context = _context()
        if self.ca_certs or self.ca_cert_dir or self.ca_cert_data:
            context.load_verify_locations(self.ca_certs, self.ca_cert_dir, self.ca_cert_data)
        else:
            context.load_default_certs()
        if self.proxy_config is None:
            raise ssl.SSLError("HTTPS proxy configuration is missing")
        self.proxy_config = self.proxy_config._replace(ssl_context=context)
        return super()._connect_tls_proxy(hostname, sock)


class _Pool(HTTPSConnectionPool):
    ConnectionCls = _Connection


class _Adapter(HTTPAdapter):
    def init_poolmanager(
        self, connections: int, maxsize: int, block: bool = False, **pool_kwargs: Any
    ) -> None:
        super().init_poolmanager(connections, maxsize, block=block, **pool_kwargs)
        self.poolmanager.pool_classes_by_scheme = {
            **self.poolmanager.pool_classes_by_scheme,
            "https": _Pool,
        }

    def proxy_manager_for(self, proxy: str, **proxy_kwargs: Any) -> Any:
        if urlsplit(proxy).scheme not in ("http", "https"):
            raise ValueError("GitHub TLS supports HTTP and HTTPS CONNECT proxies only")
        manager = super().proxy_manager_for(proxy, **proxy_kwargs)
        manager.pool_classes_by_scheme = {**manager.pool_classes_by_scheme, "https": _Pool}
        return manager

    def build_connection_pool_key_attributes(
        self,
        request: requests.PreparedRequest,
        verify: bool | str,
        cert: str | tuple[str, str] | None = None,
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        if verify is False:
            raise ValueError("GitHub TLS certificate verification cannot be disabled")
        return super().build_connection_pool_key_attributes(request, verify, cert)


class _GitHubConnection(HTTPSRequestsConnectionClass):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        previous = self.adapter
        self.adapter = _Adapter(
            max_retries=self.retry, pool_connections=self.pool_size, pool_maxsize=self.pool_size
        )
        self.session.mount("https://", self.adapter)
        previous.close()


def enforce_github_tls(client: Github) -> Github:
    """Configure a fresh, owned PyGithub 2.10.0 client before its first request.

    PyGithub has no per-instance public adapter option. Pin and validate the
    private layout rather than changing Requester's global connection classes.
    """
    if version("PyGithub") != "2.10.0":
        raise RuntimeError("GitHub TLS integration requires PyGithub 2.10.0")
    requester = getattr(client, "_Github__requester", None)
    if not isinstance(requester, Requester):
        raise RuntimeError("Unsupported GitHub requester")
    state = vars(requester)
    connections = state.get("_Requester__custom_connections")
    if (
        state.get("_Requester__connectionClass") is not HTTPSRequestsConnectionClass
        or "_Requester__connection" not in state
        or state["_Requester__connection"] is not None
        or not isinstance(connections, deque)
        or connections
        or getattr(requester, "_Requester__httpsConnectionClass", None)
        is not HTTPSRequestsConnectionClass
        or state.get("_Requester__verify") is not True
    ):
        raise RuntimeError("GitHub TLS integration requires a fresh verified HTTPS requester")
    state["_Requester__connectionClass"] = _GitHubConnection
    state["_Requester__httpsConnectionClass"] = _GitHubConnection
    return client
