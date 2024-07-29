import os
from git import Repo

def clone_repo(repo_url: str, local_path: os.PathLike):
    Repo.clone_from(repo_url, local_path)


def get_latest_commit(repo: Repo, branch: str):
    branch = repo.heads[branch]
    return branch.commit.hexsha