import pandas as pd

def compare_trends(bs_trends, pl_trends):
    differences = []
    for i in range(min(len(bs_trends), len(pl_trends))):
        if bs_trends[i] != pl_trends[i]:
            differences.append({
                "Tháng": f"T{i+2}",
                "BS trend": bs_trends[i],
                "PL trend": pl_trends[i]
            })
    return pd.DataFrame(differences)

def compare_trends_named(trend1, trend2, headers, label1="Trend A", label2="Trend B"):
    diffs = []
    for i in range(min(len(trend1), len(trend2))):
        if trend1[i] != trend2[i]:
            diffs.append({
                "Tháng": headers[i],
                label1: trend1[i],
                label2: trend2[i]
            })
    return pd.DataFrame(diffs)