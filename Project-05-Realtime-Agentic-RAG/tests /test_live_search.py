from unittest.mock import MagicMock

import pytest

from src.live_search import LiveSearch


def test_live_search_requires_api_key():
    with pytest.raises(ValueError):
        LiveSearch("")


def test_live_search_returns_normalized_results():
    search = LiveSearch("test-key")

    search.client = MagicMock()

    search.client.search.return_value = {
        "results": [
            {
                "title": "AI News",
                "content": "Latest developments in AI.",
                "url": "https://example.com/ai",
                "score": 0.91,
            }
        ]
    }

    results = search.search(
        "latest AI news",
        max_results=1,
    )

    assert len(results) == 1
    assert results[0]["title"] == "AI News"
    assert results[0]["content"] == "Latest developments in AI."
    assert results[0]["url"] == "https://example.com/ai"
    assert results[0]["score"] == 0.91

    search.client.search.assert_called_once_with(
        query="latest AI news",
        max_results=1,
    )


def test_live_search_empty_query_raises_error():
    search = LiveSearch("test-key")

    with pytest.raises(ValueError):
        search.search("")


def test_live_search_invalid_result_limit_raises_error():
    search = LiveSearch("test-key")

    with pytest.raises(ValueError):
        search.search(
            "latest AI news",
            max_results=0,
        )
