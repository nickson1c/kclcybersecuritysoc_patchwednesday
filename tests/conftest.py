import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app  # noqa: E402


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


def login_as(client, username):
    """Put a user in the session directly, so these tests don't depend on the
    login challenge being fixed first."""
    with client.session_transaction() as sess:
        sess["user"] = username
