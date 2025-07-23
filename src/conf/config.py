import os
from dotenv import load_dotenv

# Load biến môi trường từ file .env
load_dotenv()

# Lấy giá trị các sheet
SHEET_BS = os.getenv("SHEET_BS", "BS Breakdown")
SHEET_PL = os.getenv("SHEET_PL", "PL Breakdown")