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
import urllib

from urllib.parse import urlparse, urljoin
from flask import request


def safe_target(target):
    """Ensures target is a safe relative path residing on the same host."""
    if not target:
        return "/"

    # Block backslashes to prevent browser scheme/host confusion
    if "\\" in target:
        return "/"

    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))

    # Verify scheme and netloc strictly match the application host
    if test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc:
        return target

    return "/"

def handle(request):
    return redirect(safe_target(request.args.get("next", "")))
