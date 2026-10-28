"""Challenge 3 (yours, harder): file downloads.

The files page lets you download a file by name from the public files folder:
/files/download?name=welcome.txt . The handler joins the name onto the folder
path and opens whatever comes out. By putting path segments in `name`, you can
walk out of the public folder and read files you shouldn't -- this is a path
traversal (a.k.a. directory traversal) bug.

YOUR JOB: `download` must only ever serve files that live INSIDE PUBLIC_DIR.
Anything that resolves to a path outside it should be refused with _denied().

WATCH OUT: blocking the literal string "../" is not enough. The tests send
several shapes of the same trick (absolute paths, url-encoded separators,
nested ones). Resolve the final real path and check it's inside PUBLIC_DIR.

HINT: pathlib's Path.resolve(), then `.is_relative_to(PUBLIC_DIR)` (3.9+), or
compare os.path.commonpath([...]). Flask's send_from_directory does this for you.
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
PUBLIC_DIR = os.path.join(os.path.dirname(HERE), "content", "files")


def index():
    names = sorted(os.listdir(PUBLIC_DIR))
    links = "".join(
        f'<li><a href="/files/download?name={n}">{n}</a></li>' for n in names
    )
    return f"<h1>files</h1><ul>{links}</ul>"


def download(request):
    name = request.args.get("name", "")
    # THIS IS THE VULNERABLE PART: `name` is trusted and joined straight on.
    path = os.path.join(PUBLIC_DIR, name)
    try:
        with open(path, "rb") as f:
            body = f.read()
    except (OSError, ValueError):
        return _not_found()
    return (body, 200, {"Content-Type": "text/plain; charset=utf-8"})


def _not_found():
    return ("no such file", 404)


def _denied():
    return ("access denied", 403)
