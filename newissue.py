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
subscriber_blacklist = ""
subscriber_feeds = [
        "https://feeds.bbci.co.uk/news/rss.xml",
        "https://hackaday.com/feed",
        ]


# Render each article into html
# TODO: Apply style to html
newspaper_html = "<h1>The Daily Facto</h1>"

for feed_url in subscriber_feeds:

    # Load RSS feed
    feed = feedparser.parse(feed_url)

    # TODO: Filter articles more than 24 hours old (entry["published"])
    # TODO: Filter through subscriber blacklist
    # TODO: Strip html, hyperlinks, etc.
    # TODO: Randomly select enough to fill 2 pages

    entry_idx = 0
    for entry in feed.entries:

        # Insert headline
        newspaper_html += "<hr>"
        newspaper_html += f"<h2>{entry['title']}</h2>"
        
        # Insert summary
        newspaper_html += f"<p>{entry['summary']}</p>"

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
        newspaper_html += f"<img src='/home/jason/Development/paperboy/img/{entry_idx}.jpg'>"

        entry_idx = entry_idx + 1

# Create new PDF
newspaper_pdf = pydf.generate_pdf(newspaper_html)

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

# Clean-up temp files
for f in glob.glob("./img/*"):
    os.remove(f)
