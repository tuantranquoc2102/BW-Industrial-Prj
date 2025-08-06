import os
import openai, requests, base64
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv


# === Load API key từ .env ===
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("❌ OPENAI_API_KEY not found in .env file!")

openai.api_key = OPENAI_API_KEY

CAPTCHA_URL = "https://corporate-login.vietcombank.com.vn/captcha-public-service/captcha/8d795ddc-3c2c-4a2f-a6fb-b3539aeec025?r_num=5fc3ebb7-3e6f-4c9a-8070-f050026d9d03"


def fetch_and_show(url):
    resp = requests.get(url)
    resp.raise_for_status()
    img = Image.open(BytesIO(resp.content))
    img.show(title="VCB CAPTCHA")
    return resp.content

def solve_vcb_captcha(image_bytes):
    uri = f"data:image/png;base64,{base64.b64encode(image_bytes).decode()}"
    resp = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role":"system", "content":"You are a helpful assistant that reads CAPTCHA."},
            {"role":"user", "content":[
                {"type":"text", "text":"What characters are shown in this CAPTCHA image? Return only the text."},
                {"type":"image_url", "image_url":{"url":uri}}
            ]}
        ],
        max_tokens=10, temperature=0
    )
    return resp.choices[0].message.content.strip()

if __name__=="__main__":
    try:
        img_bytes = fetch_and_show(CAPTCHA_URL)
        result = solve_vcb_captcha(img_bytes)
        print("🚀 CAPTCHA text:", result)
    except Exception as e:
        print("Error:", e)
