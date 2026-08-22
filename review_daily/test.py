import datetime

date_str = "6/27"
parsed_dt = datetime.datetime.strptime(date_str, "%m/%d")
current_year = datetime.datetime.now().year
target_date = parsed_dt.date().replace(year=current_year)
today = datetime.datetime.now().date()
day_difference = (target_date - today).days
print(f"Days difference: {day_difference}")