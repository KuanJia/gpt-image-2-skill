import json
import os
import subprocess
import sys
import urllib.error
import urllib.request


def get_github_token() -> str | None:
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        return token

    try:
        result = subprocess.run(
            ["git", "credential", "fill"],
            input="protocol=https\nhost=github.com\n\n",
            capture_output=True,
            text=True,
            timeout=20,
            check=False,
        )
    except Exception:
        return None

    if result.returncode != 0:
        return None

    for line in result.stdout.splitlines():
        if line.startswith("password="):
            return line.split("=", 1)[1]
    return None


def create_repo(token: str, name: str, description: str) -> None:
    payload = json.dumps(
        {
            "name": name,
            "description": description,
            "private": False,
            "has_issues": True,
            "has_projects": False,
            "has_wiki": False,
        }
    ).encode("utf-8")
    request = urllib.request.Request(
        "https://api.github.com/user/repos",
        data=payload,
        method="POST",
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "User-Agent": "codex-skill-publisher",
            "Content-Type": "application/json",
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        body = response.read().decode("utf-8")
        print(body)


def main() -> int:
    name = "gpt-image-2-skill"
    description = "Reusable Codex skill for generating images with gpt-image-2 via OpenAI-compatible APIs."
    token = get_github_token()
    if not token:
        print("Missing GitHub token from environment or git credential store.", file=sys.stderr)
        return 1

    try:
        create_repo(token, name, description)
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        print(body, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
