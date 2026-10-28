"""Challenge 2 (yours, easier): notes.

Logged-in users can read notes at /notes/<id>. The problem: the handler looks up
a note by its id and returns it to whoever is logged in, without checking who the
note belongs to. So any member can read anyone else's notes just by changing the
number in the URL. This class of bug is called IDOR (insecure direct object
reference).

YOUR JOB: a user should only be able to read their OWN notes. Reading someone
else's note id should be refused (return the _forbidden() response below), the
same as a note that doesn't exist.

There is no syntax trick here -- it's a missing ownership check.
"""
from data import NOTES


def handle(request, session, note_id):
    who = session.get("user")
    if not who:
        return _login_first()

    if note_id is None:
        mine = [i for i, (owner, _) in NOTES.items() if owner == who]
        links = "".join(f'<li><a href="/notes/{i}">note {i}</a></li>' for i in mine)
        return f"<h1>{who}'s notes</h1><ul>{links}</ul>"

    note = NOTES.get(note_id)
    if not note:
        return _not_found()

    owner, text = note
    # THIS IS THE VULNERABLE PART: it returns the note without checking `owner`.
    return f"<h1>note {note_id}</h1><pre>{text}</pre>"


def _login_first():
    return ("please log in first", 401)


def _not_found():
    return ("no such note", 404)


def _forbidden():
    return ("not your note", 403)
