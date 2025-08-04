import os
import pandas as pd
from src.utils.date_util import DateUtil
from src.trend_analysis import get_trends_with_headers
from src.comparator import compare_trends_named
from src.writer import write_summary_full_trends
from src.conf.config import SHEET_BS, SHEET_PL

class investmentPropertiesDepreciationRule:
    def __init__(self, data_dir: str, rule_dir: str):
        self.data_dir = data_dir      # thư mục chứa các file báo cáo
        self.rule_dir = rule_dir      # thư mục chứa các sub-rules

    def read_account_list(self, file_path):
        with open(file_path, encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip()]
    
    def get_sum_by_accounts(self, df, accounts, col_start=4, col_end=16):
        values = pd.Series([0] * (col_end - col_start))
        for acc in accounts:
            matched = df[df[0].astype(str).str.contains(acc)]
            for _, row in matched.iterrows():
                row_values = matched.iloc[0, col_start:col_end].fillna(0).reset_index(drop=True)
                values += row_values
        return values.reset_index(drop=True)

    def run_sub_rule(self, file_path: str, file_name: str, sub_rule_name: str, sub_rule_path: str):
        print(f"\n📁 File: {file_name} | 🔍 Sub-rule: {sub_rule_name}")

        bs_file = os.path.join(sub_rule_path, 'bs_accounts.txt')
        pl_file = os.path.join(sub_rule_path, 'pl_accounts.txt')

        if not os.path.isfile(bs_file) or not os.path.isfile(pl_file):
            print(f"⚠️ Thiếu file bs_accounts.txt hoặc pl_accounts.txt trong {sub_rule_path}, bỏ qua.")
            return

        # Load dữ liệu từ file Excel
        bs_df = pd.read_excel(file_path, sheet_name=SHEET_BS, header=None)
        pl_df = pd.read_excel(file_path, sheet_name=SHEET_PL, header=None)
        
        # Lấy tiêu đề tháng
        raw_month_headers = bs_df.iloc[7, 4:16].tolist()
        month_headers = DateUtil.clean_month_list(raw_month_headers, fmt="long")
        months = month_headers[1:]  # Bỏ tháng đầu tiên

        # Đọc tài khoản
        bs_accounts = self.read_account_list(bs_file)
        pl_accounts = self.read_account_list(pl_file)

        # Lấy tổng
        # BS: lấy tài khoản từ cột E (index = 4), giá trị từ cột E (4) đến P (16)
        bs_values = self.get_sum_by_accounts(bs_df, bs_accounts, col_start=4, col_end=16)

        # PL: lấy tài khoản từ cột D (index = 3), giá trị từ cột D (3) đến O (15)
        pl_values = self.get_sum_by_accounts(pl_df, pl_accounts, col_start=3, col_end=15)


        print(f"📊 Tổng BS: {bs_values.tolist()}")
        print(f"📊 Tổng PL: {pl_values.tolist()}")

        # Phân tích xu hướng
        bs_trend, _ = get_trends_with_headers(bs_values, month_headers)
        pl_trend, _ = get_trends_with_headers(pl_values, month_headers)

        # Ghi kết quả
        write_summary_full_trends(
            file_path,
            trend1=bs_trend,
            trend2=pl_trend,
            months=months,
            rule_name=f"Rule: {sub_rule_name}",
            label1="BS Trend",
            label2="PL Trend"
        )


    def run(self):
        for file_name in os.listdir(self.data_dir):
            if file_name.startswith('~$') or not file_name.endswith('.xlsx'):
                continue # Bỏ qua file tạm và các file không phải .xlsx

            file_path = os.path.join(self.data_dir, file_name)
            print(f"\n===========================")
            print(f"📄 Đang xử lý file: {file_name}")
            print(f"===========================")

            for sub_rule_name in os.listdir(self.rule_dir):
                sub_rule_path = os.path.join(self.rule_dir, sub_rule_name)
                if os.path.isdir(sub_rule_path):
                    self.run_sub_rule(file_path, file_name, sub_rule_name, sub_rule_path)