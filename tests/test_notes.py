"""Tests for challenge 2: notes (IDOR).

While the bug is present, test_cannot_read_other_users_note FAILS (alice can
read bob's note 3). After you add the ownership check, all pass.
"""
from tests.conftest import login_as


def test_can_read_own_note(client):
    login_as(client, "alice")
    r = client.get("/notes/1")
    assert r.status_code == 200
    assert b"renew kclsu" in r.data


def test_cannot_read_other_users_note(client):
    login_as(client, "alice")
    r = client.get("/notes/3")  # note 3 belongs to bob
    assert r.status_code == 403, "alice should not be able to read bob's note"
    assert b"locker code" not in r.data


def test_missing_note_is_404(client):
    login_as(client, "alice")
    assert client.get("/notes/999").status_code == 404


def test_index_lists_only_your_notes(client):
    login_as(client, "alice")
    r = client.get("/notes")
    assert b"/notes/1" in r.data and b"/notes/2" in r.data
    assert b"/notes/3" not in r.data
