from src.retriever import InternalRetriever


def test_add_document():
    retriever = InternalRetriever()

    retriever.add_document(
        document_id="doc-1",
        content="The deployment process uses Docker containers.",
    )

    assert len(retriever.documents) == 1
    assert retriever.documents[0]["document_id"] == "doc-1"


def test_retrieve_returns_matching_document():
    retriever = InternalRetriever()

    retriever.add_document(
        document_id="doc-1",
        content="The deployment process uses Docker containers.",
    )

    retriever.add_document(
        document_id="doc-2",
        content="The finance team manages quarterly reports.",
    )

    results = retriever.retrieve(
        "How does the deployment process use Docker?"
    )

    assert results[0]["document_id"] == "doc-1"
    assert results[0]["score"] > 0


def test_retrieve_ranks_best_match_first():
    retriever = InternalRetriever()

    retriever.add_document(
        document_id="doc-1",
        content="Python and Docker are used for deployment.",
    )

    retriever.add_document(
        document_id="doc-2",
        content="The deployment process uses Docker containers.",
    )

    results = retriever.retrieve(
        "deployment Docker containers",
        top_k=2,
    )

    assert results[0]["document_id"] == "doc-2"


def test_empty_retriever_returns_empty_results():
    retriever = InternalRetriever()

    results = retriever.retrieve(
        "deployment process"
    )

    assert results == []
