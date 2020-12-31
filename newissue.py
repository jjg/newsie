import os
import smtplib
import glob 
import re

import feedparser
import qrcode
import cups

from email.message import EmailMessage
from datetime import datetime, timedelta, timezone

import config
import generate_pdf

# This gets rid of most HTML w/o resorting to BeautifulSoup (which we might do at some point)
def clean_html(s):
    cleanr = re.compile('<.*?>')
    clean_text = re.sub(cleanr, '', s)
    return clean_text

def send_to_email(newspaper_pdf):
    # Send via email
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

def send_to_printer(newspaper_pdf):
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

def get_weather():
    # TODO: Get weather from weather station
    weather = {"temp": 69, "humidity": 10, "pressure": 50}
    return weather

# Build a list of articles
articles = []

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

            # Filter out articles containing keywords the user doesn't want to see
            title_set = set(article["title"].lower().split())
            if config.subscriber_blocklist.intersection(title_set):
                print(f"blocked: {config.subscriber_blocklist.intersection(title_set)} {article['title']}")
            else:
                print(f"added: {article['title']}")
                articles.append(article)

# Sort articles by (parsed) publication date
articles.sort(key=lambda x: x.published_parsed, reverse=False)

article_idx = 0
selected_articles = []
# TODO: Select enough articles to fill 2 pages instead of just grabbing a fixed number 
# TODO: Consider grabbing more of the article if the summary is short.
for article in articles[-15:]:

    # Generate qr code image files
    article["qr_file"] = os.path.join(os.path.dirname(__file__),  f"img/{article_idx}.jpg")
    qr_link = qrcode.QRCode(
            version = 10,
            box_size = 1,
            border = 4,
            )
    qr_link.add_data(article["link"])
    qr_link.make(fit=False)
    qr_link_img = qr_link.make_image(fill_color="black",back_color="white")
    qr_link_img.save(article["qr_file"], "JPEG")

    selected_articles.append(article)

    article_idx = article_idx + 1

generate_pdf.generate_newspaper_pdf(selected_articles, get_weather())

# Print it!
#send_to_printer(newspaper_pdf)
