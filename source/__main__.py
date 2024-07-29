import os
import time
from pathlib import Path
from git import Repo
from structlog import getLogger
from source.git import clone_repo, get_latest_commit
from source.storage import save_commit_hexsha, get_latest_commit_from_file
from source.settings import Settings
from source.telegram import notify


settings = Settings()

REPO_NAME = settings.repo_url.replace(".git", "").split("/")[-1]
REPO_PATH = Path(settings.local_repo_path) / REPO_NAME


def main():
    logger = getLogger()

    logger.info("Checkin` updates...")

    if not os.path.exists(settings.local_repo_path):
        try:
            clone_repo(settings.repo_url, REPO_PATH)
        except Exception:
            logger.exception("Repository was not found", url=settings.repo_url)
            return

    if not os.path.exists("latest_commit"):
        save_commit_hexsha("")

    repo = Repo(REPO_PATH)
    latest_commit = get_latest_commit_from_file()

    if not latest_commit:
        latest_commit = get_latest_commit(repo, settings.branch)

        save_commit_hexsha(latest_commit)

    while True:
        repo.remotes.origin.pull()
        new_commit = get_latest_commit(repo, settings.branch)

        if new_commit != latest_commit:
            logger.info("NEW UPDATE! notifying...", commit_hexsha=new_commit)

            try:
                notify(settings.bot_token, settings.chat_id, f"♿️♿️♿️ НОВЫЙ КОММИТ <a href='{settings.repo_url}'>{REPO_NAME.upper()}</a>!!!\n\nВСЕМ ПРИГОТОВИТЬСЯ К КОДУ ОТ CHATGPT...")
            except Exception:
                logger.exception("Error while sending notification")

                time.sleep(60)

                continue

            latest_commit = new_commit

            save_commit_hexsha(latest_commit)

        time.sleep(settings.check_interval)


if __name__ == "__main__":
    main()
