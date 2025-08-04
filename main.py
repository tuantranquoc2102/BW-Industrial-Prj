import os
import re
import pandas as pd
# from src.reader import extract_data, extract_loan_data
from src.trend_analysis import to_numeric, get_trends_with_headers
from src.comparator import compare_trends, compare_trends_named
# from src.writer import write_summary_full_trends
from src.rules.investmentPropertiesDepreciationTrend import investmentPropertiesDepreciationRule
from src.rules.loan_balance import LoanInterestTrendRule


if __name__ == '__main__':
    base_dir = os.getcwd()  # thư mục hiện tại
    rule_dir = os.path.join(base_dir, "rules", "Investment_Properties_Depreciation_Trend")

    # Khởi tạo rule
    rule = investmentPropertiesDepreciationRule(
        data_dir=os.path.join(base_dir, "data"),
        rule_dir=rule_dir
    )
    rule.run()

    # rule = LoanInterestTrendRule(
    #     data_dir='data',
    #     rule_dir='rules/Loan Balance Interest Trend'
    # )
    # rule.run()