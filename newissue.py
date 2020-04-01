import pydf
import smtplib

from email.message import EmailMessage

from config import config

# TODO: Load subscriber from some datasource
subscriber_printer_email = config["debug_email"]
subscriber_blacklist = ""


# TODO: Load a list of RSS feeds
# TODO: Fetch articles from the last 24 hours
# TODO: Filter through subscriber blacklist
# TODO: Randomly select enough to fill 2 pages

# Render each article into html
newspaper_html = "<h1>The Daily Facto</h1>"

# TODO: Insert headline
# TODO: Insert summary
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
