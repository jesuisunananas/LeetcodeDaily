from email.message import EmailMessage
import os
from pathlib import Path
import smtplib
from jinja2 import Environment, FileSystemLoader

class Gmail_Mailer:
    def __init__(self):
        self.sender_email = os.environ.get("SMTP_EMAIL")
        self.sender_pass = os.environ.get("SMTP_PASS")
        self.recipient_email = os.environ.get("RECIPIENT_EMAIL")

    def fill_and_send_email_template(self, links_for_problems):
        BASE_DIR = Path(__file__).resolve().parent
        TEMPLATES_DIR = BASE_DIR / "templates"
        env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
        template = env.get_template('email_template.j2')

        data_to_fill = {}
        problems = []
        for title, url in links_for_problems:
            problems.append({"title" : title, "url" : url})
        data_to_fill["problems"] = problems

        html_content = template.render(data_to_fill)

        msg = EmailMessage()
        msg["Subject"] = "Daily Leetcode Problems"
        msg["From"] = self.sender_email
        msg["To"] = self.recipient_email

        msg.set_content("Hello! Please open this email in a client that supports HTML.")
        msg.add_alternative(html_content, subtype='html')

        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_pass)
                server.send_message(msg)
        except Exception as e:
            print(f"Message unable to send: {e}")