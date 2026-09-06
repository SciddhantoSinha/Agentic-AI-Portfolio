import pytest

from src.rag_pipeline import ScratchRAGPipeline


def test_pipeline_initialization():
    pipeline = ScratchRAGPipeline(
        openai_api_key="test-key"
    )

    assert pipeline.dimension == 1536
    assert pipeline.documents == []
    assert pipeline.index.ntotal == 0


def test_retrieve_from_empty_index():
    pipeline = ScratchRAGPipeline(
        openai_api_key="test-key"
    )

    results = pipeline.retrieve(
        query="test query",
        top_k=4
    )

    assert results == []
