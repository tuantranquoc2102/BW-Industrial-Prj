import pandas as pd

def to_numeric(series):
    return pd.to_numeric(series, errors='coerce').ffill().fillna(0)


def get_trends_with_headers(series, month_headers):
    # values = pd.to_numeric(series, errors='coerce').ffill().fillna(0)
    values = pd.to_numeric(series, errors='coerce').ffill().fillna(0).to_numpy()

    trends = []
    for i in range(1, len(values)):
        prev = values[i - 1]
        curr = values[i]

        # Xử lý chia cho 0
        if prev >= 0 and curr == 0:
            trends.append("0")  # hoặc '→' tùy yêu cầu
            continue
        elif prev == 0 and curr > 0:
            trends.append("↑ >5%")  # hoặc '→' tùy yêu cầu
            continue
        else:
            change_percent = (curr - prev) / prev

        if change_percent >= 0.05:
            trends.append("↑ >5%")
        elif 0 < change_percent < 0.05:
            trends.append("↑")
        elif change_percent <= -0.05:
            trends.append("↓ >5%")
        elif -0.05 < change_percent < 0:
            trends.append("↓")
        else:
            trends.append("→")

    print(f"📈 Xu hướng: {trends}")
    return trends, month_headers[1:]