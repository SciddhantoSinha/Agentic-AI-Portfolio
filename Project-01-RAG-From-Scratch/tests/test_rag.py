from src.rag_pipeline import ScratchRAGPipeline


def test_pipeline_initialization():
    pipeline = ScratchRAGPipeline(
        openai_api_key="test-key"
    )

    assert pipeline.dimension == 1536
    assert pipeline.documents == []
    assert pipeline.index.ntotal == 0


def test_faiss_index_configuration():
    pipeline = ScratchRAGPipeline(
        openai_api_key="test-key"
    )

    assert pipeline.index.d == 1536
    assert pipeline.index.ntotal == 0


def test_document_storage():
    pipeline = ScratchRAGPipeline(
        openai_api_key="test-key"
    )

    pipeline.documents.extend(
        [
            "This is the first document chunk.",
            "This is the second document chunk.",
        ]
    )

    assert len(pipeline.documents) == 2
    assert pipeline.documents[0] == "This is the first document chunk."
    assert pipeline.documents[1] == "This is the second document chunk."
