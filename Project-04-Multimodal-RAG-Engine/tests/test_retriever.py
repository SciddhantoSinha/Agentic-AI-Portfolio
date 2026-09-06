from src.retriever import MultimodalRetriever


def test_empty_index_returns_no_results():

    retriever = MultimodalRetriever([])

    results = retriever.retrieve(
        "financial chart"
    )

    assert results == []


def test_retriever_returns_matching_summary():

    index = [
        {
            "doc_id": "chart-1",
            "summary": (
                "Quarterly revenue increased "
                "from Q1 to Q4."
            ),
            "element_type": "chart",
        },
        {
            "doc_id": "diagram-1",
            "summary": (
                "Cloud architecture with "
                "application servers."
            ),
            "element_type": "diagram",
        },
    ]

    retriever = MultimodalRetriever(index)

    results = retriever.retrieve(
        "quarterly revenue"
    )

    assert len(results) == 1

    assert results[0]["doc_id"] == "chart-1"

    assert results[0]["score"] > 0


def test_retriever_ranks_higher_overlap_first():

    index = [
        {
            "doc_id": "chart-1",
            "summary": (
                "Revenue chart showing quarterly "
                "revenue growth."
            ),
            "element_type": "chart",
        },
        {
            "doc_id": "table-1",
            "summary": (
                "Financial table containing "
                "annual expenses."
            ),
            "element_type": "table",
        },
    ]

    retriever = MultimodalRetriever(index)

    results = retriever.retrieve(
        "revenue quarterly growth",
        top_k=2,
    )

    assert results[0]["doc_id"] == "chart-1"

    assert (
        results[0]["score"]
        >= results[1]["score"]
    )


def test_top_k_limits_results():

    index = [
        {
            "doc_id": "visual-1",
            "summary": "revenue chart",
            "element_type": "chart",
        },
        {
            "doc_id": "visual-2",
            "summary": "revenue table",
            "element_type": "table",
        },
        {
            "doc_id": "visual-3",
            "summary": "revenue diagram",
            "element_type": "diagram",
        },
    ]

    retriever = MultimodalRetriever(index)

    results = retriever.retrieve(
        "revenue",
        top_k=2,
    )

    assert len(results) == 2


def test_tokenization_is_case_insensitive():

    tokens = MultimodalRetriever._tokenize(
        "Revenue, Growth!"
    )

    assert "revenue" in tokens

    assert "growth" in tokens

    assert "Revenue" not in tokens


def test_retrieval_preserves_original_metadata():

    index = [
        {
            "doc_id": "financial-table-1",
            "summary": (
                "Balance sheet showing assets "
                "and liabilities."
            ),
            "element_type": "table",
        }
    ]

    retriever = MultimodalRetriever(index)

    results = retriever.retrieve(
        "balance sheet assets"
    )

    assert results[0]["doc_id"] == (
        "financial-table-1"
    )

    assert results[0]["element_type"] == "table"

    assert "summary" in results[0]

    assert "score" in results[0]
