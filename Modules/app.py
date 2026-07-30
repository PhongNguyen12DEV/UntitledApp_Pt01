import tkinter as tk
import Modules.setup as setup

app_data = setup.AppData

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(app_data["Title"])
        self.geometry(f"{app_data['width']}x{app_data['height']}")
        self.create_widgets()
        self.resizable(False, False)

        self.started = False 

    def create_widgets(self):
        self.label = tk.Label(self, text="Chào cậu nha")
        self.label.pack(pady=20)

        self.button = tk.Button(self, text="Start(F1)/Stop(F2)", command=self.Start_Stop_Click)
        self.button.pack(pady=10)

    def Start_Stop_Click(self):
        self.started = not self.started
        if self.started:
            print(setup.colorama.Fore.LIGHTYELLOW_EX + "Bắt đầu check...")
        else:
            print(setup.colorama.Fore.LIGHTRED_EX + "Dừng check...")