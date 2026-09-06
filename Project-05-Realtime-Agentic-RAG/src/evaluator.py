from typing import Dict, List


class RetrievalEvaluator:
    """
    Evaluates whether retrieved context is sufficiently relevant
    to the user's query before it is passed to generation.

    The prototype uses token-overlap scoring. A production
    implementation can replace this evaluator with an LLM-based
    relevance grader or a learned semantic scoring model.
    """

    def __init__(self, relevance_threshold: float = 0.2):
        if not 0.0 <= relevance_threshold <= 1.0:
            raise ValueError(
                "relevance_threshold must be between 0.0 and 1.0."
            )

        self.relevance_threshold = relevance_threshold

    @staticmethod
    def _tokenize(text: str) -> set:
        """
        Normalize text into searchable tokens.
        """

        return {
            token.strip(".,!?;:()[]{}")
            for token in text.lower().split()
            if token.strip(".,!?;:()[]{}")
        }

    def score(
        self,
        query: str,
        documents: List[Dict],
    ) -> float:
        """
        Calculate a normalized relevance score.

        The score represents the proportion of query tokens
        that appear in the retrieved context.

        Returns:
            A value between 0.0 and 1.0.
        """

        if not query or not query.strip():
            raise ValueError(
                "Query must not be empty."
            )

        if not documents:
            return 0.0

        query_tokens = self._tokenize(query)

        if not query_tokens:
            return 0.0

        document_text = " ".join(
            document.get("content", "")
            for document in documents
        )

        document_tokens = self._tokenize(
            document_text
        )

        overlap = query_tokens.intersection(
            document_tokens
        )

        return len(overlap) / len(query_tokens)

    def is_relevant(
        self,
        query: str,
        documents: List[Dict],
    ) -> bool:
        """
        Determine whether retrieved context passes
        the configured relevance threshold.
        """

        relevance_score = self.score(
            query=query,
            documents=documents,
        )

        return relevance_score >= self.relevance_threshold
