import requests
from datetime import datetime
from zoneinfo import ZoneInfo

import Modules.key as key

PINK = 0xFF69B4


def send(title: str, description: str):
    if not key.has_webhook():
        return

    webhook = key.get_webhook()

    now = datetime.now(ZoneInfo("Asia/Ho_Chi_Minh"))

    embed = {
        "title": title,
        "description": description,
        "color": PINK,
        "fields": [
            {
                "name": "🕒 Thời gian",
                "value": now.strftime("%d/%m/%Y %H:%M:%S"),
                "inline": False
            },
        ],
        "timestamp": now.isoformat()
    }

    try:
        requests.post(webhook, json={"embeds": [embed]}, timeout=5)
    except Exception as e:
        print(e)


def app_open():
    send(
        "🟢 Ứng dụng",
        "Mở app nha cậu 💖"
    )


def app_close():
    send(
        "🔴 Ứng dụng",
        "Đóng app r"
    )


def start():
    send(
        "▶️ Trạng thái",
        "Đang chạy"
    )


def stop():
    send(
        "⏹️ Trạng thái",
        "Đang dừng"
    )