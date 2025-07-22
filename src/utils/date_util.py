import re
from typing import List, Union

class DateUtil:
    @staticmethod
    def clean_month_label(label: Union[str, None], fmt: str = "short") -> str:
        """
        Chuẩn hóa nhãn tháng từ chuỗi như "As of Apr 2025"
        :param label: chuỗi đầu vào
        :param fmt: 'short' → "Apr-25", 'long' → "April 2025"
        :return: chuỗi chuẩn hóa
        """
        if not isinstance(label, str):
            return ""

        match = re.search(r"As of (\w+)\s+(\d{4})", label)
        if match:
            month = match.group(1)
            year = match.group(2)
            if fmt == "short":
                return f"{month[:3]}-{year[-2:]}"
            else:
                return f"{month} {year}"
        return label.strip()

    @staticmethod
    def clean_month_list(raw_list: List[Union[str, None]], fmt: str = "short") -> List[str]:
        """
        Chuẩn hóa toàn bộ danh sách nhãn tháng
        """
        return [DateUtil.clean_month_label(item, fmt) for item in raw_list]
