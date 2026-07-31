# main.py (hoặc tên file chính của bạn)
import tkinter as tk
import win32gui
import win32con
import win32api
import os
from Modules.Chatbot import GeminiChatbot  # Import chatbot
import Modules.key as key
import Modules.webhook as dis
import Modules.screenshot as screenshot
import Modules.setup as setup


app_data = setup.AppData

import json

with open("data/key.json","r", encoding="utf-8") as a:
    Key = json.load(a)

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title(app_data["Title"])
        self.geometry(f"{app_data['width']}x{app_data['height']}")
        self.resizable(False, False)
        self.attributes("-topmost", app_data["aot"])
        
        self.closed = False
        self.answer_text = "___"
        
        # Khởi tạo Gemini Chatbot
        self.init_chatbot()

        self.icon = tk.PhotoImage(file="assets/icon.png")
        self.iconphoto(True, self.icon)
        
        self.f8_down = False
        
        self.create_widgets()
        
        # Tạo cửa sổ answer sau khi cửa sổ chính đã được tạo
        self.after(100, self.create_answer_window)
        
        self.hotkey_after = self.after(20, self.check_hotkey)
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        
        dis.app_open()
    
    def init_chatbot(self):
        """Khởi tạo chatbot Gemini"""
        try:
            # Lấy API key từ biến môi trường hoặc hardcode
            api_key = Key['gemini_api']
            if api_key is None:
                # Bạn có thể đặt API key trực tiếp ở đây (không khuyến khích)
                # api_key = "YOUR_API_KEY_HERE"
                print("⚠️ Chưa đặt GEMINI_API_KEY trong biến môi trường")
                print("📌 Đặt bằng lệnh: set GEMINI_API_KEY=your_api_key (Windows)")
                print("📌 Hoặc: export GEMINI_API_KEY=your_api_key (Mac/Linux)")
                self.chatbot = None
            else:
                self.chatbot = GeminiChatbot(api_key)
                print("✅ Đã khởi tạo Gemini Chatbot thành công!")
        except Exception as e:
            print(f"❌ Lỗi khởi tạo chatbot: {e}")
            self.chatbot = None

    def create_widgets(self):
        # Frame trên cùng
        top_frame = tk.Frame(self)
        top_frame.pack(fill="x", padx=10, pady=(10, 0))

        self.label = tk.Label(
            top_frame,
            text="Chào cậu nha",
            font=("Segoe UI", 15, "bold")
        )
        self.label.pack(anchor="nw")

        # Frame giữa (hiển thị trạng thái)
        mid_frame = tk.Frame(self)
        mid_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.status_label = tk.Label(
            mid_frame,
            text="Sẵn sàng chụp ảnh",
            font=("Segoe UI", 12),
            fg="green"
        )
        self.status_label.pack(expand=True)

        # Frame dưới cùng (chứa nút)
        bottom = tk.Frame(self)
        bottom.pack(side="bottom", fill="x", padx=5, pady=5)

        # Nút chụp ảnh
        self.capture_button = tk.Button(
            bottom,
            text="📷 Chụp ảnh (F8)",
            width=20,
            height=2,
            font=("Segoe UI", 12, "bold"),
            command=self.capture_now,
            bg="#4CAF50",
            fg="white",
            relief="raised",
            bd=3
        )
        self.capture_button.pack(expand=True, fill="x", padx=10, pady=10)

    def create_answer_window(self):
        """Tạo cửa sổ answer với 2 label: Answer và nội dung đáp án"""
        try:
            if self.closed:
                return
                
            self.answer_window = tk.Toplevel(self)
            self.answer_window.title("Answer")
            self.answer_window.geometry("300x145")
            self.answer_window.resizable(False, False)
            self.answer_window.attributes("-topmost", True)
            
            main_frame = tk.Frame(self.answer_window, bg="white")
            main_frame.pack(expand=True, fill="both")
            
            self.answer_title_label = tk.Label(
                main_frame,
                text="Answer",
                font=("Segoe UI", 20, "bold"),
                fg="black",
                bg="white"
            )
            self.answer_title_label.pack(pady=(30, 10))
            
            self.answer_content_label = tk.Label(
                main_frame,
                text="___",
                font=("Segoe UI", 24, "bold"),  # Đậm hơn để dễ đọc
                fg="#FF6B6B",  # Màu đỏ nổi bật
                bg="white"
            )
            self.answer_content_label.pack(pady=(0, 30), expand=True)
            
            self.answer_window.protocol("WM_DELETE_WINDOW", self.on_close)
            
            self.answer_window.lift()
            self.answer_window.focus_force()
            
        except Exception as e:
            print(f"Lỗi khi tạo cửa sổ answer: {e}")
    
    def update_answer_label(self, new_text=None):
        """Cập nhật label nội dung trong cửa sổ answer"""
        if new_text is not None:
            self.answer_text = new_text
        if hasattr(self, 'answer_content_label'):
            self.answer_content_label.config(text=self.answer_text)
            # Tự động resize font nếu text quá dài
            if len(self.answer_text) > 20:
                self.answer_content_label.config(font=("Segoe UI", 18, "bold"))
            else:
                self.answer_content_label.config(font=("Segoe UI", 24, "bold"))

    def check_hotkey(self):
        """Kiểm tra phím F8"""
        if self.closed:
            return

        pressed = win32api.GetAsyncKeyState(win32con.VK_F8) < 0

        if pressed and not self.f8_down:
            self.f8_down = True
            self.capture_now()

        elif not pressed:
            self.f8_down = False

        self.hotkey_after = self.after(20, self.check_hotkey)
    
    def capture_now(self):
        """Hàm chụp ảnh và lấy đáp án từ Gemini"""
        try:
            # Đổi trạng thái
            self.status_label.config(text="📸 Đang chụp ảnh...", fg="orange")
            self.capture_button.config(
                text="⏳ Đang xử lý...",
                bg="#FF9800",
                state="disabled"
            )
            self.update()
            
            # 1. Chụp ảnh màn hình
            screenshot.capture()  # Giả sử hàm này trả về đường dẫn ảnh
            screen_path = "screenshot/screen.png"
            # 2. Gửi ảnh lên Discord (nếu có)
            screenshot.send_dis()
            
            # 3. Gửi ảnh cho Gemini để lấy đáp án
            if self.chatbot:
                self.status_label.config(text="🤖 Đang hỏi Gemini...", fg="purple")
                self.update()
                
                answer = self.chatbot.read_image_and_get_answer(screen_path)
                
                # Cập nhật đáp án lên cửa sổ answer
                self.update_answer_label(answer)
                
                self.status_label.config(text=f"✅ Đáp án: {answer}", fg="green")
            else:
                # Nếu chưa có chatbot, vẫn hiển thị "xong" như cũ
                self.update_answer_label("xong")
                self.status_label.config(text="⚠️ Chưa cấu hình Gemini", fg="orange")
            
            # Cập nhật trạng thái thành công
            self.capture_button.config(
                text="📷 Chụp ảnh (F8)",
                bg="#4CAF50",
                state="normal"
            )
            
            # Reset trạng thái sau 3 giây
            self.after(3000, self.reset_status)
            
        except Exception as e:
            # Xử lý lỗi
            self.status_label.config(text=f"❌ Lỗi: {str(e)}", fg="red")
            self.capture_button.config(
                text="📷 Chụp ảnh (F8)",
                bg="#4CAF50",
                state="normal"
            )
    
    def reset_status(self):
        """Reset trạng thái về mặc định"""
        if not self.closed:
            self.status_label.config(text="Sẵn sàng chụp ảnh", fg="green")

    def on_close(self):
        """Đóng ứng dụng - đóng cả 2 cửa sổ"""
        if self.closed:
            return
            
        self.closed = True
        
        if hasattr(self, 'answer_window') and self.answer_window.winfo_exists():
            try:
                self.answer_window.destroy()
            except:
                pass
        
        if self.hotkey_after is not None:
            try:
                self.after_cancel(self.hotkey_after)
            except:
                pass
        
        dis.app_close()
        
        try:
            self.destroy()
        except:
            pass

