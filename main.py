import Modules.app as app
import Modules.setup as setup
import time
import Modules.key as key
import Modules.webhook as dis 




setup.In4()
running = True
while running:
    choice = input()
    if choice == "1":
        setup.Clear()
        setup.machine_info()
        setup.back()
    elif choice == "2":
        setup.Clear()
        key.setup()
        if not key.is_setup():

            print("=== Thiết lập lần đầu ===")

            if not key.has_webhook():
                webhook = input("Discord Webhook: ")
                key.set_webhook(webhook)

            if not key.has_gemini():
                api = input("Gemini API: ")
                key.set_gemini_api(api)

            print("Đã lưu cấu hình!\n")

        print("Đang khởi động app...")
        time.sleep(1)

        App = app.App()
        App.mainloop()

        setup.back()





    elif choice == "3":
        running = False
    else:
        print(setup.colorama.Fore.LIGHTRED_EX + "Xin lỗi cậu nha nhưng lựa chọn của cậu không hợp lệ")