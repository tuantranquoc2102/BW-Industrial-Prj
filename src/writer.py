import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import PatternFill
from calendar import month_abbr
from openpyxl.styles import PatternFill, Alignment


def write_summary_full_trends(file_path, trend1, trend2, months, rule_name="Rule", label1="BS trend", label2="PL trend"):

    # Rule row + 2 dòng trend
    header_row = [rule_name] + months
    row1 = [label1] + trend1
    row2 = [label2] + trend2

    # Load workbook
    book = load_workbook(file_path)
    if "Anomalies Summary" in book.sheetnames:
        sheet = book["Anomalies Summary"]
        start_row = sheet.max_row + 2
    else:
        sheet = book.create_sheet("Anomalies Summary")
        start_row = 1

    # Ghi các dòng header_row, trend1, trend2
    rows = [header_row, row1, row2]
    for row_offset, row_data in enumerate(rows, start=1):
        for col_idx, val in enumerate(row_data, start=1):
            cell = sheet.cell(row=start_row + row_offset, column=col_idx, value=val)

            # Canh giữa nội dung trong ô
            cell.alignment = Alignment(horizontal="center", vertical="center")

            # Tô màu khác biệt (chỉ từ cột thứ 2 trở đi)
            if row_offset in [1, 2] and col_idx > 1:
                idx = col_idx - 2
                if idx < len(trend1) and trend1[idx] != trend2[idx]:
                    cell.fill = PatternFill(start_color="FFCCCB", end_color="FFCCCB", fill_type="solid")

    book.save(file_path)