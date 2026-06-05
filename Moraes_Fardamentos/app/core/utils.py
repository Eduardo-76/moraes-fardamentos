from datetime import datetime


def now_str() -> str:
    return datetime.now().strftime('%d/%m/%Y %H:%M')
