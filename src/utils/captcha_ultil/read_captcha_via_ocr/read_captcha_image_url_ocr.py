import requests
import pytesseract
import base64
import cv2
from io import BytesIO
from PIL import Image, ImageEnhance, ImageFilter

#=> Step 01: Cấu hình path đến Tesseract-OCR nếu chưa có trong hệ thống
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

#=> Step 02: Lấy captcha từ URL hoặc ảnh base64
# Tải ảnh từ URL
url = "https://online.acb.com.vn/acbib/Captcha.jpg"

response = requests.get(url)

# Đảm bảo request thành công
if response.status_code == 200:
    img = Image.open(BytesIO(response.content))
    img.show()  # xem ảnh nếu cần
else:
    print("Failed to download captcha:", response.status_code)

#=> Step 03: Tiền xử lý ảnh (nâng cao độ chính xác)
img = img.convert("L")  # chuyển sang grayscale
img = img.filter(ImageFilter.MedianFilter())
enhancer = ImageEnhance.Contrast(img)
img = enhancer.enhance(2)

# Dùng pytesseract để nhận diện CAPTCHA
captcha_text = pytesseract.image_to_string(
    img,
    config='--psm 8 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
)

# Giải captcha
captcha_text = captcha_text.strip()
print("Captcha OCR:", captcha_text)
