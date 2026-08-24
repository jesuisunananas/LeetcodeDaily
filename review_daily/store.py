import gspread
import os
import json
from datetime import datetime
from enum import Enum

class LastRecall(Enum):
    HIGH = ("High", 0.9)
    MID = ("Mid", 0.6)
    LOW = ("Low", 0.3)

    def __init__(self, category, mod):
        self.category = category
        self.mod = mod

    @classmethod
    def from_category(cls, category_string):
        for member in cls:
            if member.category == category_string:
                return member
        raise ValueError(f"'{category_string}' is not a valid category")

class Sheets_Store:
    def __init__(self):
        self.credentials = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")

    # retrieve all rows which I can search for problems to give
    # credentials -> rows_to_search
    def get_all_rows_less_than_today(self):
        gc = gspread.service_account_from_dict(json.loads(self.credentials))
        sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/14-OFJtG07B4tu4AtwimBqD-1Fq2XCzJhgvpWMKFuedc/')
        worksheet = sh.get_worksheet(0)
        records = worksheet.get_all_records()[0:151]
        today = datetime.now().date()
        review_problems = []

        for row in records:
            date_str = row.get("Next Review Date")
            if not date_str:
                continue
            target_date = self.convert_date_to_datetime_format(date_str)
            row["Next Review Date"] = target_date
            if (target_date - today).days <= 0:
                review_problems.append(row)

        self.row_format_verification(review_problems)

        return records, review_problems

    # verify formats in rows
    def row_format_verification(self, review_problems):
        for row in review_problems:
            row["ID"] = int(row["ID"])
            row["Link"] = str(row["Link"])
            row["Problem Name"] = str(row["Problem Name"])
            row["NumRecallAttempts"] = int(row["NumRecallAttempts"])
            row["NumConsecutiveRecalls"] = int(row["NumConsecutiveRecalls"])
            row["Last Recall Confidence"] = LastRecall.from_category(row["Last Recall Confidence"])
            row["Last Recall Speed"] = LastRecall.from_category(row["Last Recall Speed"])
            row["Date Reviewed"] = self.convert_date_to_datetime_format(row["Date Reviewed"])

    def convert_date_to_datetime_format(self, date_str):
        current_year = datetime.now().year
        parsed_dt = datetime.strptime(date_str, "%m/%d")
        target_date = parsed_dt.date().replace(year=current_year)
        return target_date
