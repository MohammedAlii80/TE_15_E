# Note to run this script (specifically for datamatrix generation) you will need the following installed:
#  - dmtx-utils (available through apt-get)
#  - pylibdmtx (available on pip3)
#  - reportlab version 3.5.52 or higher (available on pip3)


from io import BytesIO
from PyPDF2 import PdfFileReader, PdfFileMerger

from reportlab.graphics import renderPDF
from reportlab.graphics.barcode import dmtx
from reportlab.graphics.shapes import Drawing
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4


OTHER_DEMO_FILENAME = "barcodes_demo.pdf"
FONT = "Helvetica"
HEADER_FONT_SIZE = 16
LABEL_FONT_SIZE = 14
TITLE_FONT_SIZE = 11
CODE_FONT_SIZE = 8
FOOTER_FONT_SIZE = 8
PAGE_SIZE = A4


def create_page(barcodes, font_size_and_texts):
    packet = BytesIO()
    can = canvas.Canvas(packet, pagesize=PAGE_SIZE)
    for barcode in barcodes:
        d = Drawing(PAGE_SIZE[0], PAGE_SIZE[1])
        d.add(dmtx.DataMatrixWidget(barcode[2]))
        renderPDF.draw(d, can, barcode[0], barcode[1])

    # add text
    for font_size, texts in font_size_and_texts:
        can.setFont(FONT, font_size)
        for text in texts:
            can.drawString(text[0], text[1], text[2])
    can.save()
    packet.seek(0)
    return PdfFileReader(packet)


# same on all GS1 pages
footer = [(45, 45, "Don't have any barcode scanner? Right click on your screen > Inspect > Console and type the following command:"),
          (45, 35, r'   odoo.__DEBUG__.services["web.core"].bus.trigger("barcode_scanned", "setyourbarcodehere", \$(".o_web_client")[0])'),
          (45, 25, 'and replace "setyourbarcodehere" by the barcode you would like to scan OR use our mobile app.'),
          (45, 15, 'For GS1 barcodes, remove all "("s and ")"s')]

# page 1
# format is (x, y, "barcode")
# barcodes to generate
barcodes = [(65, 635, "WH-RECEIPTS"), (250, 623, "0106016478556677300000000510Lot0001"), (435, 623, "0106016478556677300000000510Lot0002"),
            (65, 490, "0106016478556677300000000510Lot0003"), (250, 500, "O-BTN.validate"),
            (65, 345, "WH-RECEIPTS"), (250, 345, "01060164785599993650000010"), (435, 345, "01060164785599823160000002"),
            (65, 215, "O-BTN.validate")]

header = [(45, 785, "GS1 Barcodes (set Barcode Nomenclature to Default GS1 Nomenclature)")]
# text to describe barcode flow
flow_labels = [(45, 752, "Receive products tracked by lot (activate Lots & Serial Numbers) "),
               (45, 460, "Receive products with different unit of measures (activate Units of Measure)")]

# text to describe (above) each barcode
barcode_titles = [(55, 733, "YourCompany Receipts"), (215, 733, "Cable Management Box x5 Lot0001"), (400, 733, "Cable Management Box x5 Lot0002"),
                  (45, 600, "Cable Management Box x5 Lot0003"), (280, 600, "Validate"),
                  (55, 444, "YourCompany Receipts"), (230, 444, "Customized Cabinet (USA) 10 ft³"), (415, 444, "Customized Cabinet (Metric) 2 m³"),
                  (93, 315, "Validate")]

# text of barcode code (below), but made to look pretty (not literal barcode)
barcode_code = [(85, 631, "WH-RECEIPTS"), (220, 619, "(01)06016478556677(30)00000005(10)Lot0001"), (405, 619, "(01)06016478556677(30)00000005(10)Lot0002"),
                (45, 485, "(01)06016478556677(30)00000005(10)Lot0003"), (275, 495, "O-BTN.validate"),
                (85, 340, "WH-RECEIPTS"), (238, 340, "(01)06016478559999(3650)000010"), (425, 340, "(01)06016478559982(3160)000002"),
                (85, 212, "O-BTN.validate")]


font_size_and_texts = [(HEADER_FONT_SIZE, header),
                       (LABEL_FONT_SIZE, flow_labels),
                       (TITLE_FONT_SIZE, barcode_titles),
                       (CODE_FONT_SIZE, barcode_code),
                       (FOOTER_FONT_SIZE, footer)]

page1 = create_page(barcodes, font_size_and_texts)

# page 2
# format is (x, y, "barcode")
# barcodes to generate
barcodes = [(65, 635, "WH-RECEIPTS"), (250, 635, "0106016478556332305"), (435, 635, "0006016471234567890591PAL"),
            (65, 500, "O-BTN.validate")]

header = []
# text to describe barcode flow
flow_labels = [(45, 752, "Put in Pack (activate Packages)")]

# text to describe (above) each barcode
barcode_titles = [(55, 733, "YourCompany Receipts"), (233, 733, "Individual Workplace x10"), (410, 733, "Put in Pack: Pallet with SSCC"),
                  (93, 600, "Validate")]

# text of barcode code (below), but made to look pretty (not literal barcode)
barcode_code = [(85, 631, "WH-RECEIPTS"), (245, 631, "(01)06016478556332(30)10"), (425, 631, "(00)060164712345678905(91)PAL"),
                (85, 495, "O-BTN.validate")]

font_size_and_texts = [(HEADER_FONT_SIZE, header),
                       (LABEL_FONT_SIZE, flow_labels),
                       (TITLE_FONT_SIZE, barcode_titles),
                       (CODE_FONT_SIZE, barcode_code),
                       (FOOTER_FONT_SIZE, footer)]

page2 = create_page(barcodes, font_size_and_texts)


# merge with other demo barcodes
merger = PdfFileMerger()
merger.append(PdfFileReader(open(OTHER_DEMO_FILENAME, "rb")))
merger.append(page1)
merger.append(page2)
merger.write(OTHER_DEMO_FILENAME)
