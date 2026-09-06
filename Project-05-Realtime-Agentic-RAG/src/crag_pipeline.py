from typing import Any, Dict, List

from openai import OpenAI

from .evaluator import RetrievalEvaluator
from .live_search import LiveSearch
from .retriever import InternalRetriever
from .router import Route, SemanticRouter


class CRAGPipeline:
    """
    Corrective RAG pipeline combining:

    1. Dynamic query routing.
    2. Internal knowledge retrieval.
    3. Retrieval relevance evaluation.
    4. Live-search fallback when internal context is insufficient.
    5. Grounded answer generation.
    6. Basic hallucination checking against the selected context.
    """

    def __init__(
        self,
        api_key: str,
        live_search: LiveSearch,
        internal_retriever: InternalRetriever,
        evaluator: RetrievalEvaluator = None,
        router: SemanticRouter = None,
    ):
        self.client = OpenAI(
            api_key=api_key
        )

        self.live_search = live_search
        self.internal_retriever = internal_retriever

        self.evaluator = (
            evaluator
            if evaluator is not None
            else RetrievalEvaluator()
        )

        self.router = (
            router
            if router is not None
            else SemanticRouter()
        )

    def _retrieve_internal(
        self,
        query: str,
    ) -> List[Dict[str, Any]]:
        """
        Retrieve context from the internal knowledge store.
        """

        return self.internal_retriever.retrieve(
            query=query,
            top_k=3,
        )

    def _retrieve_live(
        self,
        query: str,
    ) -> List[Dict[str, Any]]:
        """
        Retrieve fresh external context.
        """

        return self.live_search.search(
            query=query,
            max_results=5,
        )

    @staticmethod
    def _format_context(
        documents: List[Dict[str, Any]],
    ) -> str:
        """
        Convert retrieved documents into a generation context.
        """

        if not documents:
            return "No supporting context was retrieved."

        sections = []

        for index, document in enumerate(
            documents,
            start=1,
        ):
            content = document.get(
                "content",
                "",
            )

            title = document.get(
                "title",
                document.get(
                    "document_id",
                    f"Source {index}",
                ),
            )

            url = document.get(
                "url",
                "",
            )

            source_header = f"[{index}] {title}"

            if url:
                source_header += f" ({url})"

            sections.append(
                f"{source_header}\n{content}"
            )

        return "\n\n".join(sections)

    def _generate(
        self,
        query: str,
        documents: List[Dict[str, Any]],
    ) -> str:
        """
        Generate an answer grounded in retrieved context.
        """

        context = self._format_context(
            documents
        )

        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a grounded RAG assistant. "
                        "Answer only from the supplied context. "
                        "If the context does not contain enough "
                        "evidence, explicitly say that the evidence "
                        "is insufficient. Do not invent facts."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"Question:\n{query}\n\n"
                        f"Supporting context:\n{context}"
                    ),
                },
            ],
            temperature=0.0,
        )

        return response.choices[0].message.content

    @staticmethod
    def _check_hallucination(
        answer: str,
        documents: List[Dict[str, Any]],
    ) -> bool:
        """
        Perform a lightweight grounding check.

        The prototype checks whether meaningful answer tokens
        have overlap with the retrieved evidence. This is not a
        replacement for an LLM-based faithfulness evaluator.
        """

        if not answer or not answer.strip():
            return False

        context = " ".join(
            document.get("content", "")
            for document in documents
        )

        answer_tokens = {
            token.strip(".,!?;:()[]{}")
            for token in answer.lower().split()
            if len(
                token.strip(".,!?;:()[]{}")
            ) > 3
        }

        context_tokens = {
            token.strip(".,!?;:()[]{}")
            for token in context.lower().split()
            if len(
                token.strip(".,!?;:()[]{}")
            ) > 3
        }

        if not answer_tokens:
            return False

        overlap = answer_tokens.intersection(
            context_tokens
        )

        return bool(overlap)

    def run(
        self,
        query: str,
    ) -> Dict[str, Any]:
        """
        Execute the complete Corrective RAG workflow.

        Returns:
            Dictionary containing the selected route,
            retrieval results, relevance information,
            fallback status, generated answer, and
            hallucination-check result.
        """

        if not query or not query.strip():
            raise ValueError(
                "Query must not be empty."
            )

        route = self.router.route(
            query
        )

        fallback_triggered = False

        if route == Route.LIVE:
            documents = self._retrieve_live(
                query
            )

            relevance_score = 1.0 if documents else 0.0

        else:
            documents = self._retrieve_internal(
                query
            )

            relevance_score = self.evaluator.score(
                query=query,
                documents=documents,
            )

            if not self.evaluator.is_relevant(
                query=query,
                documents=documents,
            ):
                documents = self._retrieve_live(
                    query
                )

                fallback_triggered = True

        if not documents:
            return {
                "route": route.value,
                "documents": [],
                "relevance_score": relevance_score,
                "fallback_triggered": fallback_triggered,
                "answer": (
                    "No sufficiently relevant evidence "
                    "was retrieved."
                ),
                "grounded": False,
            }

        answer = self._generate(
            query=query,
            documents=documents,
        )

        grounded = self._check_hallucination(
            answer=answer,
            documents=documents,
        )

        if not grounded:
            answer = (
                "The generated response failed the "
                "grounding check and was withheld."
            )

        return {
            "route": route.value,
            "documents": documents,
            "relevance_score": relevance_score,
            "fallback_triggered": fallback_triggered,
            "answer": answer,
            "grounded": grounded,
        }
