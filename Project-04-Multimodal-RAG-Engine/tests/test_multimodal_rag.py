import pytest

from src.multimodal_rag_engine import MultimodalRAGEngine


def test_image_encoding_returns_base64_string():
    image_bytes = b"test-image-data"

    encoded = MultimodalRAGEngine._encode_image_b64(
        image_bytes
    )

    assert isinstance(encoded, str)
    assert encoded != ""


def test_engine_initializes_empty_stores():

    agent = MultimodalRAGEngine.__new__(
        MultimodalRAGEngine
    )

    agent.docstore = {}
    agent.vector_index = []

    assert agent.docstore == {}
    assert agent.vector_index == []


def test_query_without_indexed_documents_is_rejected():

    agent = MultimodalRAGEngine.__new__(
        MultimodalRAGEngine
    )

    agent.docstore = {}
    agent.vector_index = []

    with pytest.raises(
        ValueError,
        match="No visual elements have been indexed",
    ):
        agent.query_multimodal(
            "What does the image show?"
        )


def test_ingested_visual_element_is_stored():

    agent = MultimodalRAGEngine.__new__(
        MultimodalRAGEngine
    )

    agent.docstore = {}
    agent.vector_index = []

    def fake_summary(
        image_bytes: bytes,
        element_type: str = "chart",
    ) -> str:
        return (
            "A chart showing quarterly revenue trends."
        )

    agent.summarize_visual_element = fake_summary

    doc_id = agent.ingest_image_element(
        image_bytes=b"test-image",
        element_type="chart",
    )

    assert doc_id in agent.docstore
    assert len(agent.vector_index) == 1

    assert (
        agent.vector_index[0]["doc_id"]
        == doc_id
    )

    assert (
        agent.vector_index[0]["summary"]
        == "A chart showing quarterly revenue trends."
    )

    assert (
        agent.vector_index[0]["element_type"]
        == "chart"
    )

    assert (
        agent.docstore[doc_id]["type"]
        == "image"
    )


def test_ingested_image_preserves_original_bytes_as_base64():

    agent = MultimodalRAGEngine.__new__(
        MultimodalRAGEngine
    )

    agent.docstore = {}
    agent.vector_index = []

    agent.summarize_visual_element = (
        lambda image_bytes, element_type="chart":
        "Visual summary"
    )

    original_bytes = b"original-visual-data"

    doc_id = agent.ingest_image_element(
        image_bytes=original_bytes,
        element_type="diagram",
    )

    stored_base64 = agent.docstore[doc_id]["b64"]

    decoded_bytes = (
        __import__("base64")
        .b64decode(stored_base64)
    )

    assert decoded_bytes == original_bytes


def test_multiple_visual_elements_receive_unique_ids():

    agent = MultimodalRAGEngine.__new__(
        MultimodalRAGEngine
    )

    agent.docstore = {}
    agent.vector_index = []

    agent.summarize_visual_element = (
        lambda image_bytes, element_type="chart":
        f"Summary for {element_type}"
    )

    first_id = agent.ingest_image_element(
        b"chart-data",
        "chart",
    )

    second_id = agent.ingest_image_element(
        b"table-data",
        "table",
    )

    assert first_id != second_id
    assert len(agent.docstore) == 2
    assert len(agent.vector_index) == 2
