from enum import Enum


class Route(str, Enum):
    INTERNAL = "INTERNAL"
    LIVE = "LIVE"


class SemanticRouter:
    """
    Routes incoming queries toward either:
    1. Internal knowledge retrieval.
    2. Live external search.

    This prototype uses deterministic semantic signals so that
    routing behavior remains transparent and easy to test.
    A production implementation can replace the routing logic
    with an embedding-based semantic router.
    """

    LIVE_TERMS = {
        "latest",
        "today",
        "current",
        "now",
        "recent",
        "breaking",
        "live",
        "weather",
        "stock",
        "stocks",
        "price",
        "news",
        "market",
        "temperature",
    }

    def route(self, query: str) -> Route:
        """
        Determine the appropriate retrieval route.

        Args:
            query: User's natural-language query.

        Returns:
            Route.INTERNAL or Route.LIVE.
        """

        if not query or not query.strip():
            raise ValueError("Query must not be empty.")

        normalized_query = query.lower()

        tokens = {
            token.strip(".,!?;:()[]{}")
            for token in normalized_query.split()
        }

        if tokens.intersection(self.LIVE_TERMS):
            return Route.LIVE

        return Route.INTERNAL
