# vector.py

"""
Handles text embedding and FAISS vector store for similarity retrieval.
"""

from langchain_community.vectorstores import FAISS
from langchain_community.vectorstores.faiss import DistanceStrategy
from langchain_huggingface import HuggingFaceEmbeddings
from config import EMBEDDING_MODEL_NAME, SIMILARITY_THRESHOLD
from utils import csv_to_paragraphs
import torch


class VectorStore:
    """
    Builds and queries a FAISS vector store from CSV content.
    """

    def __init__(self):
        self.embedding_model = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL_NAME,
            model_kwargs={"device": "cuda" if torch.cuda.is_available() else "cpu"},
            encode_kwargs={"normalize_embeddings": True}
        )
        self.vector_db = None

    def load_csv(self, file_path: str):
        """
        Converts CSV into vector DB by creating paragraph embeddings.
        """
        paragraphs = csv_to_paragraphs(file_path)
        self.vector_db = FAISS.from_texts(
            paragraphs,
            self.embedding_model,
            distance_strategy=DistanceStrategy.COSINE
        )

    def retrieve(self, query: str) -> tuple[str, float]:
        """
        Retrieves the most relevant paragraph for a given query.
        
        Returns:
            (content, similarity) or (None, 0.0) if not found or too dissimilar.
        """
        if not self.vector_db:
            return None, 0.0

        docs = self.vector_db.similarity_search_with_score(query, k=3)
        if not docs:
            return None, 0.0

        doc, distance = docs[0]
        similarity = 1 - distance
        if similarity < SIMILARITY_THRESHOLD:
            return None, similarity

        return doc.page_content, similarity
