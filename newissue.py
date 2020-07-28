import os
import smtplib
import glob 
import re

import feedparser
import pydf
import qrcode
import cups

from email.message import EmailMessage
from datetime import datetime, timedelta, timezone

import config

# This gets rid of most HTML w/o resorting to BeautifulSoup (which we might do at some point)
def clean_html(s):
    cleanr = re.compile('<.*?>')
    clean_text = re.sub(cleanr, '', s)
    return clean_text

# TODO: Load subscriber from some datasource
#subscriber_printer_email = config.subscriber_email
#subscriber_blocklist = set(["coronavirus", "coronavirus:", "trump"])
#subscriber_feeds = [
#        "https://hackaday.com/feed",
#        "http://feeds.bbci.co.uk/news/rss.xml",
#        "https://blog.adafruit.com/feed",
#        "https://feeds.npr.org/1001/rss.xml",
#        ]

articles = []

# Render each article into html
column_text = ["",""]

for feed_url in config.subscriber_feeds:

    # Load RSS feed
    feed = feedparser.parse(feed_url)

    for article in feed.entries:
        yesterday = datetime.now(timezone.utc) - timedelta(days=1)

        # Different feeds specify the TZ with different formats.  This is an attempt
        # to handle that; it's awkward but will do until we find something better
        try:
            article.published_parsed = datetime.strptime(article["published"], "%a, %d %b %Y %H:%M:%S %z")
        except ValueError:
            # Thanks to a bug in strptime (https://bugs.python.org/issue22377), we have to force the TZ on these
            article.published_parsed= datetime.strptime(article["published"], "%a, %d %b %Y %H:%M:%S %Z").replace(tzinfo=timezone.utc)

        if article.published_parsed > yesterday:

            # TODO: Strip html, hyperlinks, etc.
            # Filter out articles containingi keywords the user doesn't want to see
            title_set = set(article["title"].lower().split())
            if config.subscriber_blocklist.intersection(title_set):
                print(f"blocked: {config.subscriber_blocklist.intersection(title_set)} {article['title']}")
            else:
                print(f"added: {article['title']}")
                articles.append(article)

# Sort articles by (parsed) publication date
articles.sort(key=lambda x: x.published_parsed, reverse=False)

article_idx = 0
# TODO: Select enough articles to fill 2 pages instead of just grabbing a fixed number 
for article in articles[-20:]:

    # Insert headline
    # TODO: Replace this variable with a better name
    newspaper_body = ""
    newspaper_body += f"<h2>{article['title']}</h2>"

    # TODO: Consider grabbing more of the article if the summary is short.

    # Insert QR code link to source
    qr_link = qrcode.QRCode(
            version = 10,
            box_size = 1,
            border = 4,
            )
    qr_link.add_data(article["link"])
    qr_link.make(fit=False)
    qr_link_img = qr_link.make_image(fill_color="black",back_color="white")
    qr_link_img.save(f"./img/{article_idx}.jpg", "JPEG")

    # TODO: Full path required here, but find a way to 
    # avoid hard-coding it.
    # TODO: Align this better, perhaps alternate left/right?
    newspaper_body += f"<img align='left' src='/home/jason/Development/paperboy/img/{article_idx}.jpg'>"

    # Insert summary
    newspaper_body += f"<p>{clean_html(article['summary'])}</p>"

    column_text[(article_idx % 2)] += newspaper_body

    article_idx = article_idx + 1


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

# Send to printer via email
message = EmailMessage()
message["Subject"] = "Extree! Extree!"
message["From"] = config.email
message["To"] = config.subscriber_email
message.set_content("Latest edition attached!")
message.add_attachment(newspaper_pdf, maintype="application/pdf", subtype="pdf")

smtp = smtplib.SMTP(f"{config.smtp_server}:{config.smtp_port}")
smtp.ehlo()
smtp.starttls()
smtp.login(config.email, config.password)
smtp.send_message(message)
smtp.quit()

# Print directly to the printer with CUPS
if config.print_direct:
    pdf_file = "./img/issue.pdf"
    with open(pdf_file, "wb") as pf:
        pf.write(newspaper_pdf)

    conn = cups.Connection()
    conn.printFile(config.printer_name, pdf_file, " ", {"sides":"two-sided-long-edge", "fit-to-page":"1"}) 

# Clean-up temp files
for f in glob.glob("./img/*"):
    os.remove(f)
