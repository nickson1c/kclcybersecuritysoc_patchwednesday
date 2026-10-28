"""Tests for challenge 1: login (SQL injection).

While the bug is present, test_injection_is_rejected FAILS (a crafted username
logs in without the password). When you switch to a parameterised query, all of
these pass.
"""
from challenges.login import check_login

# A few shapes of the same trick: each tries to log in as alice with no valid
# password. None of them should succeed.
INJECTION_USERNAMES = [
    "alice' --",
    "alice'/*",
    "' OR '1'='1",
    "' OR 1=1 --",
    "admin' --",
]


def test_correct_credentials_work():
    assert check_login("alice", "alpaca") == "alice"
    assert check_login("admin", "hunter2") == "admin"


def test_wrong_password_is_rejected():
    assert check_login("alice", "wrong") is None
    assert check_login("nosuchuser", "whatever") is None


def test_injection_is_rejected():
    for username in INJECTION_USERNAMES:
        assert check_login(username, "anything") is None, (
            f"logged in with a crafted username ({username!r}) and no real "
            "password -- the query is still built from the input"
        )
