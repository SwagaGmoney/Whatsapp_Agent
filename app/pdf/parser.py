import re
from typing import Dict, Optional, List

import pdfplumber
import fitz  # PyMuPDF


class ResumeParser:
    """
    Production-grade PDF → text parser.
    Uses pdfplumber as primary extractor and PyMuPDF as fallback.
    Includes:
        - bullet normalization
        - whitespace cleanup
        - section detection
        - email/phone/linkedin extraction
    """

   
    # Public API
    def parse(self, file_path: str) -> Dict:
        raw_text = self._extract_text(file_path)
        cleaned = self._clean_text(raw_text)
        sections = self._split_into_sections(cleaned)

        return {
            "raw_text": raw_text,
            "cleaned_text": cleaned,
            "sections": sections,
            "metadata": {
                "emails": self._extract_emails(cleaned),
                "phones": self._extract_phones(cleaned),
                "linkedin": self._extract_linkedin(cleaned),
            },
        }

    
    # Extraction Layer
    def _extract_text(self, file_path: str) -> str:
        """
        Try pdfplumber first (best for structured text).
        Fallback to PyMuPDF if pdfplumber fails or returns empty.
        """
        text = ""

        # Primary: pdfplumber
        try:
            with pdfplumber.open(file_path) as pdf:
                pages = [page.extract_text() or "" for page in pdf.pages]
                text = "\n".join(pages)
        except Exception:
            text = ""

        # Fallback: PyMuPDF
        if not text.strip():
            try:
                doc = fitz.open(file_path)
                text = "\n".join([page.get_text() for page in doc])
            except Exception:
                pass

        return text or ""

   
    # Cleaning Layer
    def _clean_text(self, text: str) -> str:
        if not text:
            return ""

        # Normalize bullets
        text = re.sub(r"[•●▪■]", "-", text)

        # Remove double spaces
        text = re.sub(r"\s{2,}", " ", text)

        # Normalize newlines
        text = re.sub(r"\n{2,}", "\n", text)

        return text.strip()

   
    # Section Splitting
    SECTION_HEADERS = [
        "summary",
        "experience",
        "work experience",
        "professional experience",
        "education",
        "projects",
        "skills",
        "certifications",
        "publications",
        "achievements",
        "awards",
    ]

    def _split_into_sections(self, text: str) -> Dict[str, str]:
        """
        Splits resume into sections based on common headers.
        """
        lines = text.split("\n")
        sections = {}
        current_header = "general"
        sections[current_header] = []

        for line in lines:
            normalized = line.lower().strip()

            if any(normalized.startswith(h) for h in self.SECTION_HEADERS):
                current_header = normalized
                sections[current_header] = []
            else:
                sections[current_header].append(line)

        # Join lines
        return {k: "\n".join(v).strip() for k, v in sections.items()}

   
    # Metadata Extraction
    def _extract_emails(self, text: str) -> List[str]:
        return re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)

    def _extract_phones(self, text: str) -> List[str]:
        return re.findall(r"\+?\d[\d\-\(\) ]{7,}\d", text)

    def _extract_linkedin(self, text: str) -> Optional[str]:
        match = re.search(r"(https?://)?(www\.)?linkedin\.com/[A-Za-z0-9/\-_%]+", text)
        return match.group(0) if match else None



parser = ResumeParser()
