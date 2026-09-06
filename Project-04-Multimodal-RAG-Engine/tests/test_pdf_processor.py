from pathlib import Path

import fitz
import pytest

from src.pdf_processor import PDFProcessor


def create_test_pdf(pdf_path: Path):
    document = fitz.open()

    page = document.new_page()

    page.insert_text(
        (72, 72),
        "Multimodal RAG Test Document"
    )

    page.insert_text(
        (72, 100),
        "This page contains test document content."
    )

    document.save(pdf_path)
    document.close()


def test_extract_pages_returns_page_information(tmp_path):

    pdf_path = tmp_path / "test.pdf"

    create_test_pdf(pdf_path)

    processor = PDFProcessor()

    pages = processor.extract_pages(
        str(pdf_path)
    )

    assert len(pages) == 1

    assert pages[0]["page_number"] == 1

    assert (
        "Multimodal RAG Test Document"
        in pages[0]["text"]
    )


def test_render_page_returns_png_bytes(tmp_path):

    pdf_path = tmp_path / "test.pdf"

    create_test_pdf(pdf_path)

    processor = PDFProcessor()

    image_bytes = processor.render_page(
        str(pdf_path),
        page_number=1,
    )

    assert isinstance(image_bytes, bytes)

    assert image_bytes.startswith(
        b"\x89PNG"
    )


def test_missing_pdf_is_rejected(tmp_path):

    processor = PDFProcessor()

    missing_path = tmp_path / "missing.pdf"

    with pytest.raises(
        FileNotFoundError,
        match="PDF file not found",
    ):
        processor.extract_pages(
            str(missing_path)
        )


def test_invalid_page_number_is_rejected(tmp_path):

    pdf_path = tmp_path / "test.pdf"

    create_test_pdf(pdf_path)

    processor = PDFProcessor()

    with pytest.raises(
        ValueError,
        match="page_number must be greater",
    ):
        processor.render_page(
            str(pdf_path),
            page_number=0,
        )


def test_page_beyond_document_is_rejected(tmp_path):

    pdf_path = tmp_path / "test.pdf"

    create_test_pdf(pdf_path)

    processor = PDFProcessor()

    with pytest.raises(
        ValueError,
        match="PDF contains only 1 pages",
    ):
        processor.render_page(
            str(pdf_path),
            page_number=2,
        )
