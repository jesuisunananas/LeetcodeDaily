from store import Sheets_Store
from ranking import rank_questions, first_n_new
from mailer import Gmail_Mailer

def main():
    sheet_store = Sheets_Store()
    records, review_problems = sheet_store.get_all_rows_less_than_today()
    review_p = rank_questions(review_problems, 3)
    new_p = first_n_new(records, 2)
    links = gather_links(review_p, new_p, records)
    gmail_mailer = Gmail_Mailer()
    gmail_mailer.fill_and_send_email_template(links)

def gather_links(review_p, new_p, records):
    links = []
    for p in review_p:
        links.append((records[p[1] - 1]["Problem Name"], records[p[1] - 1]["Link"]))
    for p in new_p:
        links.append((p["Problem Name"],p["Link"]))

    return links

if __name__ == "__main__":
    main()
