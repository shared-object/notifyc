def save_commit_hexsha(hash: str):
    with open(".latest_commit", "w") as file:
        file.write(hash)

        
def get_latest_commit_from_file() -> str:
    with open(".latest_commit", "r") as file:
        return file.read()

