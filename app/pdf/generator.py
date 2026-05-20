import os
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.pagesizes import LETTER
from app.pdf.layout import (
    PAGE_MARGIN,
    ATS_PARAGRAPH_STYLE
)
from app.schemas import PdfArtifact


def generate_pdf(user_phone: str, text: str) -> PdfArtifact:
    """
    Generates a clean, ATS-compliant PDF resume.
    - Single column
    - No tables, images, or multi-column layouts
    - Pure text for maximum ATS compatibility
    """

    # Output directory
    folder = f"data/output/{user_phone}"
    os.makedirs(folder, exist_ok=True)

    file_path = f"{folder}/optimized_resume.pdf"

    # Create PDF document
    doc = SimpleDocTemplate(
        file_path,
        pagesize=LETTER,
        leftMargin=PAGE_MARGIN,
        rightMargin=PAGE_MARGIN,
        topMargin=PAGE_MARGIN,
        bottomMargin=PAGE_MARGIN,
    )

    # Split text into paragraphs
    paragraphs = []
    for block in text.split("\n"):
        block = block.strip()
        if block:
            paragraphs.append(Paragraph(block, ATS_PARAGRAPH_STYLE))

    # Build PDF
    doc.build(paragraphs)

    # File size
    file_size_kb = round(os.path.getsize(file_path) / 1024, 2)

    return PdfArtifact(
        file_path=file_path,
        file_size_kb=file_size_kb,
        delivered_to=user_phone
    )
