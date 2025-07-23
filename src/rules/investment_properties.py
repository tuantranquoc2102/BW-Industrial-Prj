import pandas as pd
from src.utils.date_util import DateUtil
from src.trend_analysis import get_trends_with_headers
from src.comparator import compare_trends_named
from src.writer import write_summary_full_trends
from src.conf.config import SHEET_BS, SHEET_PL

class DepreciationTrendRule:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.bs_df = pd.read_excel(file_path, sheet_name=SHEET_BS, header=None)
        self.pl_df = pd.read_excel(file_path, sheet_name=SHEET_PL, header=None)

        # Chuẩn hóa header tháng
        raw_month_headers = self.bs_df.iloc[7, 4:16].tolist()
        self.month_headers = DateUtil.clean_month_list(raw_month_headers, fmt="long")
        self.months = self.month_headers[1:]  # Bỏ tháng đầu tiên để so sánh từ tháng 2

    def extract_values(self):
        # 1. BS Breakdown: Lấy giá trị từ dòng "- Nguyên giá (231)"
        bs_row_idx = self.bs_df[self.bs_df[0] == "- Nguyên giá (231)"].index[0]
        self.bs_values = self.bs_df.iloc[bs_row_idx, 4:16]
        print(f"📊 Tổng BS Breakdown: {self.bs_values.tolist()}")

        # 2. Xác định 12 cột tháng từ dòng tiêu đề (row 8 - index 7), bắt đầu từ cột D (index=3)
        raw_month_headers = self.pl_df.iloc[7, 3:15]
        month_column_indexes = raw_month_headers.index.tolist()
        print(f"📅 Các tháng: {raw_month_headers.tolist()}")

        # 3. PL Breakdown: Xử lý từng mã riêng
        self.pl_code_values = {}  # Dict chứa từng mã và series 12 tháng
        pl_codes = ["632100001", "632100002", "632100003", "632100004", "632100005", "632100017"]

        for code in pl_codes:
            matches = self.pl_df[self.pl_df[0].astype(str).str.contains(code)]
            if not matches.empty:
                # values = matches.iloc[0, month_column_indexes].fillna(0)
                values = matches.iloc[0, 3:15].fillna(0).reset_index(drop=True)
            else:
                print(f"⚠️ Không tìm thấy mã {code}, gán mặc định 0.")
                values = pd.Series([0] * 12)

            self.pl_code_values[code] = values

        # 4. Tổng tất cả mã để phân tích
        self.pl_values = sum(self.pl_code_values.values())
        #self.pl_values = sum(self.pl_code_values.values()).reset_index(drop=True)

        print(f"📊 Tổng PL Breakdown: {self.pl_values.tolist()}")

    def analyze_trend(self):
        # Tính xu hướng từng bên
        self.bs_trend, _ = get_trends_with_headers(self.bs_values, self.month_headers)
        self.pl_trend, _ = get_trends_with_headers(self.pl_values, self.month_headers)

    def compare_and_write(self):
        # Ghi trực tiếp toàn bộ xu hướng theo tháng, đánh màu khác biệt
        write_summary_full_trends(
            self.file_path,
            trend1=self.bs_trend,
            trend2=self.pl_trend,
            months=self.months,
            rule_name="Rule 1: Investment Properties vs. Depreciation Trend",
            label1="Investment Properties Trend",
            label2="Depreciation Trend"
        )

    def run(self):
        self.extract_values()
        self.analyze_trend()
        self.compare_and_write()
