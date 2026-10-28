"""Tests for bonus challenge B: the continue redirect (open redirect).

While the bug is present, test_external_targets_are_blocked FAILS (next can point
at another site). After safe_target only allows same-site paths, all pass.
"""
from challenges.redirect_after_login import safe_target


def test_local_path_is_kept():
    assert safe_target("/notes") == "/notes"
    assert safe_target("/files") == "/files"


def test_empty_falls_back_home():
    assert safe_target("") == "/"


def test_external_targets_are_blocked():
    for target in [
        "http://evil.example",
        "https://evil.example/login",
        "//evil.example",            # protocol-relative: browsers treat as a host
        "https:evil.example",
    ]:
        assert safe_target(target) == "/", (
            f"{target!r} points off-site and should fall back to '/'"
        )
