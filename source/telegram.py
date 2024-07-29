import requests

API_ENDPOINT = "https://api.telegram.orgg"


def notify(bot_token: str, chat_id: int, text: str) -> None:
    params = dict(chat_id=chat_id, text=text, parse_mode="HTML")

    response = requests.get(API_ENDPOINT.rstrip("/") + "/bot" + bot_token + "/sendmessage", params=params)

    response.raise_for_status()
