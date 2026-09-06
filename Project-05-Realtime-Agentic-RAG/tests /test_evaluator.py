import pytest

from src.evaluator import RetrievalEvaluator


def test_relevant_documents_pass_threshold():
    evaluator = RetrievalEvaluator(
        relevance_threshold=0.5
    )

    documents = [
        {
            "content": (
                "The deployment process uses Docker "
                "containers for production."
            )
        }
    ]

    assert evaluator.is_relevant(
        "deployment Docker",
        documents,
    )


def test_irrelevant_documents_fail_threshold():
    evaluator = RetrievalEvaluator(
        relevance_threshold=0.5
    )

    documents = [
        {
            "content": (
                "The finance team manages quarterly "
                "financial reports."
            )
        }
    ]

    assert not evaluator.is_relevant(
        "deployment Docker",
        documents,
    )


def test_empty_documents_return_zero_score():
    evaluator = RetrievalEvaluator()

    score = evaluator.score(
        "deployment process",
        [],
    )

    assert score == 0.0


def test_relevance_score_is_normalized():
    evaluator = RetrievalEvaluator()

    documents = [
        {
            "content": (
                "The deployment process uses Docker."
            )
        }
    ]

    score = evaluator.score(
        "deployment Docker unknown",
        documents,
    )

    assert 0.0 <= score <= 1.0
    assert score == pytest.approx(2 / 3)


def test_empty_query_raises_error():
    evaluator = RetrievalEvaluator()

    with pytest.raises(ValueError):
        evaluator.score(
            "",
            [],
        )


def test_invalid_threshold_raises_error():
    with pytest.raises(ValueError):
        RetrievalEvaluator(
            relevance_threshold=1.5
        )
