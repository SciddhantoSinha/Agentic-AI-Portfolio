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


def create_test_pdf_with_image(pdf_path: Path):
    document = fitz.open()

    page = document.new_page()

    page.insert_text(
        (72, 72),
        "PDF with embedded image"
    )

    image_document = fitz.open()

    image_page = image_document.new_page(
        width=200,
        height=200,
    )

    image_page.draw_rect(
        fitz.Rect(40, 40, 160, 160),
        fill=(0.5, 0.5, 0.5),
    )

    image_bytes = image_page.get_pixmap().tobytes(
        "png"
    )

    image_document.close()

    page.insert_image(
        fitz.Rect(100, 120, 300, 320),
        stream=image_bytes,
    )

    document.save(pdf_path)
    document.close()


def test_extract_pages_returns_page_information(
    tmp_path,
):

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


def test_render_page_returns_png_bytes(
    tmp_path,
):

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


def test_extract_images_returns_embedded_image(
    tmp_path,
):

    pdf_path = tmp_path / "image.pdf"

    create_test_pdf_with_image(
        pdf_path
    )

    processor = PDFProcessor()

    images = processor.extract_images(
        str(pdf_path)
    )

    assert len(images) == 1

    image = images[0]

    assert image["page_number"] == 1

    assert image["image_index"] == 1

    assert image["extension"] == "png"

    assert isinstance(
        image["bytes"],
        bytes,
    )

    assert len(image["bytes"]) > 0


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


def test_missing_pdf_is_rejected_for_images(
    tmp_path,
):

    processor = PDFProcessor()

    missing_path = tmp_path / "missing.pdf"

    with pytest.raises(
        FileNotFoundError,
        match="PDF file not found",
    ):
        processor.extract_images(
            str(missing_path)
        )


def test_invalid_page_number_is_rejected(
    tmp_path,
):

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


def test_page_beyond_document_is_rejected(
    tmp_path,
):

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
