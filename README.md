<img width="957" height="567" alt="Screenshot 2026-08-24 at 3 09 11 PM" src="https://github.com/user-attachments/assets/67fa2237-71b8-4549-8cee-5c40c2cdef69" />

Motivation: This project really stemmed from problem fatigue while I was doing leetcode problems, I would find myself doing 10+ problems and then the next day I wouldn't do any. This was really built to integrate Leetcode as a daily, easily repeatable habit.

System Design:  
[ Sheets API ] (using sheets.py)  
      |  
      v  
[Ranking Logic] (using ranking.py)  
      |  
      v  
 [Mail Logic] (using mailer.py)  

This system pulls rows from a sheets document, then ranks n previously reviewed problems and pulls m new problems. The n+m problems are sent over smtp, I fill out a jinja template with the links.

Next Steps:
 - Make a feedback loop using some sort of google form rather than manually updating the google sheet
 - Webhook for status updates in Discord/Slack
 - Possibly add support for different database sources and mail
 - Add support for multiple users by collecting emails to a database and linking problems to users
