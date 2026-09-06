from typing import Dict, List


class InternalRetriever:
    """
    Lightweight internal knowledge retriever.

    The prototype uses token-overlap scoring over an in-memory
    collection of knowledge chunks. The retrieval interface can
    later be replaced by FAISS, Pinecone, or another vector store
    without changing the CRAG pipeline.
    """

    def __init__(self, documents: List[Dict] = None):
        self.documents = documents or []

    @staticmethod
    def _tokenize(text: str) -> set:
        """
        Normalize text into a set of searchable tokens.
        """

        return {
            token.strip(".,!?;:()[]{}")
            for token in text.lower().split()
            if token.strip(".,!?;:()[]{}")
        }

    def add_document(
        self,
        document_id: str,
        content: str,
        metadata: Dict = None,
    ) -> None:
        """
        Add a knowledge chunk to the internal collection.
        """

        if not document_id:
            raise ValueError(
                "document_id must not be empty."
            )

        if not content or not content.strip():
            raise ValueError(
                "content must not be empty."
            )

        self.documents.append(
            {
                "document_id": document_id,
                "content": content,
                "metadata": metadata or {},
            }
        )

    def retrieve(
        self,
        query: str,
        top_k: int = 3,
    ) -> List[Dict]:
        """
        Retrieve the most relevant internal knowledge chunks.

        Args:
            query: User's search query.
            top_k: Maximum number of chunks to return.

        Returns:
            Ranked retrieval results containing a relevance score.
        """

        if not query or not query.strip():
            raise ValueError(
                "Query must not be empty."
            )

        if top_k < 1:
            raise ValueError(
                "top_k must be greater than or equal to 1."
            )

        if not self.documents:
            return []

        query_tokens = self._tokenize(query)

        scored_results = []

        for document in self.documents:
            document_tokens = self._tokenize(
                document["content"]
            )

            overlap = query_tokens.intersection(
                document_tokens
            )

            score = len(overlap)

            scored_results.append(
                {
                    **document,
                    "score": score,
                }
            )

        scored_results.sort(
            key=lambda item: item["score"],
            reverse=True,
        )

        return scored_results[:top_k]
