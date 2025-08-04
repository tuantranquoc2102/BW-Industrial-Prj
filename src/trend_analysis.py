import pandas as pd

def to_numeric(series):
    return pd.to_numeric(series, errors='coerce').ffill().fillna(0)

# def get_trends(series):
#     values = to_numeric(series)
#     trends = []
#     for i in range(1, len(values)):
#         if values[i] > values[i - 1]:
#             trends.append("↑")
#         elif values[i] < values[i - 1]:
#             trends.append("↓")
#         else:
#             trends.append("→")
#     return trends

def get_trends_with_headers(series, month_headers):
    # values = pd.to_numeric(series, errors='coerce').ffill().fillna(0)
    values = pd.to_numeric(series, errors='coerce').ffill().fillna(0).to_numpy()

    trends = []
    for i in range(1, len(values)):
        if values[i] > values[i - 1]:
            trends.append("↑")
        elif values[i] < values[i - 1]:
            if values[i] == 0:
                trends.append("0")
            else:
                trends.append("↓")
        else:
            if values[i] == 0:
                trends.append("0")
            else:
                trends.append("→")
    print(f"📈 Xu hướng: {trends}")
    return trends, month_headers[1:]