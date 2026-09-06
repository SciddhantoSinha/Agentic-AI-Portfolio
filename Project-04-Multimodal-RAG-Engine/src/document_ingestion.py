from typing import Dict, List

from .multimodal_rag_engine import MultimodalRAGEngine
from .pdf_processor import PDFProcessor


class DocumentIngestionPipeline:
    """
    Multimodal document ingestion pipeline.

    Processes a PDF into page-level content and visual
    representations, then sends visual elements through
    the multimodal RAG ingestion process.

    Text and visual content are kept conceptually separate
    so that visual information is not flattened into plain OCR
    text.
    """

    def __init__(
        self,
        rag_engine: MultimodalRAGEngine,
        pdf_processor: PDFProcessor = None,
    ):
        self.rag_engine = rag_engine

        self.pdf_processor = (
            pdf_processor
            if pdf_processor is not None
            else PDFProcessor()
        )

    def ingest_pdf(
        self,
        pdf_path: str,
    ) -> Dict[str, List]:
        """
        Process a PDF and ingest its visual elements.

        Args:
            pdf_path: Path to the PDF document.

        Returns:
            Dictionary containing extracted pages, images,
            and generated document identifiers.
        """

        pages = self.pdf_processor.extract_pages(
            pdf_path
        )

        images = self.pdf_processor.extract_images(
            pdf_path
        )

        document_ids = []

        for image in images:

            element_type = self._infer_element_type(
                image
            )

            doc_id = (
                self.rag_engine.ingest_image_element(
                    image_bytes=image["bytes"],
                    element_type=element_type,
                )
            )

            document_ids.append(doc_id)

        return {
            "pages": pages,
            "images": images,
            "document_ids": document_ids,
        }

    @staticmethod
    def _infer_element_type(
        image: Dict,
    ) -> str:
        """
        Infer a basic visual element type.

        The current prototype uses metadata and defaults
        to a generic visual element when the PDF does not
        provide semantic information.
        """

        extension = image.get(
            "extension",
            "",
        ).lower()

        if extension in {
            "png",
            "jpg",
            "jpeg",
        }:
            return "visual"

        return "image"
