import os
import smtplib
import glob 

import feedparser
import pydf
import qrcode

from email.message import EmailMessage

from config import config

# TODO: Load subscriber from some datasource
subscriber_printer_email = config["debug_email"]
subscriber_blocklist = ""
subscriber_feeds = [
        "https://hackaday.com/feed",
        ]

# Render each article into html
column_text = ["",""]

for feed_url in subscriber_feeds:

    # Load RSS feed
    feed = feedparser.parse(feed_url)

    # TODO: Filter articles more than 24 hours old (entry["published"])
    # TODO: Filter through subscriber blocklist
    # TODO: Strip html, hyperlinks, etc.
    # TODO: Randomly select enough to fill 2 pages

    entry_idx = 0
    for entry in feed.entries:

        # Insert headline
        # TODO: Replace this variable with a better name
        newspaper_body = ""
        newspaper_body += f"<h2>{entry['title']}</h2>"
        

        # TODO: Consider grabbing more of the article if the summary is short.

        # Insert QR code link to source
        qr_link = qrcode.QRCode(
                version = 10,
                box_size = 1,
                border = 4,
                )
        qr_link.add_data(entry["link"])
        qr_link.make(fit=False)
        qr_link_img = qr_link.make_image(fill_color="black",back_color="white")
        qr_link_img.save(f"./img/{entry_idx}.jpg", "JPEG")

        # TODO: Full path required here, but find a way to 
        # avoid hard-coding it.
        # TODO: Align this better, perhaps alternate left/right?
        newspaper_body += f"<img align='left' src='/home/jason/Development/paperboy/img/{entry_idx}.jpg'>"

        # Insert summary
        newspaper_body += f"<p>{entry['summary']}</p>"

        column_text[(entry_idx % 2)] += newspaper_body

        entry_idx = entry_idx + 1

# TODO: Make this part of the config
paper_title = "The Cyber Gazzette"

newspaper_html = f"""
<table width=100% border=0>
   <tr><th colspan=2><h1>{paper_title}</h1></th></tr>
   <tr><td>{column_text[0]}</td><td>{column_text[1]}</td></tr>
</table>
"""

# Create new PDF
newspaper_pdf = pydf.generate_pdf(newspaper_html)

# Send to printer
message = EmailMessage()
message["Subject"] = "Extree! Extree!"
message["From"] = config["email"]
message["To"] = subscriber_printer_email
message.set_content("Latest edition attached!")
message.add_attachment(newspaper_pdf, maintype="application/pdf", subtype="pdf")

smtp = smtplib.SMTP(f"{config['smtp_server']}:{config['smtp_port']}")
smtp.ehlo()
smtp.starttls()
smtp.login(config["email"], config["password"])
smtp.send_message(message)
smtp.quit()

# Clean-up temp files
for f in glob.glob("./img/*"):
    os.remove(f)
