"""Bonus challenge A: the network tools page.

A little "reachability check": you type a host and it runs a shell command to
look it up. The host you type is pasted into a shell command string, so shell
punctuation in the input lets you tack on a SECOND command of your choice --
this is command (OS) injection.

YOUR JOB: `run_check` must treat the whole input as a single argument, so no
extra command can ever run, whatever punctuation is in it. The fix is to stop
using a shell: pass the program and its arguments as a list.

HINT (works on windows, mac and linux):
    subprocess.run(
        [sys.executable, "-c", "import sys; print('resolving', sys.argv[1])", host],
        capture_output=True, text=True, timeout=5,
    )
`sys.executable` is the python that's running this app, so it exists everywhere,
and with a list (no shell=True) `host` can only ever be one argument.
"""
import subprocess
import sys  # noqa: F401  (you'll want it for the fix)


def run_check(host):
    """Return the tool output as text. THIS IS THE VULNERABLE PART."""
    cmd = f"echo resolving {host}"
    try:
        out = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=5
        )
        return out.stdout + out.stderr
    except subprocess.SubprocessError:
        return "lookup failed"


def handle(request, session):
    if not session.get("user"):
        return ("please log in first", 401)
    output = ""
    if request.method == "POST":
        output = f"<pre>{run_check(request.form.get('host', ''))}</pre>"
    return (
        "<h1>reachability check</h1>"
        '<form method="post"><input name="host" placeholder="hostname">'
        "<button>check</button></form>" + output
    )
