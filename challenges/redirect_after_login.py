"""Bonus challenge B: the "continue" redirect.

Several links send you through /go?next=... so the app can bounce you onward
(e.g. back to the page you came from). The handler redirects to whatever `next`
says, including a full URL on another site. An attacker can send someone a
link to OUR site that quietly forwards them to a lookalike phishing page -- this
is an open redirect.

YOUR JOB: `safe_target` should allow only redirects that stay on THIS site
(a path like /notes). Anything pointing at another host should fall back to "/".

WATCH OUT: it's not just "starts with http". A leading "//" or "https:\\" is
also treated as another site by browsers. Allow only values that are a single
local path.

HINT: urllib.parse.urlparse(next).netloc must be empty AND the value must start
with a single "/" (reject "//..."). Then it's same-site.
"""
from flask import redirect


def safe_target(next_value):
    """Return a safe URL to redirect to. THIS IS THE VULNERABLE PART."""
    if not next_value:
        return "/"
    return next_value


def handle(request):
    return redirect(safe_target(request.args.get("next", "")))
