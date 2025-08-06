import pandas as pd
pd.set_option('future.no_silent_downcasting', True)
from src.utils.date_util import DateUtil
from src.trend_analysis import get_trends_with_headers
from src.writer import write_summary_full_trends_filtered
from src.conf.config import SHEET_BS, SHEET_PL


class LoanInterestTrendRule:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.bs_df = pd.read_excel(file_path, sheet_name=SHEET_BS, header=None)
        self.pl_df = pd.read_excel(file_path, sheet_name=SHEET_PL, header=None)

        # Chuẩn hóa tiêu đề tháng
        raw_month_headers = self.bs_df.iloc[7, 4:16].tolist()
        self.month_headers = DateUtil.clean_month_list(raw_month_headers, fmt="long")
        self.months = self.month_headers[1:]

    def extract_values(self):
        # Dòng khoản vay
        bs_df_idx = self.bs_df[self.bs_df[0] == "11. Thuế thu nhập hoãn lại phải trả (341)"].index[0]
        self.loan_values = self.bs_df.iloc[bs_df_idx, 4:16]
        
        # 3. PL Breakdown: Xử lý từng mã riêng
        self.pl_code_values = {}  # Dict chứa từng mã và series 12 tháng
        pl_codes = ["635000001", "635000005", "635600001", "635600002"]

        for code in pl_codes:
            matches = self.pl_df[self.pl_df[0].astype(str).str.contains(code)]
            if not matches.empty:
                # values = matches.iloc[0, month_column_indexes].fillna(0)
                # values = matches.iloc[0, 3:15].fillna(0).reset_index(drop=True)
                values = matches.iloc[0, 3:3+12].fillna(0).infer_objects(copy=False)
                values = values.reset_index(drop=True)
            else:
                print(f"⚠️ Không tìm thấy mã {code}, gán mặc định 0.")
                values = pd.Series([0] * 12)

            self.pl_code_values[code] = values

        # 4. Tổng tất cả mã để phân tích
        self.interest_expense_values = sum(self.pl_code_values.values())

    def analyze_trend(self):
        self.loan_trend, _ = get_trends_with_headers(self.loan_values, self.month_headers)
        self.interest_trend, _ = get_trends_with_headers(self.interest_expense_values, self.month_headers)

    def compare_and_write(self):
        write_summary_full_trends_filtered(
            self.file_path,
            trend1=self.loan_trend,
            trend2=self.interest_trend,
            months=self.months,
            rule_name="Rule 2: Loan Balance vs. Interest Expense Trend",
            label1="Loan Balance Trend",
            label2="Interest Expense Trend",
            month_filter_path="src/conf/month_filter.xlsx"  # đường dẫn file filter
        )
       

    def run(self):
        self.extract_values()
        self.analyze_trend()
        self.compare_and_write()
