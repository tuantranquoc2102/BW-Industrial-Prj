import requests
import pytesseract
import base64
import cv2
from io import BytesIO
from PIL import Image, ImageEnhance, ImageFilter

#=> Step 01: Cấu hình path đến Tesseract-OCR nếu chưa có trong hệ thống
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

#=> Step 02: Lấy captcha từ URL hoặc ảnh base64
#--- Xử lý captcha từ URL captcha Image (ACB) ---
# Tải ảnh từ URL
url = "https://online.acb.com.vn/acbib/Captcha.jpg"

response = requests.get(url)

# Đảm bảo request thành công
if response.status_code == 200:
    img = Image.open(BytesIO(response.content))
    ###img.show()  # xem ảnh nếu cần
else:
    print("Failed to download captcha:", response.status_code)

#=> Step 03: Tiền xử lý ảnh (nâng cao độ chính xác)
img = img.convert("L")  # chuyển sang grayscale
img = img.filter(ImageFilter.MedianFilter())
enhancer = ImageEnhance.Contrast(img)
img = enhancer.enhance(2)


#--- Xử lý captcha từ ảnh CAPTCHA được mã hóa base64 (MB) ---
# Base64 captcha image
data = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAMgAAAAjCAYAAADR20XfAAAB00lEQVR42u3by2nFMBCFYTeTZfpIP9loGdJP1ikkhYRbgcJdBIzQy5o58us/oI0jMFz0MRrJWRZCCCGEEEIIIYQQQggh5F55Dy/xOfgliCyf4RHTcRYYVwDyEX5i72C17gSj9LcjA7laBalBAMpOQFp42GLtg2QEERFUD+scgMwFAhKAAAQgx+4/AAIQgDROrehBAAKSAhIrju/wFkujNdcDiPII+De8xvU4W5P+CF/xOXLP0udkyd+BeFSOLQt/FEcKJIXhCSUHQgGltvgtR71rBP8Q0mcgGdxueSBpzbNusXIAvIDUEKiAqC4LaxhAMrmK9CCxVI/eHsQDSM+WS1VBPHuOFgCAZHAoq0kPEHWTbqkiac9RGwC5aOWoVRR1FZkBxFJFVM341h7Ee4sFkEEcCiQlIFYcdwLihQQgTkB651iQnAnILCQAAUj0aM5HgFhOsFpAlD2IJxKAHBRIisQDx8xTrBaSWUCsSADi3Id4v3MvIJZ31E6rZl4U5oCMXhgCxIBE+R2WJ441kNonJx7vUR/vbl34o0gAYkAy619uPYGUoKg+YJwBo3fxb5nb+qyEz04OEgUOQgBCCDgIuREGxb0HIZcDAg5CGkD4RQghRJg/2bE+l5tyg/IAAAAASUVORK5CYII="

# Bỏ phần đầu "data:image/png;base64,"
image_data = base64.b64decode(data.split(",")[1])
image = Image.open(BytesIO(image_data))

# Lưu nếu cần debug
# image.save("captcha_debug.png")

# Chuyển sang đen trắng
image = image.convert("L")

# Tăng tương phản, lọc nhiễu, threshold nếu cần
import numpy as np
import cv2

# Convert PIL.Image -> OpenCV image
open_cv_image = np.array(image)
# Áp dụng threshold
_, thresh_img = cv2.threshold(open_cv_image, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

# Chuyển lại về PIL.Image
image = Image.fromarray(thresh_img)




# Dùng pytesseract để nhận diện CAPTCHA
captcha_text = pytesseract.image_to_string(
    image,
    config='--psm 8 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
)

# Giải captcha
captcha_text = captcha_text.strip()
print("Captcha OCR:", captcha_text)
