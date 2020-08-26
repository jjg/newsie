import os
import smtplib
from email.message import EmailMessage

from pylatex import Math, TikZ, Axis, Plot, Figure, Matrix, Alignat
from pylatex import Document, Section, Subsection, Tabular
from pylatex.utils import italic

import config

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

image_filename = os.path.join(os.path.dirname(__file__), "img/0.jpg")

#geometry_options = {"tmargin": "1cm", "lmargin": "10cm"}
#doc = Document(geometry_options=geometry_options)
#cmd = Command(
#    "documentclass",
#    options=Options("a3paper", "12pt", 
doc = Document(documentclass="\\documentclass[paper=a3, fontsize=12pt, parskip=half, DIV=30]{scartcl}]")

with doc.create(Section("The fancy stuff")):
    doc.create(Subsection("The subsection"))
#    with doc.create(Subsection("The QR Code")):
#        with doc.create(Figure(position="h!")) as qr_img:
#            qr_img.add_image(image_filename)

doc.generate_pdf("full", clean_tex=False)

with open("full.pdf", "rb") as pdf_file:
    send_to_email(pdf_file.read())

