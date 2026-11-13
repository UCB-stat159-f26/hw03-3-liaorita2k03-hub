import socket

import pytest


@pytest.fixture(autouse=True)
def block_network(monkeypatch):
    def fail_on_network(*args, **kwargs):
        pytest.fail("Automated tests must use local fixtures. Network access attempted.")

    monkeypatch.setattr(socket, "getaddrinfo", fail_on_network)
    monkeypatch.setattr(socket.socket, "connect", fail_on_network)
    monkeypatch.setattr(socket.socket, "connect_ex", fail_on_network)
