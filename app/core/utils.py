import re
from typing import Optional
from datetime import datetime, timedelta


def format_datetime_local(dt_str: str | None) -> str:
    if not dt_str:
        return "Não informado"

    try:
        dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
        dt_local = dt - timedelta(hours=3)  # Brasil UTC-3
        return dt_local.strftime("%d/%m/%Y %H:%M")
    except Exception:
        return dt_str

def normalize_text(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None

    cleaned = " ".join(value.strip().split())
    return cleaned or None


def normalize_name(value: Optional[str]) -> Optional[str]:
    value = normalize_text(value)
    if not value:
        return None

    return " ".join(word.capitalize() for word in value.split())


def normalize_city(value: Optional[str]) -> Optional[str]:
    value = normalize_text(value)
    if not value:
        return None

    return " ".join(word.capitalize() for word in value.split())


def normalize_size(value: Optional[str]) -> Optional[str]:
    value = normalize_text(value)
    if not value:
        return None

    return value.upper()


def normalize_gender(value: Optional[str]) -> Optional[str]:
    value = normalize_text(value)
    if not value:
        return None

    return value.capitalize()


def normalize_phone(value: Optional[str]) -> Optional[str]:
    value = normalize_text(value)
    if not value:
        return None

    digits = re.sub(r"\D", "", value)
    return digits or None


def normalize_money(value: Optional[str]) -> float:
    value = normalize_text(value)
    if not value:
        return 0.0

    value = value.replace(",", ".")
    try:
        return float(value)
    except ValueError:
        return 0.0


def normalize_int(value: Optional[str]) -> int:
    value = normalize_text(value)
    if not value:
        return 0

    try:
        return int(value)
    except ValueError:
        return 0