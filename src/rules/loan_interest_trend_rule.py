import pandas as pd
from src.utils.date_util import DateUtil
from src.trend_analysis import get_trends_with_headers
from src.writer import write_summary_full_trends


class LoanInterestTrendRule:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.bs_df = pd.read_excel(file_path, sheet_name="BSbreakdown", header=None)
        self.pl_df = pd.read_excel(file_path, sheet_name="PL Breakdown", header=None)

        # Chuẩn hóa tiêu đề tháng
        raw_month_headers = self.bs_df.iloc[7, 4:16].tolist()
        self.month_headers = DateUtil.clean_month_list(raw_month_headers, fmt="long")
        self.months = self.month_headers[1:]

    def extract_values(self):
        # Dòng khoản vay
        short_term_idx = self.bs_df[self.bs_df[0] == "10. Vay và nợ thuê tài chính ngắn hạn (320)"].index[0]
        long_term_idx = self.bs_df[self.bs_df[0] == "8. Vay và nợ thuê tài chính dài hạn (338)"].index[0]
        interest_idx = self.pl_df[self.pl_df[0] == "515100001 - Financial Income: Interest"].index[0]

        # Lấy dữ liệu
        short_term_loan = self.bs_df.iloc[short_term_idx, 4:16]
        long_term_loan = self.bs_df.iloc[long_term_idx, 4:16]

        self.loan_values = short_term_loan.fillna(0) + long_term_loan.fillna(0)
        self.interest_income_values = self.pl_df.iloc[interest_idx, 3:15]

    def analyze_trend(self):
        self.loan_trend, _ = get_trends_with_headers(self.loan_values, self.month_headers)
        self.interest_trend, _ = get_trends_with_headers(self.interest_income_values, self.month_headers)

    def compare_and_write(self):
        write_summary_full_trends(
            self.file_path,
            trend1=self.loan_trend,
            trend2=self.interest_trend,
            months=self.months,
            rule_name="Rule 2: Loan vs Interest Income Trend",
            label1="Loan Trend",
            label2="Interest Income Trend"
        )

    def run(self):
        self.extract_values()
        self.analyze_trend()
        self.compare_and_write()
