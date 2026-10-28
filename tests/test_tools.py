"""Tests for bonus challenge A: tools (command injection).

While the bug is present, test_injection_does_not_run FAILS (a crafted host runs
a second command that creates a file). After you drop the shell and pass the host
as a single argument, all pass. These tests never touch the network.

On windows the injection test is skipped locally (cmd.exe uses different shell
syntax). Push your fix and GitHub Actions grades it on linux -- the tick there
is the one that counts.
"""
import sys

import pytest

from challenges.tools import run_check


def test_legit_host_is_echoed():
    out = run_check("cybersoc.kcl.ac.uk")
    assert "cybersoc.kcl.ac.uk" in out


@pytest.mark.skipif(sys.platform == "win32", reason="shell syntax differs on windows; graded on github actions")
def test_injection_does_not_run(tmp_path):
    sentinel = tmp_path / "pwned"
    # a host value that, if dropped into a shell, would run a second command
    payload = f"x; touch {sentinel}"
    run_check(payload)
    assert not sentinel.exists(), (
        "the input ran a second shell command -- it must be treated as one "
        "argument, not pasted into a shell string"
    )
