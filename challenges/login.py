"""Challenge 1 (walkthrough): the login check.

This is the bug we fix together at the start of the session. The login query is
built by pasting the username and password straight into a SQL string, so a
crafted username can change what the query means and log in without a valid
password.

YOUR JOB: make `check_login` only return a user when the username exists AND the
password is correct. A blocklist of "bad characters" will not pass the tests;
the fix is to stop mixing user input into the query text at all.

HINT: sqlite3 supports placeholders -> cur.execute("... WHERE x = ?", (value,))
"""
import sqlite3

from data import USERS


def _fresh_db():
    """A throwaway in-memory users table, rebuilt per request.

    (Building it per call also sidesteps the SQLite 'same thread' error that
    bit WelcomeCTF's Injector challenge -- a connection can't be shared across
    Flask's request threads.)
    """
    con = sqlite3.connect(":memory:")
    con.execute("CREATE TABLE users (username TEXT, password TEXT, role TEXT)")
    con.executemany(
        "INSERT INTO users VALUES (?, ?, ?)",
        [(u, p, r) for u, (p, r) in USERS.items()],
    )
    return con


def check_login(username, password):
    """Return the matching username, or None. THIS IS THE VULNERABLE PART."""
    con = _fresh_db()
    try:
        query = (
            "SELECT username FROM users "
            f"WHERE username = '{username}' AND password = '{password}'"
        )
        row = con.execute(query).fetchone()
        return row[0] if row else None
    except sqlite3.Error:
        # never 500 on a malformed query -- treat it as a failed login
        return None
    finally:
        con.close()


def handle(request, session):
    error = None
    if request.method == "POST":
        user = check_login(
            request.form.get("username", ""),
            request.form.get("password", ""),
        )
        if user:
            session["user"] = user
            return _redirect_home()
        error = "wrong username or password"
    return _form(error)


def _redirect_home():
    from flask import redirect, url_for

    return redirect(url_for("home"))


def _form(error):
    msg = f'<p style="color:red">{error}</p>' if error else ""
    return (
        "<h1>log in</h1>" + msg + '<form method="post">'
        '<p>username <input name="username"></p>'
        '<p>password <input name="password" type="password"></p>'
        '<button>log in</button></form>'
    )
