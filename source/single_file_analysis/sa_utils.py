"""Single File Analysis Utility Module"""
from __future__ import annotations

from datetime import datetime
def cert_day_validator(expiry_date):
    present = datetime.now()
    return datetime(expiry_date) < present