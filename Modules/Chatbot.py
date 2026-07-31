# chatbot.py
import google.generativeai as genai
import base64
from PIL import Image
import io
import json
import time

with open("data/key.json", "r", encoding="utf-8") as a:
    Key = json.load(a)


class GeminiChatbot:
    def __init__(self, api_key=None):
        """
        Khởi tạo Gemini Chatbot
        Args:
            api_key: API key của Google Gemini (nếu None thì lấy từ file key.json)
        """
        if api_key is None:
            api_key = Key.get('gemini_api')
            if api_key is None:
                raise ValueError("Vui lòng cung cấp GEMINI_API_KEY trong file key.json")
        
        genai.configure(api_key=api_key)
        
        # Danh sách model mới nhất từ API của bạn - ưu tiên model mới nhất
        self.model_names = [
            'gemini-3.5-flash',           # Mới nhất 3.5
            'gemini-3-pro-image',         # Pro image
            'gemini-3.1-flash-image',     # 3.1 Flash image
            'gemini-3.1-flash-image-preview',
            'gemini-3.1-flash-lite-image',
            'gemini-2.5-flash-image',     # Chuyên về image
            'gemini-2.0-flash',           # Flash 2.0
            'gemini-flash-latest',        # Latest flash
            'gemini-pro-latest',          # Latest pro
            'gemini-3.1-pro-preview',     # 3.1 Pro preview
            'gemini-3-flash-preview',     # 3 Flash preview
        ]
        
        self.model = None
        self.current_model_name = None
        
        # Lấy danh sách model có sẵn từ API
        try:
            print("📋 Đang lấy danh sách model có sẵn...")
            available_models = genai.list_models()
            available_model_names = []
            
            print("📋 Các model Gemini có sẵn:")
            for m in available_models:
                if 'generateContent' in m.supported_generation_methods:
                    model_name = m.name.replace('models/', '')
                    if 'gemini' in model_name.lower() or 'gemma' in model_name.lower():
                        available_model_names.append(model_name)
                        print(f"  ✅ {model_name}")
            
            # Thử từng model trong danh sách ưu tiên
            found_model = False
            for model_name in self.model_names:
                if model_name in available_model_names:
                    try:
                        print(f"🔄 Đang kết nối với model: {model_name}")
                        self.model = genai.GenerativeModel(model_name)
                        self.current_model_name = model_name
                        print(f"✅ Đã kết nối thành công với model: {model_name}")
                        found_model = True
                        break
                    except Exception as e:
                        print(f"❌ Lỗi khi kết nối với {model_name}: {e}")
                        continue
                else:
                    print(f"❌ Model {model_name} không có sẵn")
            
            # Nếu không tìm thấy model nào trong danh sách ưu tiên
            if not found_model:
                print("🔄 Không tìm thấy model ưu tiên, thử các model có sẵn khác...")
                for model_name in available_model_names:
                    if 'gemini' in model_name.lower() and 'image' in model_name.lower():
                        try:
                            print(f"🔄 Đang thử model image: {model_name}")
                            self.model = genai.GenerativeModel(model_name)
                            self.current_model_name = model_name
                            print(f"✅ Đã kết nối thành công với model: {model_name}")
                            found_model = True
                            break
                        except:
                            continue
                
                # Nếu vẫn chưa có, thử model gemini đầu tiên
                if not found_model:
                    for model_name in available_model_names:
                        if 'gemini' in model_name.lower():
                            try:
                                print(f"🔄 Đang thử model: {model_name}")
                                self.model = genai.GenerativeModel(model_name)
                                self.current_model_name = model_name
                                print(f"✅ Đã kết nối thành công với model: {model_name}")
                                found_model = True
                                break
                            except:
                                continue
            
        except Exception as e:
            print(f"❌ Lỗi khi lấy danh sách model: {e}")
            # Fallback: thử các model phổ biến
            fallback_models = [
                'gemini-3.5-flash',
                'gemini-2.5-flash-image',
                'gemini-2.0-flash',
                'gemini-flash-latest'
            ]
            for model_name in fallback_models:
                try:
                    print(f"🔄 Đang thử model fallback: {model_name}")
                    self.model = genai.GenerativeModel(model_name)
                    self.current_model_name = model_name
                    print(f"✅ Đã kết nối thành công với model: {model_name}")
                    break
                except Exception as e:
                    print(f"❌ Lỗi với {model_name}: {e}")
                    continue
        
        if self.model is None:
            raise Exception("Không thể khởi tạo bất kỳ model Gemini nào. Vui lòng kiểm tra API key và kết nối internet.")
        
        # Prompt template để chỉ lấy đáp án đúng
        self.prompt_template = """
        Bạn là một trợ lý AI chuyên về giải đáp câu hỏi trắc nghiệm.
        
        Nhiệm vụ của bạn:
        1. Xem ảnh câu hỏi trắc nghiệm được cung cấp
        2. Xác định đáp án ĐÚNG
        3. CHỈ trả về nội dung của đáp án đúng, KHÔNG thêm bất kỳ giải thích hay nội dung nào khác
        
        Quy tắc:
        - Chỉ trả về đúng nội dung đáp án (ví dụ: "phongdeptrai", "A", "Đáp án A", tùy theo định dạng trong ảnh)
        - Không thêm dấu câu, không giải thích, không số thứ tự
        - Nếu không thể xác định, trả về "Không xác định"
        
        Ví dụ:
        Ảnh hiển thị:
        a. skibid
        b. dop dop
        c. adubip
        d. phongdeptrai
        Trả về: phongdeptrai
        
        Hoặc:
        A. Hà Nội
        B. TP.HCM
        C. Đà Nẵng
        D. Cần Thơ
        Đáp án đúng: A. Hà Nội
        Trả về: Hà Nội
        """
    
    def list_available_models(self):
        """Liệt kê các model có sẵn và hỗ trợ generateContent"""
        try:
            models = genai.list_models()
            print("📋 Các model Gemini có sẵn và hỗ trợ generateContent:")
            
            gemini_models = []
            for model in models:
                if 'generateContent' in model.supported_generation_methods:
                    model_name = model.name.replace('models/', '')
                    if 'gemini' in model_name.lower() or 'gemma' in model_name.lower():
                        gemini_models.append(model_name)
            
            # Sắp xếp và hiển thị
            for name in sorted(gemini_models):
                # Đánh dấu model image
                if 'image' in name.lower():
                    print(f"  🖼️  {name}")
                else:
                    print(f"  ✅ {name}")
            
            return gemini_models
        except Exception as e:
            print(f"Lỗi khi liệt kê model: {e}")
            return None
    
    def encode_image(self, image_path):
        """Mã hóa ảnh thành base64"""
        try:
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')
        except Exception as e:
            print(f"Lỗi đọc ảnh: {e}")
            return None
    
    def encode_image_from_pil(self, pil_image):
        """Mã hóa ảnh từ PIL Image thành base64"""
        try:
            buffered = io.BytesIO()
            # Nén ảnh để giảm dung lượng
            pil_image.save(buffered, format="JPEG", quality=80, optimize=True)
            return base64.b64encode(buffered.getvalue()).decode('utf-8')
        except Exception as e:
            print(f"Lỗi mã hóa ảnh PIL: {e}")
            return None
    
    def read_image_and_get_answer(self, image_input):
        """
        Đọc ảnh và trả về đáp án đúng
        
        Args:
            image_input: Có thể là đường dẫn file ảnh (str) hoặc PIL Image object
        
        Returns:
            str: Đáp án đúng hoặc "Không xác định" nếu không tìm thấy
        """
        if self.model is None:
            return "Lỗi: Chưa khởi tạo được model Gemini"
        
        try:
            # Xử lý ảnh đầu vào
            image_data = None
            
            if isinstance(image_input, str):
                # Đọc ảnh bằng PIL để có thể resize
                try:
                    img = Image.open(image_input)
                    # Resize ảnh nếu quá lớn (giảm thời gian xử lý)
                    max_size = 1024
                    if img.width > max_size or img.height > max_size:
                        img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
                    image_data = self.encode_image_from_pil(img)
                except Exception as e:
                    print(f"Lỗi đọc ảnh bằng PIL: {e}")
                    # Fallback: đọc ảnh trực tiếp
                    image_data = self.encode_image(image_input)
                    
            elif isinstance(image_input, Image.Image):
                img = image_input
                max_size = 1024
                if img.width > max_size or img.height > max_size:
                    img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
                image_data = self.encode_image_from_pil(img)
            else:
                return "Không xác định (định dạng ảnh không hợp lệ)"
            
            if image_data is None:
                return "Không xác định (lỗi đọc/mã hóa ảnh)"
            
            # Gọi Gemini API
            print(f"🔄 Đang gửi ảnh lên Gemini (model: {self.current_model_name})...")
            
            # Tạo prompt với ảnh
            response = self.model.generate_content(
                [
                    self.prompt_template,
                    {"mime_type": "image/jpeg", "data": image_data}
                ]
            )
            
            # Lấy kết quả và làm sạch
            answer = response.text.strip()
            print(f"📝 Gemini trả về: {answer}")
            
            # Nếu kết quả quá dài hoặc có nhiều dòng, lấy dòng đầu tiên
            if "\n" in answer:
                answer = answer.split("\n")[0].strip()
            
            # Xóa dấu câu nếu có
            answer = answer.strip('.,!?:;')
            
            # Xử lý các định dạng đáp án khác nhau
            if answer and len(answer) >= 3:
                # Xử lý "A. Nội dung" -> "Nội dung"
                if answer[1] == '.' and answer[2] == ' ':
                    answer = answer[3:].strip()
                # Xử lý "a) Nội dung" -> "Nội dung"
                elif answer[1] == ')' and answer[2] == ' ':
                    answer = answer[3:].strip()
                # Xử lý "A." -> "Nội dung"
                elif answer[1] == '.' and len(answer) > 2:
                    answer = answer[2:].strip()
                # Xử lý số thứ tự "1. Nội dung"
                elif answer[0].isdigit() and answer[1] == '.' and answer[2] == ' ':
                    answer = answer[3:].strip()
            
            return answer if answer else "Không xác định"
            
        except Exception as e:
            error_msg = str(e)
            print(f"❌ Lỗi khi gọi Gemini API: {error_msg}")
            print(f"Model đang dùng: {self.current_model_name}")
            
            # Nếu lỗi do model deprecated, thử model khác
            if "no longer available" in error_msg or "not found" in error_msg:
                print("🔄 Model không còn khả dụng, đang thử model khác...")
                # Thử các model image khác
                try:
                    # Thử gemini-3.1-flash-image
                    self.model = genai.GenerativeModel('gemini-3.1-flash-image')
                    self.current_model_name = 'gemini-3.1-flash-image'
                    print(f"✅ Đã chuyển sang model: gemini-3.1-flash-image")
                    return self.read_image_and_get_answer(image_input)
                except:
                    pass
                
                try:
                    # Thử gemini-2.5-flash-image
                    self.model = genai.GenerativeModel('gemini-2.5-flash-image')
                    self.current_model_name = 'gemini-2.5-flash-image'
                    print(f"✅ Đã chuyển sang model: gemini-2.5-flash-image")
                    return self.read_image_and_get_answer(image_input)
                except:
                    pass
            
            return f"Lỗi: {error_msg}"
    
    def read_image_with_custom_prompt(self, image_input, custom_prompt):
        """
        Đọc ảnh với prompt tùy chỉnh
        
        Args:
            image_input: Đường dẫn file ảnh hoặc PIL Image
            custom_prompt: Prompt tùy chỉnh
        
        Returns:
            str: Kết quả từ Gemini
        """
        if self.model is None:
            return "Lỗi: Chưa khởi tạo được model Gemini"
        
        try:
            # Xử lý ảnh tương tự như trên
            image_data = None
            
            if isinstance(image_input, str):
                try:
                    img = Image.open(image_input)
                    max_size = 1024
                    if img.width > max_size or img.height > max_size:
                        img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
                    image_data = self.encode_image_from_pil(img)
                except:
                    image_data = self.encode_image(image_input)
                    
            elif isinstance(image_input, Image.Image):
                img = image_input
                max_size = 1024
                if img.width > max_size or img.height > max_size:
                    img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
                image_data = self.encode_image_from_pil(img)
            else:
                return "Không xác định (định dạng ảnh không hợp lệ)"
            
            if image_data is None:
                return "Không xác định (lỗi đọc/mã hóa ảnh)"
            
            response = self.model.generate_content([
                custom_prompt,
                {"mime_type": "image/jpeg", "data": image_data}
            ])
            
            return response.text.strip()
            
        except Exception as e:
            print(f"Lỗi khi gọi Gemini API: {e}")
            return f"Lỗi: {str(e)}"


# Hàm tiện ích để sử dụng nhanh
def get_answer_from_image(image_path, api_key=None):
    """
    Hàm tiện ích: Lấy đáp án từ ảnh
    
    Args:
        image_path: Đường dẫn đến file ảnh
        api_key: Gemini API key (nếu None sẽ lấy từ file key.json)
    
    Returns:
        str: Đáp án đúng
    """
    chatbot = GeminiChatbot(api_key)
    return chatbot.read_image_and_get_answer(image_path)


# Ví dụ sử dụng
if __name__ == "__main__":
    print("=== CHATBOT GEMINI ===")
    print("🔍 Đang tìm model phù hợp...")
    
    try:
        # Khởi tạo chatbot
        chatbot = GeminiChatbot()
        print(f"\n✅ Model đang dùng: {chatbot.current_model_name}")
        
        # Liệt kê các model có sẵn
        print("\n📋 Danh sách model Gemini có sẵn:")
        chatbot.list_available_models()
        
        print("\n💡 Hướng dẫn sử dụng:")
        print("  chatbot = GeminiChatbot()")
        print("  answer = chatbot.read_image_and_get_answer('path/to/image.png')")
        print("  print(f'Đáp án: {answer}')")
            
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        print("\n💡 Hướng dẫn khắc phục:")
        print("1. Kiểm tra file data/key.json có chứa 'gemini_api' không")
        print("2. Kiểm tra API key có đúng không")
        print("3. Kiểm tra kết nối internet")