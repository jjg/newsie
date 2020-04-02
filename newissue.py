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
#newspaper_html = "<h1>The Daily Facto</h1>"
newspaper_body = ""

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
        newspaper_body += "<br>"
        newspaper_body += f"<b>{entry['title']}</b>"
        
        # Insert summary
        newspaper_body += f"<p>{entry['summary']}</p>"

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
        newspaper_body += f"<img src='/home/jason/Development/paperboy/img/{entry_idx}.jpg'>"

        entry_idx = entry_idx + 1

paper_title = "Daily Paperboy"
publication_date = "Monday, April 1st 2020"
newspaper_html = f"""
<!DOCTYPE html>
<html>
    <head>
        <title>{paper_title}</title>
        <meta charset='utf-8'>
        <meta name="viewport" content="width=1024px; initial-scale=1.0;">
        <link rel="stylesheet" href="/home/jason/Development/paperboy/css/reset.css" media="all" />
        <link rel="stylesheet" href="/home/jason/Development/paperboy/css/multi-col.css" media="all" />
    </head>
    <body>
        <section>
            <header>
                <h1><span>{publication_date}</span>{paper_title}</h1>
                <h2><span>something?</span></h2>
            </header>

            <article class="cols">
                {newspaper_body}
            </article>

        </section>
    </body>
</html>
"""

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
