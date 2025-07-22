import pandas as pd
from src.utils.date_util import DateUtil
from src.trend_analysis import get_trends_with_headers
from src.comparator import compare_trends_named
from src.writer import write_summary_full_trends


class DepreciationTrendRule:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.bs_df = pd.read_excel(file_path, sheet_name="BSbreakdown", header=None)
        self.pl_df = pd.read_excel(file_path, sheet_name="PL Breakdown", header=None)

        # Chuẩn hóa header tháng
        raw_month_headers = self.bs_df.iloc[7, 4:16].tolist()
        self.month_headers = DateUtil.clean_month_list(raw_month_headers, fmt="long")
        self.months = self.month_headers[1:]  # Bỏ tháng đầu tiên để so sánh từ tháng 2

    def extract_values(self):
        # Lấy index dòng cần đọc
        bs_row_idx = self.bs_df[self.bs_df[0] == "- Nguyên giá (231)"].index[0]
        pl_row_idx = self.pl_df[self.pl_df[0] == "632100002 - Expense Depreciation: RBF for lease"].index[0]

        # Lấy giá trị từng tháng
        self.bs_values = self.bs_df.iloc[bs_row_idx, 4:16]
        self.pl_values = self.pl_df.iloc[pl_row_idx, 3:15]

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
            rule_name="Rule 1: Depreciation Trend",
            label1="BS trend",
            label2="PL trend"
        )

    def run(self):
        self.extract_values()
        self.analyze_trend()
        self.compare_and_write()
