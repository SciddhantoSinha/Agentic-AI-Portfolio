from typing import Any, Dict, List

from tavily import TavilyClient


class LiveSearch:
    """
    Wrapper around Tavily for retrieving fresh external
    information when internal knowledge is insufficient
    or when a query requires current information.
    """

    def __init__(self, api_key: str):
        if not api_key or not api_key.strip():
            raise ValueError(
                "TAVILY_API_KEY must not be empty."
            )

        self.client = TavilyClient(
            api_key=api_key
        )

    def search(
        self,
        query: str,
        max_results: int = 5,
    ) -> List[Dict[str, Any]]:
        """
        Execute a live web search.

        Args:
            query: User's search query.
            max_results: Maximum number of results.

        Returns:
            A normalized list of search results.
        """

        if not query or not query.strip():
            raise ValueError(
                "Query must not be empty."
            )

        if max_results < 1:
            raise ValueError(
                "max_results must be greater than or equal to 1."
            )

        response = self.client.search(
            query=query,
            max_results=max_results,
        )

        results = response.get(
            "results",
            [],
        )

        return [
            {
                "title": result.get(
                    "title",
                    "",
                ),
                "content": result.get(
                    "content",
                    "",
                ),
                "url": result.get(
                    "url",
                    "",
                ),
                "score": result.get(
                    "score",
                    0.0,
                ),
            }
            for result in results
        ]
