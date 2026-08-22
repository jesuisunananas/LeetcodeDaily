import gspread
import os
import json
from datetime import datetime

def load_credentials():
    credentials = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")
    return credentials

def get_all_rows_less_than_today(credentials):
    gc = gspread.service_account_from_dict(json.loads(credentials))
    sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/14-OFJtG07B4tu4AtwimBqD-1Fq2XCzJhgvpWMKFuedc/edit?gid=0#gid=0')
    worksheet = sh.get_worksheet(0)
    records = worksheet.get_all_records()
    today = datetime.now().date()
    current_year = today.year
    matching_rows = [] #[row for row in records if row.get("Next Review Date") <= target_date]
    for row in records:
        