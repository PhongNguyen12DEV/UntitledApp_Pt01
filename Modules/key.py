import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "Data")
FILE_NAME = os.path.join(DATA_DIR, "key.json")

DEFAULT_DATA = {
    "gemini_api": "",
    "webhook": ""
}

def setup():
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_DATA, f, indent=4)

def load():
    setup()

    with open(FILE_NAME, "r", encoding="utf-8") as f:
        return json.load(f)

def save(data: dict):
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def get_gemini_api():
    return load()["gemini_api"]

def get_webhook():
    return load()["webhook"]

def set_gemini_api(api):
    data = load()
    data["gemini_api"] = api
    save(data)

def set_webhook(url):
    data = load()
    data["webhook"] = url
    save(data)

def is_setup():
    setup()
    data = load()

    return (
        data["gemini_api"].strip() != "" and
        data["webhook"].strip() != ""
    )
def has_gemini():
    data = load()
    return data.get("gemini_api", "").strip() != ""


def has_webhook():
    data = load()
    return data.get("webhook", "").strip() != ""