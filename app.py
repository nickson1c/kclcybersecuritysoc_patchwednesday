"""patch wednesday: a small members portal with a few deliberate bugs to fix.

Run it:  python app.py   then open http://127.0.0.1:5000
Each bug lives in its own module under challenges/. Fix the function, re-run the
tests (pytest), and when they pass you've patched it. Start with the README.
"""
from flask import Flask, redirect, request, session, url_for

from challenges import files, login, notes, redirect_after_login, tools
from data import USERS, seed

app = Flask(__name__)
app.secret_key = "patch-wednesday-not-a-real-secret"


@app.route("/")
def home():
    who = session.get("user")
    if not who:
        return (
            "<h1>cybersoc portal</h1>"
            '<p><a href="/login">log in</a></p>'
        )
    return (
        f"<h1>hi {who}</h1><ul>"
        '<li><a href="/notes">my notes</a></li>'
        '<li><a href="/files">files</a></li>'
        '<li><a href="/tools">tools</a></li>'
        '<li><a href="/logout">log out</a></li></ul>'
    )


@app.route("/login", methods=["GET", "POST"])
def login_view():
    return login.handle(request, session)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


@app.route("/go")
def go():
    # redirect the user onward after some action (e.g. ?next=/notes)
    return redirect_after_login.handle(request)


@app.route("/notes")
@app.route("/notes/<int:note_id>")
def notes_view(note_id=None):
    return notes.handle(request, session, note_id)


@app.route("/files")
def files_index():
    return files.index()


@app.route("/files/download")
def files_download():
    return files.download(request)


@app.route("/tools", methods=["GET", "POST"])
def tools_view():
    return tools.handle(request, session)


if __name__ == "__main__":
    seed()
    print("seeded users:", ", ".join(USERS))
    app.run(debug=False, port=5000)
