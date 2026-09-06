import hashlib
import json
from typing import Any, Optional

import redis


class SemanticCache:
    """
    Redis-backed cache for previously generated responses.

    This prototype uses normalized-query hashing as the cache key.
    A production implementation can replace the keying strategy
    with embedding-based cosine similarity to support true
    semantic-cache matching.
    """

    def __init__(
        self,
        redis_url: str = "redis://localhost:6379",
        ttl_seconds: int = 3600,
    ):
        if ttl_seconds < 1:
            raise ValueError(
                "ttl_seconds must be greater than 0."
            )

        self.client = redis.from_url(
            redis_url,
            decode_responses=True,
        )

        self.ttl_seconds = ttl_seconds

    @staticmethod
    def _normalize_query(
        query: str,
    ) -> str:
        """
        Normalize a query before generating its cache key.
        """

        if not query or not query.strip():
            raise ValueError(
                "Query must not be empty."
            )

        return " ".join(
            query.lower().strip().split()
        )

    @classmethod
    def _cache_key(
        cls,
        query: str,
    ) -> str:
        """
        Generate a deterministic Redis key for a query.
        """

        normalized_query = cls._normalize_query(
            query
        )

        digest = hashlib.sha256(
            normalized_query.encode("utf-8")
        ).hexdigest()

        return f"crag:response:{digest}"

    def get(
        self,
        query: str,
    ) -> Optional[dict]:
        """
        Retrieve a cached response if available.
        """

        key = self._cache_key(
            query
        )

        cached_value = self.client.get(
            key
        )

        if cached_value is None:
            return None

        return json.loads(
            cached_value
        )

    def set(
        self,
        query: str,
        response: dict[str, Any],
    ) -> None:
        """
        Store a response in Redis with a time-to-live.
        """

        key = self._cache_key(
            query
        )

        self.client.setex(
            key,
            self.ttl_seconds,
            json.dumps(response),
        )

    def delete(
        self,
        query: str,
    ) -> None:
        """
        Remove a cached response.
        """

        key = self._cache_key(
            query
        )

        self.client.delete(
            key
        )

    def clear(
        self,
    ) -> None:
        """
        Remove all CRAG response cache entries.

        This uses the configured CRAG key namespace rather than
        flushing the entire Redis database.
        """

        keys = self.client.keys(
            "crag:response:*"
        )

        if keys:
            self.client.delete(
                *keys
            )
