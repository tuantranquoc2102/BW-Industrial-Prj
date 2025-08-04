import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import PatternFill
from calendar import month_abbr
from openpyxl.styles import PatternFill, Alignment, Font


# def write_summary_full_trends(file_path, trend1, trend2, months, rule_name="Rule", label1="BS trend", label2="PL trend"):

#     # Rule row + 2 dòng trend
#     header_row = [rule_name] + months
#     row1 = [label1] + trend1
#     row2 = [label2] + trend2

#     # Load workbook
#     book = load_workbook(file_path)

#     # Xác định vị trí bắt đầu
#     #---TH mà đã có sheet "Anomalies Summary" thì start_row = max_row + 2
#     if "Anomalies Summary" in book.sheetnames:
#         sheet = book["Anomalies Summary"]
#         start_row = sheet.max_row + 2
#     #---TH mà chưa có sheet "Anomalies Summary" thì start_row = 1
#     else:
#         sheet = book.create_sheet("Anomalies Summary")
#         start_row = 1

#     # Colors
#     diff_fill = PatternFill(start_color="FFCCCB", end_color="FFCCCB", fill_type="solid")  # Light red



#     # # Ghi các dòng header_row, trend1, trend2
#     # rows = [header_row, row1, row2]
#     # for row_offset, row_data in enumerate(rows, start=1):
#     #     for col_idx, val in enumerate(row_data, start=1):
#     #         cell = sheet.cell(row=start_row + row_offset, column=col_idx, value=val)

#     #         # Canh giữa nội dung trong ô
#     #         cell.alignment = Alignment(horizontal="center", vertical="center")

#     #         # Tô màu khác biệt (chỉ từ cột thứ 2 trở đi)
#     #         if row_offset in [1, 2] and col_idx > 1:
#     #             idx = col_idx - 2
#     #             if idx < len(trend1) and trend1[idx] != trend2[idx]:
#     #                 cell.fill = diff_fill

#     # Ghi header
#     for col_idx, val in enumerate(header_row, start=1):
#         cell = sheet.cell(row=start_row, column=col_idx, value=val)
#         cell.alignment = Alignment(horizontal="center", vertical="center")

#     # Ghi BS trend & PL trend + tô màu nếu khác nhau
#     for col_idx in range(1, len(months) + 2):  # +2 vì cột 1 là label
#         # Ghi BS trend
#         bs_cell = sheet.cell(row=start_row + 1, column=col_idx,
#                              value=row1[col_idx - 1])
#         bs_cell.alignment = Alignment(horizontal="center", vertical="center")

#         # Ghi PL trend
#         pl_cell = sheet.cell(row=start_row + 2, column=col_idx,
#                              value=row2[col_idx - 1])
#         pl_cell.alignment = Alignment(horizontal="center", vertical="center")

#         # So sánh trend (bỏ cột label)
#         if col_idx > 1:
#             idx = col_idx - 2
#             if idx < len(trend1) and trend1[idx] != trend2[idx]:
#                 bs_cell.fill = diff_fill
#                 pl_cell.fill = diff_fill

#     # Lưu file
#     book.save(file_path)

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

    # Highlight styles
    diff_fill = PatternFill(start_color="FFFFCCCB", end_color="FFFFCCCB", fill_type="solid")
    red_font = Font(color="FF0000")  # Red text

    # Ghi các dòng header_row, trend1, trend2
    rows = [header_row, row1, row2]
    for row_offset, row_data in enumerate(rows, start=1):
        for col_idx, val in enumerate(row_data, start=1):
            cell = sheet.cell(row=start_row + row_offset, column=col_idx, value=val)
            cell.alignment = Alignment(horizontal="center", vertical="center")

            # Tô màu khác biệt nếu là dòng trend1 hoặc trend2 (offset 2 hoặc 3) và từ cột 2 trở đi
            if row_offset in [2, 3] and col_idx > 1:
                idx = col_idx - 2
                if idx < len(trend1) and trend1[idx] != trend2[idx]:
                    cell.fill = diff_fill
                    cell.font = red_font  # tô màu chữ để dễ thấy

    # Lưu file
    book.save(file_path)