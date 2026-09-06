from typing import Dict, List


class MultimodalRetriever:
    """
    Lightweight semantic retrieval layer for multimodal RAG.

    The retriever searches textual summaries associated with
    visual assets and returns the corresponding parent document
    identifiers.

    This prototype uses simple keyword-overlap scoring.
    A production implementation can replace this layer with
    embeddings and a vector database such as FAISS or Pinecone.
    """

    def __init__(
        self,
        vector_index: List[Dict],
    ):
        self.vector_index = vector_index

    @staticmethod
    def _tokenize(text: str) -> set:
        """
        Convert text into a normalized set of tokens.
        """

        return {
            token.strip(".,!?;:()[]{}")
            for token in text.lower().split()
            if token.strip(".,!?;:()[]{}")
        }

    def retrieve(
        self,
        query: str,
        top_k: int = 1,
    ) -> List[Dict]:
        """
        Retrieve the most relevant visual summaries.

        Args:
            query: User's semantic search query.
            top_k: Maximum number of results.

        Returns:
            Ranked retrieval results.
        """

        if not self.vector_index:
            return []

        query_tokens = self._tokenize(query)

        scored_results = []

        for item in self.vector_index:

            summary_tokens = self._tokenize(
                item.get("summary", "")
            )

            score = len(
                query_tokens.intersection(
                    summary_tokens
                )
            )

            scored_results.append(
                {
                    **item,
                    "score": score,
                }
            )

        scored_results.sort(
            key=lambda item: item["score"],
            reverse=True,
        )

        return scored_results[:top_k]
