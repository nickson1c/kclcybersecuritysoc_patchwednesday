"""In-memory seed data shared by the challenges. No real database, no secrets."""

# username -> (password, role)
USERS = {
    "alice": ("alpaca", "member"),
    "bob": ("bonobo", "member"),
    "admin": ("hunter2", "admin"),
}

# note id -> (owner, text)
NOTES = {
    1: ("alice", "alice: remember to renew kclsu membership"),
    2: ("alice", "alice: ctf team name ideas"),
    3: ("bob", "bob: my locker code is 1337"),
    4: ("admin", "admin: committee meeting notes, members only"),
}


def seed():
    """Hook for app startup. The data above is static, so nothing to do yet."""
    return None
