import os

from pylatex import Document, PageStyle, Head, Foot, MiniPage, LargeText, MediumText, LineBreak, Tabu
from pylatex.utils import bold, NoEscape


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
        title_wrapper.append(MediumText(bold("Date")))

with first_page.create(Head("L")) as left_header:
    with left_header.create(MiniPage(width=NoEscape(r"0.49\textwidth"), pos="c", align="l")) as weather_wrapper:
        weather_wrapper.append(MediumText(bold("Temp: 88")))
        weather_wrapper.append(LineBreak())
        weather_wrapper.append(MediumText(bold("Humidity: 44")))

doc.preamble.append(first_page)


# "body"?
with doc.create(Tabu("X[l] X[r]")) as first_page_table:
        customer = MiniPage(width=NoEscape(r"0.49\textwidth"), pos='h')
        customer.append(bold("The title of a story"))
        customer.append("\n")
        customer.append("This is what this looks like with some very long text, like the kind you'd get from an rss feed of a news article.  I hope that it will wrap and lay-out in some not terrible way!")
        customer.append("\n")
        customer.append("Address1")
        customer.append("\n")
        customer.append("Address2")
        customer.append("\n")
        customer.append("Address3")

        # Add branch information
        branch = MiniPage(width=NoEscape(r"0.49\textwidth"), pos='t!',
                          align='r')
        branch.append("Branch no.")
        branch.append(LineBreak())
        branch.append(bold("1181..."))
        branch.append(LineBreak())
        branch.append(bold("TIB Cheque"))

        first_page_table.add_row([customer, branch])
        first_page_table.add_empty_row()

doc.change_document_style("firstpage")
doc.add_color(name="lightgray", model="gray", description="0.80")

doc.generate_pdf("newspaper", clean_tex = False)
