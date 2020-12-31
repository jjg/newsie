import os

from pylatex import Package, Document, PageStyle, Head, Foot, MiniPage, LargeText, MediumText, LineBreak, Tabu, Figure, Section, StandAloneGraphic
from pylatex.utils import bold, NoEscape

def generate_newspaper_pdf(articles):

    MAX_ARTICLES = len(articles) 

    geometry_options = {
        "head": "40pt",
        "margin": "0.5in",
        "bottom": "0.6in",
        "includeheadfoot": True
    }

    doc = Document(geometry_options = geometry_options)

    # Try adding the graphicx manually to fix errors with adding images
    doc.packages.append(Package("graphicx"))
    #Package(name="graphicx")

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
        article_frames = []
        for article in articles:
            
            qr_file = os.path.join(os.path.dirname(__file__), article["qr_code"])

            article_frame = MiniPage(width=NoEscape(r"0.45\textwidth"), pos='h')
            with article_frame.create(Section(title=article["title"], numbering=False)):
                article_frame.append(article["summary"])
                article_frame.append(StandAloneGraphic(filename="/home/jason/Development/paperboy/img/10.jpg",image_options="width=65px"))

            #article_frame = MiniPage(pos='h')
            # TODO: Add QR code
            #with article_frame.create(MiniPage(pos="l")) as qr_wrapper:
            #qr_file = os.path.join(os.path.dirname(__file__), article["qr_code"])
            #print(qr_file)
            #    qr_wrapper.append(StandAloneGraphic(filename=qr_file))
            #article_frame.append(StandAloneGraphic(filename=qr_file))
            #with article_frame.create(Figure()) as qr_figure:
            #    qr_figure.add_image(qr_file, width="12px")
            #article_frame.add_image(qr_file)
            #article_frame.append(bold(article["title"]))
            #article_frame.append(LineBreak())
            #article_frame.append(article["summary"])
            #article_frame.append(LineBreak())

            article_frames.append(article_frame)

        # Add each article to alternating columns.
        for i in range(int(MAX_ARTICLES / 2)):
            first_page_table.add_row([article_frames[i], article_frames[i*2]])
            first_page_table.add_empty_row()

    # This adds the header to the page for some reason???
    doc.change_document_style("firstpage")

    # TODO: Figure out what the line below does and if we need it
    #doc.add_color(name="lightgray", model="gray", description="0.80")

    # TODO: Consider adding a footer

    doc.generate_pdf("newspaper", clean_tex = False)
