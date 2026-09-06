from unittest.mock import MagicMock

from src.crag_pipeline import CRAGPipeline
from src.evaluator import RetrievalEvaluator
from src.retriever import InternalRetriever
from src.router import Route


def build_pipeline():
    live_search = MagicMock()
    internal_retriever = InternalRetriever()

    internal_retriever.add_document(
        document_id="doc-1",
        content=(
            "The deployment process uses Docker containers "
            "for production applications."
        ),
    )

    evaluator = RetrievalEvaluator(
        relevance_threshold=0.2
    )

    pipeline = CRAGPipeline(
        api_key="test-key",
        live_search=live_search,
        internal_retriever=internal_retriever,
        evaluator=evaluator,
    )

    pipeline.client = MagicMock()

    return pipeline, live_search


def test_internal_query_uses_internal_retrieval():
    pipeline, live_search = build_pipeline()

    pipeline.client.chat.completions.create.return_value.choices[
        0
    ].message.content = (
        "Docker containers are used for deployment."
    )

    result = pipeline.run(
        "How does deployment use Docker?"
    )

    assert result["route"] == Route.INTERNAL.value
    assert result["fallback_triggered"] is False
    assert result["documents"]
    assert result["grounded"] is True
    live_search.search.assert_not_called()


def test_low_relevance_triggers_live_fallback():
    pipeline, live_search = build_pipeline()

    live_search.search.return_value = [
        {
            "title": "Latest Deployment Guide",
            "content": (
                "The current deployment platform "
                "uses Kubernetes."
            ),
            "url": "https://example.com/deployment",
            "score": 0.95,
        }
    ]

    pipeline.client.chat.completions.create.return_value.choices[
        0
    ].message.content = (
        "The current deployment platform uses Kubernetes."
    )

    result = pipeline.run(
        "What is the current Kubernetes deployment platform?"
    )

    assert result["fallback_triggered"] is True
    assert result["documents"]
    live_search.search.assert_called_once()


def test_live_route_uses_live_search():
    pipeline, live_search = build_pipeline()

    live_search.search.return_value = [
        {
            "title": "Current AI News",
            "content": (
                "The latest AI systems are improving."
            ),
            "url": "https://example.com/ai",
            "score": 0.9,
        }
    ]

    pipeline.client.chat.completions.create.return_value.choices[
        0
    ].message.content = (
        "The latest AI systems are improving."
    )

    result = pipeline.run(
        "What is the latest AI news?"
    )

    assert result["route"] == Route.LIVE.value
    assert result["fallback_triggered"] is False
    live_search.search.assert_called_once()


def test_no_evidence_returns_safe_response():
    pipeline, live_search = build_pipeline()

    live_search.search.return_value = []

    result = pipeline.run(
        "What is the current status of this unknown topic?"
    )

    assert result["documents"] == []
    assert result["grounded"] is False
    assert "No sufficiently relevant evidence" in (
        result["answer"]
    )


def test_empty_query_raises_error():
    pipeline, _ = build_pipeline()

    try:
        pipeline.run("")
        assert False
    except ValueError:
        assert True
