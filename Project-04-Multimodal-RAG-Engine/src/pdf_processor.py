from pathlib import Path
from typing import List, Dict

import fitz


class PDFProcessor:
    """
    Basic PDF processor for multimodal document ingestion.

    Extracts page-level text and renders PDF pages as images,
    providing the foundation for separating textual and visual
    document elements.
    """

    def extract_pages(
        self,
        pdf_path: str,
    ) -> List[Dict]:
        """
        Extract text and metadata from every PDF page.

        Args:
            pdf_path: Path to the PDF document.

        Returns:
            A list containing page-level document information.
        """

        path = Path(pdf_path)

        if not path.exists():
            raise FileNotFoundError(
                f"PDF file not found: {pdf_path}"
            )

        document = fitz.open(pdf_path)

        pages = []

        for page_number, page in enumerate(document, start=1):
            pages.append(
                {
                    "page_number": page_number,
                    "text": page.get_text(),
                }
            )

        document.close()

        return pages

    def render_page(
        self,
        pdf_path: str,
        page_number: int = 1,
    ) -> bytes:
        """
        Render a PDF page into PNG image bytes.

        Args:
            pdf_path: Path to the PDF document.
            page_number: One-based page number.

        Returns:
            PNG image bytes for the requested page.
        """

        path = Path(pdf_path)

        if not path.exists():
            raise FileNotFoundError(
                f"PDF file not found: {pdf_path}"
            )

        if page_number < 1:
            raise ValueError(
                "page_number must be greater than or equal to 1."
            )

        document = fitz.open(pdf_path)

        if page_number > len(document):
            document.close()
            raise ValueError(
                f"PDF contains only {len(document)} pages."
            )

        page = document.load_page(page_number - 1)

        pixmap = page.get_pixmap()

        image_bytes = pixmap.tobytes("png")

        document.close()

        return image_bytes
