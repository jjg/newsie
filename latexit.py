from pylatex import Document, Section, Subsection, Tabular
from pylatex import Math, TikZ, Axis, Plot, Figure, Matrix, Alignat
from pylatex.utils import italic
import os

image_filename = os.path.join(os.path.dirname(__file__), "img/0.jpg")

geometry_options = {"tmargin": "1cm", "lmargin": "10cm"}
doc = Document(geometry_options=geometry_options)

with doc.create(Section("The fancy stuff")):
    with doc.create(Subsection("The QR Code")):
        with doc.create(Figure(position="h!")) as qr_img:
            qr_img.add_image(image_filename)

doc.generate_pdf("full", clean_tex=False)
