"""Upload main.py and README.md for the Elevator entry to GitHub.

Uses the GitHub Contents API: GET the current blob sha when the file
already exists, then PUT with that sha to update, or without it to
create. Auth goes through the custom.github surrogate.
"""

import base64
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/bin")
from dynamic_credentials import add_surrogate_to_request  # noqa: E402

OWNER = "rezimtirani"
REPO = "u-eager-stork-81-9647-what-the-elevator-would-say-90844958-entry"
API_BASE = "https://api.github.com"
ENTRY_DIR = Path(__file__).resolve().parent
FILES = ["main.py", "README.md"]


def call_github(method, url, payload=None):
    body = None
    headers = {"Accept": "application/vnd.github+json"}
    if payload is not None:
        body = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    request = urllib.request.Request(url, data=body, method=method, headers=headers)
    add_surrogate_to_request(request, "custom.github", allowed_hosts=["api.github.com"])
    with urllib.request.urlopen(request) as response:
        return json.loads(response.read().decode("utf-8"))


def current_sha(path):
    try:
        info = call_github("GET", f"{API_BASE}/repos/{OWNER}/{REPO}/contents/{path}")
    except urllib.error.HTTPError as error:
        if error.code == 404:
            return None
        raise
    return info.get("sha")


def upload_one(path):
    local = ENTRY_DIR / path
    encoded = base64.b64encode(local.read_bytes()).decode("ascii")
    payload = {"message": f"Add {path} — Elevator entry", "content": encoded}
    sha = current_sha(path)
    if sha:
        payload["sha"] = sha
    result = call_github(
        "PUT", f"{API_BASE}/repos/{OWNER}/{REPO}/contents/{path}", payload
    )
    print(f"{path}: {result['commit']['sha']}")
    return result["commit"]["sha"]


def main():
    for name in FILES:
        upload_one(name)
    print(f"Done: {OWNER}/{REPO}")


if __name__ == "__main__":
    main()
