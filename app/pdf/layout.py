from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib import colors

# Global PDF layout settings
PAGE_MARGIN = 40
LINE_SPACING = 14
FONT_NAME = "Helvetica"
FONT_SIZE = 11

# Paragraph style for ATS-friendly text
ATS_PARAGRAPH_STYLE = ParagraphStyle(
    name="ATSParagraph",
    fontName=FONT_NAME,
    fontSize=FONT_SIZE,
    leading=LINE_SPACING,
    alignment=TA_LEFT,
    textColor=colors.black,
    spaceAfter=8,
)
