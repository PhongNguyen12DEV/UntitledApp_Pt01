import json, os
import colorama
import platform

colorama.init(autoreset=True)

OS = platform.system()



with open("data/Global.json", "r", encoding="utf-8") as data:
    Data = json.load(data)
with open("data/app.json", "r", encoding="utf-8") as app:
    AppData = json.load(app)




def Logo():
    print(colorama.Fore.LIGHTRED_EX + r"""
 _   _       _   _ _   _          _      _               
| | | |_ __ | |_(_) |_| | ___  __| |    / \   _ __  _ __
| | | | '_ \| __| | __| |/ _ \/ _` |   / _ \ | '_ \| '_ \
| |_| | | | | |_| | |_| |  __/ (_| |  / ___ \| |_) | |_) |
 \___/|_| |_|\__|_|\__|_|\___|\__,_| /_/   \_\ .__/| .__/
                                             |_|   |_|
    """)
    print(colorama.Fore.LIGHTYELLOW_EX + "Được nấu ra bởi: " + colorama.Fore.LIGHTCYAN_EX + "Coder PhongVeChai")

def Clear():
    if OS == "Windows":
        os.system("cls")
    elif OS == "Linux" or OS == "Darwin":
        os.system("clear")

def machine_info():
    print(colorama.Fore.LIGHTCYAN_EX + f"Hệ điều hành: {platform.system()}")
    print(colorama.Fore.LIGHTCYAN_EX + f"Phiên bản: {platform.version()}")
    print(colorama.Fore.LIGHTCYAN_EX + f"Kiến trúc: {platform.architecture()[0]}")
    print(colorama.Fore.LIGHTCYAN_EX + f"Máy chủ: {platform.node()}")
    print(colorama.Fore.LIGHTCYAN_EX + f"Ngôn ngữ Python: {platform.python_version()}")
    print(colorama.Fore.LIGHTCYAN_EX + f"Kiến trúc CPU: {platform.processor()}")

def In4():
    Clear()
    Logo()
    print("//////////////////////////////////////////////////////////////////////")
    print(colorama.Fore.LIGHTCYAN_EX + f"Tên: {Data['name']}")
    print(colorama.Fore.LIGHTGREEN_EX + f"Bản: {Data['version']}")
    print(colorama.Fore.LIGHTCYAN_EX + f"Coder chính: {Data['author']}")
    print(colorama.Fore.LIGHTCYAN_EX + f"Bản quyền: {Data['license']}\n\n")
    print(colorama.Fore.LIGHTCYAN_EX + f"Đừng quên ghé thăm github và follow tiktok của tớ nha")
    print("//////////////////////////////////////////////////////////////////////\n")
    print(colorama.Fore.LIGHTBLUE_EX + f"Cảm ơn các con vợ nhìu: {Data['supporter']}")
    print(colorama.Fore.LIGHTBLUE_EX + f"[1] - Xem thông tin máy [2] - Bật app [3] - Thoát\n")
    print("//////////////////////////////////////////////////////////////////////\n")
    print(colorama.Fore.LIGHTYELLOW_EX + f"Chọn mục để bắt đầu nha cậu: ")



def back():
    print(colorama.Fore.LIGHTYELLOW_EX + "\n\nẤn Enter để quay lại nha cậu...")
    input()
    In4()