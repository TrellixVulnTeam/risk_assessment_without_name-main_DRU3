"""General Utility Module"""
from __future__ import annotations

import datetime

BRC_GRADE_RANKING = {"aa+": 1, "aa": 2, "a": 3, "b+": 4, "b": 5, "c+": 6, "c": 7, "d+": 8, "d": 9}

def score_ranking(current_score, previous_score, format_type):
    if format_type == "BRC":
        if BRC_GRADE_RANKING[current_score] > BRC_GRADE_RANKING[previous_score]:
            return False

def check_date(date):
    current_date = datetime.date.today()
    print(date, current_date)
    if current_date < date:
        return True

