from unittest.mock import MagicMock

import pytest

from src.cache import SemanticCache


def test_cache_requires_positive_ttl():
    with pytest.raises(ValueError):
        SemanticCache(
            redis_url="redis://localhost:6379",
            ttl_seconds=0,
        )


def test_query_normalization():
    cache = SemanticCache()

    assert cache._normalize_query(
        "  What   is   AI?  "
    ) == "what is ai?"


def test_equivalent_queries_generate_same_key():
    cache = SemanticCache()

    key_one = cache._cache_key(
        "What is AI?"
    )

    key_two = cache._cache_key(
        "  what   is   ai? "
    )

    assert key_one == key_two


def test_cache_get_returns_stored_response():
    cache = SemanticCache()

    cache.client = MagicMock()

    cache.client.get.return_value = (
        '{"answer": "Cached response"}'
    )

    result = cache.get(
        "What is AI?"
    )

    assert result == {
        "answer": "Cached response"
    }


def test_cache_get_returns_none_on_miss():
    cache = SemanticCache()

    cache.client = MagicMock()

    cache.client.get.return_value = None

    result = cache.get(
        "What is AI?"
    )

    assert result is None


def test_cache_set_stores_response_with_ttl():
    cache = SemanticCache(
        ttl_seconds=1800
    )

    cache.client = MagicMock()

    response = {
        "answer": "Cached response"
    }

    cache.set(
        "What is AI?",
        response,
    )

    cache.client.setex.assert_called_once()

    args = cache.client.setex.call_args.args

    assert args[0] == cache._cache_key(
        "What is AI?"
    )

    assert args[1] == 1800
    assert '"answer": "Cached response"' in args[2]


def test_cache_delete_removes_key():
    cache = SemanticCache()

    cache.client = MagicMock()

    cache.delete(
        "What is AI?"
    )

    cache.client.delete.assert_called_once_with(
        cache._cache_key(
            "What is AI?"
        )
    )


def test_cache_clear_removes_crag_keys():
    cache = SemanticCache()

    cache.client = MagicMock()

    cache.client.keys.return_value = [
        "crag:response:key1",
        "crag:response:key2",
    ]

    cache.clear()

    cache.client.delete.assert_called_once_with(
        "crag:response:key1",
        "crag:response:key2",
    )


def test_empty_query_raises_error():
    cache = SemanticCache()

    with pytest.raises(ValueError):
        cache.get("")
