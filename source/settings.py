from pydantic_settings import BaseSettings



class Settings(BaseSettings):
    bot_token: str
    repo_url: str
    local_repo_path: str
    branch: str
    chat_id: str
    check_interval: int

    class Config:
        env_file = ".env"