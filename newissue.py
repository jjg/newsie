import smtplib

import feedparser
import pydf

from email.message import EmailMessage

from config import config

# TODO: Load subscriber from some datasource
subscriber_printer_email = config["debug_email"]
subscriber_blacklist = ""
rssfeed = "https://feeds.bbci.co.uk/news/rss.xml"

# Load RSS feed
# TODO: Load multiple feeds
feed = feedparser.parse(rssfeed)

# TODO: Filter articles more than 24 hours old
# TODO: Filter through subscriber blacklist
# TODO: Randomly select enough to fill 2 pages

# Render each article into html
newspaper_html = "<h1>The Daily Facto</h1>"

for entry in feed.entries:

    # Insert headline
    newspaper_html += "<hr>"
    newspaper_html += f"<h2>{entry['title']}</h2>"
    
    # Insert summary
    newspaper_html += f"<p>{entry['summary']}</p>"

    # TODO: Insert QR code link to source

# Create new PDF
newspaper_pdf = pydf.generate_pdf(newspaper_html)

# DEBUG: Write to filesystem
#with open("newspaper.pdf","wb") as f:
#    f.write(newspaper_pdf)

# Send to printer
message = EmailMessage()
message["Subject"] = "Extree! Extree!"
message["From"] = config["email"]
message["To"] = subscriber_printer_email
message.add_attachment(newspaper_pdf, maintype="application/pdf", subtype="pdf")

smtp = smtplib.SMTP(f"{config['smtp_server']}:{config['smtp_port']}")
smtp.ehlo()
smtp.starttls()
smtp.login(config["email"], config["password"])
smtp.send_message(message)
smtp.quit()
