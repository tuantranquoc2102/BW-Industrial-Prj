from src.reader import extract_data, extract_loan_data
from src.trend_analysis import get_trends, to_numeric, get_trends_with_headers
from src.comparator import compare_trends, compare_trends_named
from src.writer import write_summary_full_trends
import pandas as pd
import re
from src.rules.investment_properties import DepreciationTrendRule
from src.rules.loan_balance import LoanInterestTrendRule


file_path = "data/DAL_May'25_example.xlsx"  # 🔁 Cập nhật đường dẫn nếu khác

rule1 = DepreciationTrendRule(file_path)
rule1.run()

rule2 = LoanInterestTrendRule(file_path)
rule2.run()

print("✅ Đã xử lý và ghi kết quả vào sheet 'Summary Report'")
