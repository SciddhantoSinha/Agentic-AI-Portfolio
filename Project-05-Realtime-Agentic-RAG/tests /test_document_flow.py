from unittest.mock import MagicMock

from src.crag_pipeline import CRAGPipeline
from src.evaluator import RetrievalEvaluator
from src.retriever import InternalRetriever
from src.router import Route


def test_crag_internal_to_generation_flow():
    live_search = MagicMock()

    retriever = InternalRetriever()

    retriever.add_document(
        document_id="policy-1",
        content=(
            "The internal security policy requires "
            "multi-factor authentication for all users."
        ),
    )

    pipeline = CRAGPipeline(
        api_key="test-key",
        live_search=live_search,
        internal_retriever=retriever,
        evaluator=RetrievalEvaluator(
            relevance_threshold=0.2
        ),
    )

    pipeline.client = MagicMock()

    pipeline.client.chat.completions.create.return_value.choices[
        0
    ].message.content = (
        "The internal security policy requires "
        "multi-factor authentication for all users."
    )

    result = pipeline.run(
        "What does the security policy require "
        "for authentication?"
    )

    assert result["route"] == Route.INTERNAL.value
    assert result["fallback_triggered"] is False
    assert result["grounded"] is True
    assert result["documents"]

    live_search.search.assert_not_called()


def test_crag_corrective_fallback_flow():
    live_search = MagicMock()

    retriever = InternalRetriever()

    retriever.add_document(
        document_id="internal-1",
        content=(
            "The internal handbook describes employee "
            "onboarding procedures."
        ),
    )

    live_search.search.return_value = [
        {
            "title": "Current Platform Status",
            "content": (
                "The current platform status is operational."
            ),
            "url": "https://example.com/status",
            "score": 0.94,
        }
    ]

    pipeline = CRAGPipeline(
        api_key="test-key",
        live_search=live_search,
        internal_retriever=retriever,
        evaluator=RetrievalEvaluator(
            relevance_threshold=0.5
        ),
    )

    pipeline.client = MagicMock()

    pipeline.client.chat.completions.create.return_value.choices[
        0
    ].message.content = (
        "The current platform status is operational."
    )

    result = pipeline.run(
        "What is the current platform status?"
    )

    assert result["fallback_triggered"] is True
    assert result["documents"]
    assert result["grounded"] is True

    live_search.search.assert_called_once_with(
        query="What is the current platform status?",
        max_results=5,
    )
