from pathlib import Path
from typing import List, Dict

import fitz


class PDFProcessor:
    """
    PDF processor for multimodal document ingestion.

    Extracts:
    1. Page-level text.
    2. Embedded images.
    3. Rendered page images.

    This provides the foundation for separating textual
    and visual document elements.
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
            Page-level document information.
        """

        path = Path(pdf_path)

        if not path.exists():
            raise FileNotFoundError(
                f"PDF file not found: {pdf_path}"
            )

        document = fitz.open(pdf_path)

        pages = []

        for page_number, page in enumerate(
            document,
            start=1,
        ):
            pages.append(
                {
                    "page_number": page_number,
                    "text": page.get_text(),
                }
            )

        document.close()

        return pages

    def extract_images(
        self,
        pdf_path: str,
    ) -> List[Dict]:
        """
        Extract embedded images from a PDF.

        Args:
            pdf_path: Path to the PDF document.

        Returns:
            Metadata and raw bytes for each embedded image.
        """

        path = Path(pdf_path)

        if not path.exists():
            raise FileNotFoundError(
                f"PDF file not found: {pdf_path}"
            )

        document = fitz.open(pdf_path)

        images = []

        for page_number, page in enumerate(
            document,
            start=1,
        ):
            for image_index, image_info in enumerate(
                page.get_images(full=True),
                start=1,
            ):
                xref = image_info[0]

                image_data = document.extract_image(
                    xref
                )

                images.append(
                    {
                        "page_number": page_number,
                        "image_index": image_index,
                        "extension": image_data["ext"],
                        "bytes": image_data["image"],
                    }
                )

        document.close()

        return images

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
                page_count = len(document)
                document.close()

    raise ValueError(
        f"PDF contains only {page_count} pages."
    )

        page = document.load_page(
            page_number - 1
        )

        pixmap = page.get_pixmap()

        image_bytes = pixmap.tobytes("png")

        document.close()

        return image_bytes
