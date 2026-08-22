import gspread
import os
import json
from datetime import datetime
from enum import Enum

class LastRecall(Enum):
    HIGH = "High"
    MID = "Mid"
    LOW = "Low"

# get credentials
def load_credentials():
    credentials = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")
    return credentials

# retrieve all rows which I can search for problems to give
# credentials -> rows_to_search
def get_all_rows_less_than_today(credentials):
    gc = gspread.service_account_from_dict(json.loads(credentials))
    sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/14-OFJtG07B4tu4AtwimBqD-1Fq2XCzJhgvpWMKFuedc/')
    worksheet = sh.get_worksheet(0)
    records = worksheet.get_all_records()[0:151]
    today = datetime.datetime.now().date()
    current_year = datetime.datetime.now().year
    review_problems = []

    for row in records:
        date_str = row.get("Next Review Date")
        if not date_str:
            continue
        parsed_dt = datetime.datetime.strptime(date_str, "%m/%d")
        target_date = parsed_dt.date().replace(year=current_year)
        if (target_date - today).days <= 0:
            review_problems.append(row)

    return records, review_problems

# verify formats in rows
def row_format_verification(review_problems):
    for row in review_problems:
        row["ID"] = int(row["ID"])
        row["Link"] = str(row["Link"])
        row["Problem Name"] = str(row["Problem Name"])
        row["NumRecallAttempts"] = int(row["NumRecallAttempts"])
        row["NumConsecutiveRecalls"] = int(row["NumConsecutiveRecalls"])
        row["Last Recall Confidence"] = LastRecall(row["Last Recall Confidence"])
        row["Last Recall Speed"] = LastRecall(row["Last Recall Speed"])
        row["Next Review Date"] = int(row["Next Review Date"]) # this can be ignored
        row["Date Reviewed"] = int(row["Date Reviewed"]) # this can also be ignored

