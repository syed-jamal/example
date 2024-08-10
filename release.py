import os
import requests
from github import Github
import git

def write_to_version_file(version) -> None:
    with open("version.txt", "w") as f:
        f.write(f"{version}\n")

def generate_release_notes(token):
    url = f"https://api.github.com/repos/syed-jamal/example/releases/generate-notes"
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    data = {
        "tag_name": "0.0.4",
        "previous_tag_name": "0.0.3",
        "target_commitish": "main",
    }

    response = requests.post(url=url, headers=headers, json=data)
    response.raise_for_status()

    return response.json()["body"]


def create_release(token):
    write_to_version_file("0.0.4")

    local_repo = git.Repo(".")
    local_repo.git.commit("-am", f"Bump to Release version: 0.0.4")
    local_repo.git.tag("0.0.4")

    write_to_version_file("0.0.5-SNAPSHOT")

    local_repo.git.commit("-am", f"Bump to Pre-release version: 0.0.5-SNAPSHOT")

    message = generate_release_notes(token)

    local_repo.git.push()
    local_repo.git.push("origin", "0.0.4")

    gh = Github(token)
    repo = gh.get_repo("syed-jamal/example")

    repo.create_git_release(
        tag="0.0.4",
        name="0.0.4",
        message=message,
        target_commitish="main",
    )


if __name__ == "__main__":
    token = os.environ.get("EXAMPLE_PAT")
    create_release(token)
