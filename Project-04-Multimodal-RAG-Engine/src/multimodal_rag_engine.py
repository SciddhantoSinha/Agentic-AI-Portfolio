import base64
import uuid
from typing import Dict, List

from openai import OpenAI

from .retriever import MultimodalRetriever


class MultimodalRAGEngine:
    """
    Multimodal RAG engine using dual-representation indexing.

    Visual assets are:
    1. Summarized by a vision-capable LLM.
    2. Stored as raw base64 data in a document store.
    3. Represented by textual summaries for semantic retrieval.
    4. Retrieved through their summary representation.
    5. Resolved back to the original visual asset for generation.
    """

    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)

        self.docstore: Dict[str, Dict] = {}
        self.vector_index: List[Dict] = []

        self.retriever = MultimodalRetriever(
            self.vector_index
        )

    @staticmethod
    def _encode_image_b64(
        image_bytes: bytes,
    ) -> str:
        return base64.b64encode(
            image_bytes
        ).decode("utf-8")

    def summarize_visual_element(
        self,
        image_bytes: bytes,
        element_type: str = "chart",
    ) -> str:

        b64_img = self._encode_image_b64(
            image_bytes
        )

        prompt = (
            f"Analyze this {element_type}. "
            "Detail all important data points, trends, "
            "relationships, columns, labels, and "
            "structural information so the description "
            "can be used for dense semantic retrieval."
        )

        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt,
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": (
                                    "data:image/png;base64,"
                                    f"{b64_img}"
                                )
                            },
                        },
                    ],
                }
            ],
            max_tokens=500,
        )

        return response.choices[0].message.content

    def ingest_image_element(
        self,
        image_bytes: bytes,
        element_type: str = "chart",
    ) -> str:

        doc_id = str(uuid.uuid4())

        summary = self.summarize_visual_element(
            image_bytes=image_bytes,
            element_type=element_type,
        )

        self.docstore[doc_id] = {
            "type": "image",
            "element_type": element_type,
            "b64": self._encode_image_b64(
                image_bytes
            ),
        }

        self.vector_index.append(
            {
                "doc_id": doc_id,
                "summary": summary,
                "element_type": element_type,
            }
        )

        return doc_id

    def retrieve_visual_context(
        self,
        user_query: str,
        top_k: int = 1,
    ) -> List[Dict]:
        """
        Retrieve visual elements using their textual
        summary representations.
        """

        return self.retriever.retrieve(
            query=user_query,
            top_k=top_k,
        )

    def query_multimodal(
        self,
        user_query: str,
    ) -> str:

        if not self.vector_index:
            raise ValueError(
                "No visual elements have been indexed."
            )

        results = self.retrieve_visual_context(
            user_query=user_query,
            top_k=1,
        )

        if not results:
            raise ValueError(
                "No relevant visual elements found."
            )

        matched_doc_id = results[0]["doc_id"]

        raw_asset = self.docstore[
            matched_doc_id
        ]

        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": (
                                "Answer the following query "
                                "using the provided visual "
                                "context:\n\n"
                                f"{user_query}"
                            ),
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": (
                                    "data:image/png;base64,"
                                    f"{raw_asset['b64']}"
                                )
                            },
                        },
                    ],
                }
            ],
        )

        return response.choices[0].message.content
