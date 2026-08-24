from email.message import EmailMessage
import os
import smtplib
from jinja2 import Environment, FileSystemLoader

class Gmail_Mailer:
    def __init__(self):
        self.sender_email = os.environ.get("SMTP_EMAIL")
        self.sender_pass = os.environ.get("SMTP_PASS")
        self.recipient_email = os.environ.get("RECIPIENT_EMAIL")

    def fill_and_send_email_template(self, links_for_problems):
        env = Environment(loader=FileSystemLoader('.'))
        template = env.get_template('email_template.j2')

        data_to_fill = {}
        for i in range(len(links_for_problems)):
            problem_number = f"problem_{i}"
            data_to_fill[problem_number] = links_for_problems[i]

        html_content = template.render(data_to_fill)

        msg = EmailMessage()
        msg["Subject"] = "Daily Leetcode Problems"
        msg["From"] = self.sender_email
        msg["To"] = self.recipient_email

        msg.set_content("Hello! Please open this email in a client that supports HTML.")
        msg.add_alternative(html_content, subtype='html')

        try:
            with smtplib.SMTP("://gmail.com", 587) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_pass)
                server.send_message(msg)
        except Exception as e:
            print(f"Message unable to send: {e}")