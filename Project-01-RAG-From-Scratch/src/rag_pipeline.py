import os
import numpy as np
import faiss
from typing import List, Dict, Any
from langchain_text_splitters import RecursiveCharacterTextSplitter
from openai import OpenAI


class ScratchRAGPipeline:
    def __init__(
        self,
        openai_api_key: str,
        embedding_model: str = "text-embedding-3-small"
    ):
        self.client = OpenAI(api_key=openai_api_key)
        self.model = embedding_model
        self.dimension = 1536

        # Inner Product on normalized vectors = Cosine Similarity
        self.index = faiss.IndexFlatIP(self.dimension)

        self.documents: List[str] = []

    def _get_embedding(self, texts: List[str]) -> np.ndarray:
        response = self.client.embeddings.create(
            input=texts,
            model=self.model
        )

        embeddings = [item.embedding for item in response.data]

        norm_embeddings = np.array(
            embeddings,
            dtype=np.float32
        )

        faiss.normalize_L2(norm_embeddings)

        return norm_embeddings

    def ingest_document(
        self,
        text: str,
        chunk_size: int = 600,
        chunk_overlap: int = 100
    ):
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ". ", " ", ""]
        )

        chunks = splitter.split_text(text)

        self.documents.extend(chunks)

        embeddings = self._get_embedding(chunks)

        self.index.add(embeddings)

        print(
            f"[Ingestion] Added {len(chunks)} chunks to FAISS Index."
        )

    def retrieve(
        self,
        query: str,
        top_k: int = 4
    ) -> List[Dict[str, Any]]:
        query_vec = self._get_embedding([query])

        distances, indices = self.index.search(
            query_vec,
            top_k
        )

        results = []

        for dist, idx in zip(
            distances[0],
            indices[0]
        ):
            if idx != -1:
                results.append(
                    {
                        "chunk": self.documents[idx],
                        "score": float(dist)
                    }
                )

        return results

    def query(
        self,
        user_query: str,
        top_k: int = 4
    ) -> str:
        retrieved_chunks = self.retrieve(
            user_query,
            top_k=top_k
        )

        context = "\n\n---\n\n".join(
            [r["chunk"] for r in retrieved_chunks]
        )

        prompt = (
            f"CONTEXT:\n{context}\n\n"
            f"QUERY: {user_query}\n"
            f"ANSWER:"
        )

        completion = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.0
        )

        return completion.choices[0].message.content
