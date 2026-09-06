import base64

import pytest

from src.multimodal_rag_engine import (
    MultimodalRAGEngine,
)


def create_test_engine():
    engine = MultimodalRAGEngine.__new__(
        MultimodalRAGEngine
    )

    engine.docstore = {}
    engine.vector_index = []

    from src.retriever import MultimodalRetriever

    engine.retriever = MultimodalRetriever(
        engine.vector_index
    )

    return engine


def test_image_encoding_returns_base64_string():

    image_bytes = b"test-image-data"

    encoded = (
        MultimodalRAGEngine._encode_image_b64(
            image_bytes
        )
    )

    assert isinstance(encoded, str)

    assert encoded != ""


def test_engine_initializes_empty_stores():

    agent = create_test_engine()

    assert agent.docstore == []

    assert agent.vector_index == []


def test_query_without_indexed_documents_is_rejected():

    agent = create_test_engine()

    with pytest.raises(
        ValueError,
        match="No visual elements have been indexed",
    ):
        agent.query_multimodal(
            "What does the image show?"
        )


def test_ingested_visual_element_is_stored():

    agent = create_test_engine()

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

    agent = create_test_engine()

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

    decoded_bytes = base64.b64decode(
        stored_base64
    )

    assert decoded_bytes == original_bytes


def test_multiple_visual_elements_receive_unique_ids():

    agent = create_test_engine()

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


def test_retrieval_resolves_to_original_visual_asset():

    agent = create_test_engine()

    agent.summarize_visual_element = (
        lambda image_bytes, element_type="chart":
        "Quarterly revenue increased from Q1 to Q4."
    )

    original_bytes = b"financial-chart-data"

    doc_id = agent.ingest_image_element(
        image_bytes=original_bytes,
        element_type="chart",
    )

    results = agent.retrieve_visual_context(
        "quarterly revenue",
        top_k=1,
    )

    assert len(results) == 1

    assert results[0]["doc_id"] == doc_id

    matched_doc = agent.docstore[
        results[0]["doc_id"]
    ]

    assert matched_doc["type"] == "image"

    assert (
        base64.b64decode(
            matched_doc["b64"]
        )
        == original_bytes
    )
