import os
import openai
import base64
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv


# === Load API key từ .env ===
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("❌ OPENAI_API_KEY not found in .env file!")

openai.api_key = OPENAI_API_KEY

BASE64_IMAGE = """
data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAMgAAAAjCAYAAADR20XfAAABrUlEQVR42u3a0W3DIBRG4Tx3jg6Sp05QqauwRVeJ1IU6Qxeg8kNUZFF8DT8XsM6ReEksS434BNS+3YiIiIiIiIiIiIiIiPK9hZ+4DX4JY1/hHq1jxb/vNXzGbSjv+REeMR2Sm4aXWD1OwABIJxwA+YPxHxY5FMV1CRBWkAogVkQr41AAKSHohkR1HVusPjhWBpLiUAGpBdQNyPNagIzfhq0IRLXFsk5+gIBjKRwjgEiQVGydAAKQqkM5QAAyPZD38B23kfts/7n1e8vqcVkgDXhyQPgX8CAc6SRPJ/r+86PvrEhyEJRA3A7qJSCNq0uKYA8DKIO2V+kkL60kNStNCYcKiHXyy4E0PhwsAckBAMhJIKp7WbdTZ7ZoVgRqIEcPC1daQTinTHI4bwVgAVKDRwHlCcL1OYgTEJBcAMjR5O/xLlbX7dUEQFhFHLdXHkDOjqlxCLZRAFlo9QAIQAAy+AwycoslxzEREDQ4bK+uDKQLjgmAsHo4rh5XBCJ/vX1CIGgAyNw4OiEpPQxk5Rh09qh9raTltRMlkO4ocjCcoQCDiIiIiIiIiIiIiBz6BezlZ1tEt99JAAAAAElFTkSuQmCC
""".strip()


def extract_base64_data(data_uri: str) -> str:
    """
    Loại bỏ tiền tố data:image/... và lấy phần base64
    """
    if "," in data_uri:
        return data_uri.split(",")[1]
    return data_uri


def show_image(base64_data: str):
    """
    Hiển thị ảnh base64 bằng Pillow
    """
    image_data = base64.b64decode(base64_data)
    image = Image.open(BytesIO(image_data))
    image.show(title="CAPTCHA")
    return image_data  # trả về raw bytes để encode lại nếu cần


def send_to_gpt4(base64_data: bytes, mime_type="image/png") -> str:
    """
    Gửi ảnh base64 đến GPT-4o để nhận diện ký tự trong CAPTCHA
    """
    data_uri = f"data:{mime_type};base64,{base64.b64encode(base64_data).decode('utf-8')}"
    
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that can read CAPTCHA images."},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "What characters are shown in this CAPTCHA image? Return only the text."},
                    {"type": "image_url", "image_url": {"url": data_uri}},
                ],
            }
        ],
        max_tokens=10,
        temperature=0
    )
    return response.choices[0].message.content.strip()


def main():
    try:
        base64_data = extract_base64_data(BASE64_IMAGE)
        raw_bytes = show_image(base64_data)
        result = send_to_gpt4(raw_bytes)
        print(f"[✅] CAPTCHA Result: {result}")
    except Exception as e:
        print("[❌] Lỗi xảy ra:", e)


if __name__ == "__main__":
    main()
