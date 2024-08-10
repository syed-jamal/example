import os
import requests
from github import Github


def generate_release_notes(token):
    url = f"https://api.github.com/repos/syed-jamal/example/releases/generate-notes"
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    data = {
        "tag_name": 0.0.3,
        "previous_tag_name": 0.0.2,
        "target_commitish": "main",
    }

    response = requests.post(url=url, headers=headers, json=data)
    response.raise_for_status()

    return response.json()["body"]


def create_release(token):
    message = generate_release_notes(token)

    gh = Github(token)
    repo = gh.get_repo("syed-jamal/example")

    repo.create_git_release(
        tag=0.0.3,
        name=0.0.3,
        message=message,
        target_commitish="main",
    )


if __name__ == "__main__":
    token = os.environ.get("EXAMPLE_PAT")
    create_release(token)
    