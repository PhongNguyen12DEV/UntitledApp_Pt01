import tkinter as tk
import Modules.setup as setup
import keyboard

app_data = setup.AppData

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(app_data["Title"])
        self.geometry(f"{app_data['width']}x{app_data['height']}")
        self.create_widgets()
        self.resizable(False, False)
        self.attributes("-topmost", setup.AppData["aot"])

        self.started = False 
        self.icon = tk.PhotoImage(file="assets/icon.png")
        self.iconphoto(True, self.icon)





        keyboard.add_hotkey("f1", self.Start_Stop)
        self.protocol("WM_DELETE_WINDOW", self.on_close)
    def create_widgets(self):
        top_frame = tk.Frame(self)
        top_frame.pack(fill="x", padx=10, pady=(10, 0))

        self.label = tk.Label(top_frame,text="Chào cậu nha",font=("Segoe UI", 15, "bold"))
        self.label.pack(anchor="nw", padx=10, pady=(10, 0))

        self.logo = tk.PhotoImage(file="assets/icon.png")
        self.logo = self.logo.subsample(7, 7)

        self.logo_label = tk.Label(top_frame,image=self.logo)
        self.logo_label.pack(side="right")

        self.session = tk.Label(self,text="Session: 00s",font=("Segoe UI", 10))
        self.session.pack(anchor="nw", padx=10, pady=(3, 0))

        bottom_frame = tk.Frame(self)
        bottom_frame.pack(side="bottom", fill="x", padx=5, pady=5)

        self.status = tk.Label(bottom_frame,text="Status: NULL",font=("Segoe UI", 10))
        self.status.pack(side="left")

        self.button = tk.Button(bottom_frame,text="Start / Stop (F1)",command=self.Start_Stop,width=14)
        self.button.pack(side="right")

    def Start_Stop(self):
        self.started = not self.started
        if self.started:
            print("ok")
        else:
            print("bruh")

    def on_close(self):
        keyboard.unhook_all_hotkeys()
        self.destroy()
