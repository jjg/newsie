import os

from pylatex import Document, PageStyle, Head, Foot, MiniPage, LargeText, MediumText, LineBreak, Tabu
from pylatex.utils import bold, NoEscape

MAX_ARTICLES = 10

geometry_options = {
    "head": "40pt",
    "margin": "0.5in",
    "bottom": "0.6in",
    "includeheadfoot": True
}

doc = Document(geometry_options = geometry_options)

first_page = PageStyle("firstpage")

# Header
with first_page.create(Head("C")) as center_header:
    with center_header.create(MiniPage(width=NoEscape(r"0.49\textwidth"), pos="c", align="c")) as title_wrapper:
        title_wrapper.append(LargeText(bold("Its Some News")))
        title_wrapper.append(LineBreak())
        # TODO: Add the actual date (not just the string Date)
        title_wrapper.append(MediumText(bold("Date")))

with first_page.create(Head("L")) as left_header:
    with left_header.create(MiniPage(width=NoEscape(r"0.49\textwidth"), pos="c", align="l")) as weather_wrapper:
        # TODO: Get the actual values from the weather station
        # TODO: These should be smaller, maybe include an image?
        weather_wrapper.append(MediumText(bold("Temp: 88")))
        weather_wrapper.append(LineBreak())
        weather_wrapper.append(MediumText(bold("Humidity: 44")))

# TODO: Consider adding something to the right of the header
doc.preamble.append(first_page)

# Body 
with doc.create(Tabu("X[l] X[r]")) as first_page_table:

    # Generate a MiniPage for each article. 
    articles = []
    for i in range(MAX_ARTICLES):
        article = MiniPage(width=NoEscape(r"0.45\textwidth"), pos='h')
        # TODO: Add QR code
        article.append(bold("Headline"))
        article.append(LineBreak())
        article.append("This is the text of the article summary.  It should be a few lines long, but I don't want to type a bunch of stuff so maybe this will be enough?  I don't know, let's try one more sentence and see what happens.")
        article.append(LineBreak())

        articles.append(article)

    # Add each article to alternating columns.
    for i in range(int(MAX_ARTICLES / 2)):
        first_page_table.add_row([articles[i], articles[i*2]])
        first_page_table.add_empty_row()

# This adds the header to the page for some reason???
doc.change_document_style("firstpage")

# TODO: Figure out what the line below does and if we need it
#doc.add_color(name="lightgray", model="gray", description="0.80")

# TODO: Consider adding a footer

doc.generate_pdf("newspaper", clean_tex = False)
