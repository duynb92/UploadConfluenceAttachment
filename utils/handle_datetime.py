from datetime import datetime


def convert_str_to_datetime(value: str, fmt="%B %Y") -> datetime:
    return datetime.strptime(value, fmt)
