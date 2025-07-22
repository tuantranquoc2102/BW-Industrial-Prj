import pandas as pd

# Extract data from BS Breakdown and PL Breakdown sheets
# Returns two pandas Series: one for BS values and one for PL values
def extract_data(file_path):
    bs_df = pd.read_excel(file_path, sheet_name="BSbreakdown", header=None)
    pl_df = pd.read_excel(file_path, sheet_name="PL Breakdown", header=None)

    bs_row_idx = bs_df[bs_df[0] == "- Nguyên giá (231)"].index[0]
    pl_row_idx = pl_df[pl_df[0] == "632100002 - Expense Depreciation: RBF for lease"].index[0]

    bs_values = bs_df.iloc[bs_row_idx, 4:].reset_index(drop=True)
    pl_values = pl_df.iloc[pl_row_idx, 3:].reset_index(drop=True)

    return bs_values, pl_values

def extract_loan_data(file_path):
    bs_df = pd.read_excel(file_path, sheet_name="BSbreakdown", header=None)
    pl_df = pd.read_excel(file_path, sheet_name="PL Breakdown", header=None)

    # Lấy 2 dòng khoản vay
    short_term_idx = bs_df[bs_df[0] == "10. Vay và nợ thuê tài chính ngắn hạn (320)"].index[0]
    long_term_idx = bs_df[bs_df[0] == "8. Vay và nợ thuê tài chính dài hạn (338)"].index[0]

    # Trích xuất dữ liệu ngắn hạn và dài hạn từ cột E
    short_term = bs_df.iloc[short_term_idx, 4:].reset_index(drop=True)
    long_term = bs_df.iloc[long_term_idx, 4:].reset_index(drop=True)

    # Lấy dòng interest income từ PL Breakdown
    interest_income_idx = pl_df[pl_df[0] == "515100001 - Financial Income: Interest"].index[0]
    interest_income = pl_df.iloc[interest_income_idx, 3:].reset_index(drop=True)

    return short_term, long_term, interest_income
