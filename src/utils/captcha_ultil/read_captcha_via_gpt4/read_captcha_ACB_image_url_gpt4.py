import os
import openai
import requests
import base64
import tempfile
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv


# === Load API key từ .env ===
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("❌ OPENAI_API_KEY not found in .env file!")

openai.api_key = OPENAI_API_KEY

CAPTCHA_URL = "https://online.acb.com.vn/acbib/Captcha.jpg"

def download_and_preview_image(url: str) -> tuple[str, str]:
    print(f"[+] Đang tải ảnh từ: {url}")
    response = requests.get(url)
    response.raise_for_status()

    # Dùng PIL mở ảnh
    image = Image.open(BytesIO(response.content))

    # Hiển thị ảnh
    image.show(title="CAPTCHA Image")

    # Mã hóa base64
    encoded = base64.b64encode(response.content).decode("utf-8")
    mime_type = Image.MIME.get(image.format, "image/jpeg")
    return f"data:{mime_type};base64,{encoded}", mime_type

def image_url_to_base64_data_uri(url: str) -> str:
    """
    Tải ảnh từ URL và mã hóa base64 thành dạng data URI.
    """
    print(f"[+] Đang tải ảnh từ: {url}")
    response = requests.get(url)
    response.raise_for_status()
    encoded = base64.b64encode(response.content).decode("utf-8")
    return f"data:image/jpeg;base64,{encoded}"


def read_captcha_with_openai(base64_data_uri: str) -> str:
    """
    Gửi ảnh đến GPT-4 Vision để phân tích và đọc ký tự trong CAPTCHA.
    """
    print("[+] Đang gửi ảnh đến GPT-4 Vision...")
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that can read CAPTCHA images."
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "What characters are shown in this CAPTCHA image? Return only the text."},
                    {"type": "image_url", "image_url": {"url": base64_data_uri}}
                ]
            }
        ],
        max_tokens=10,
        temperature=0
    )

    captcha_text = response.choices[0].message.content.strip()
    return captcha_text


def main():
    try:
        base64_data_uri, mime = download_and_preview_image(CAPTCHA_URL)
        result = read_captcha_with_openai(base64_data_uri)
        print(f"[✅] Kết quả CAPTCHA: {result}")
    except Exception as e:
        print("[❌] Lỗi xảy ra:", str(e))


if __name__ == "__main__":
    main()
