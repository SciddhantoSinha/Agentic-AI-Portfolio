from src.document_ingestion import (
    DocumentIngestionPipeline,
)


class FakePDFProcessor:
    def extract_pages(self, pdf_path):

        return [
            {
                "page_number": 1,
                "text": "Financial report",
            }
        ]

    def extract_images(self, pdf_path):

        return [
            {
                "page_number": 1,
                "image_index": 1,
                "extension": "png",
                "bytes": b"chart-data",
            },
            {
                "page_number": 2,
                "image_index": 1,
                "extension": "png",
                "bytes": b"table-data",
            },
        ]


class FakeRAGEngine:
    def __init__(self):

        self.ingested_elements = []

    def ingest_image_element(
        self,
        image_bytes,
        element_type="chart",
    ):

        self.ingested_elements.append(
            {
                "bytes": image_bytes,
                "element_type": element_type,
            }
        )

        return (
            f"doc-{len(self.ingested_elements)}"
        )


def test_ingestion_pipeline_processes_pdf():

    rag_engine = FakeRAGEngine()

    processor = FakePDFProcessor()

    pipeline = DocumentIngestionPipeline(
        rag_engine=rag_engine,
        pdf_processor=processor,
    )

    result = pipeline.ingest_pdf(
        "test-document.pdf"
    )

    assert len(result["pages"]) == 1

    assert len(result["images"]) == 2

    assert result["document_ids"] == [
        "doc-1",
        "doc-2",
    ]


def test_visual_elements_are_sent_to_rag_engine():

    rag_engine = FakeRAGEngine()

    processor = FakePDFProcessor()

    pipeline = DocumentIngestionPipeline(
        rag_engine=rag_engine,
        pdf_processor=processor,
    )

    pipeline.ingest_pdf(
        "test-document.pdf"
    )

    assert len(
        rag_engine.ingested_elements
    ) == 2

    assert (
        rag_engine.ingested_elements[0]["bytes"]
        == b"chart-data"
    )

    assert (
        rag_engine.ingested_elements[1]["bytes"]
        == b"table-data"
    )


def test_element_type_is_inferred():

    png_image = {
        "extension": "png",
        "bytes": b"image-data",
    }

    result = (
        DocumentIngestionPipeline
        ._infer_element_type(
            png_image
        )
    )

    assert result == "visual"


def test_unknown_extension_defaults_to_image():

    image = {
        "extension": "webp",
        "bytes": b"image-data",
    }

    result = (
        DocumentIngestionPipeline
        ._infer_element_type(
            image
        )
    )

    assert result == "image"
