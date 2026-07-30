import Modules.app as app
import Modules.setup as setup
import time




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
        print(setup.colorama.Fore.LIGHTYELLOW_EX + "Đang khởi động app...")
        time.sleep(1)
        App = app.App()
        setup.back()





    elif choice == "3":
        running = False
    else:
        print(setup.colorama.Fore.LIGHTRED_EX + "Xin lỗi cậu nha nhưng lựa chọn của cậu không hợp lệ")