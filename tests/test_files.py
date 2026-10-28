"""Tests for challenge 3: file downloads (path traversal).

While the bug is present, test_traversal_is_blocked FAILS (a crafted name reads
content/secret.txt, which lives outside the public folder). After you contain the
path to PUBLIC_DIR, all pass.
"""
from urllib.parse import quote

from tests.conftest import login_as

# Each of these aims at content/secret.txt (one level above the public folder).
# Different shapes of the same trick; none should return the secret.
TRAVERSAL_NAMES = [
    "../secret.txt",
    "../../content/secret.txt",
    "..%2fsecret.txt",            # url-encoded slash
    "%2e%2e%2fsecret.txt",        # url-encoded ../
    "/etc/hostname",              # absolute path, escapes the folder entirely
]


def test_legit_file_downloads(client):
    login_as(client, "alice")
    r = client.get("/files/download?name=welcome.txt")
    assert r.status_code == 200
    assert b"members portal" in r.data


def test_traversal_is_blocked(client):
    login_as(client, "alice")
    for name in TRAVERSAL_NAMES:
        r = client.get("/files/download?name=" + quote(name, safe=""))
        assert b"FLAG" not in r.data, (
            f"served a file outside the public folder via {name!r}"
        )
        assert r.status_code in (403, 404), (
            f"traversal {name!r} should be refused, got {r.status_code}"
        )
