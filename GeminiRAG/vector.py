# vector.py

"""
Handles text embedding and FAISS vector store for similarity-based retrieval.
"""
from langchain_community.vectorstores import FAISS
from langchain_community.vectorstores.faiss import DistanceStrategy
from langchain_huggingface import HuggingFaceEmbeddings
from config import EMBEDDING_MODEL_NAME, SIMILARITY_THRESHOLD
from utils import csv_to_paragraphs
import torch


class VectorStore:
    """
    A wrapper around FAISS for building and querying a vector store 
    using HuggingFace embeddings.
    """

    def __init__(self):
        """
        Initializes the vector store with a HuggingFace embedding model.

        The embedding model is loaded onto GPU if available, otherwise CPU.
        The FAISS vector database is initialized as None and will be created
        when CSV data is loaded.
        """

        self.embedding_model = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL_NAME,
            model_kwargs={"device": "cuda" if torch.cuda.is_available() else "cpu"},
            encode_kwargs={"normalize_embeddings": True}
        )
        self.vector_db = None

    def load_csv(self, file_path: str):
        """
        Loads a CSV file and builds a FAISS vector database.

        Each row in the CSV is converted into a text paragraph, embedded using 
        the HuggingFace embedding model, and stored in the FAISS index.

        Args:
            file_path (str): Path to the CSV file containing knowledge data.
        """
        paragraphs = csv_to_paragraphs(file_path)
        self.vector_db = FAISS.from_texts(
            paragraphs,
            self.embedding_model,
            distance_strategy=DistanceStrategy.COSINE
        )

    def retrieve(self, query: str) -> tuple[str, float]:
        """
        Retrieves the most relevant paragraph(s) for a given query.

        Performs a similarity search in the FAISS vector database and returns
        the top results joined by separators, along with the similarity score 
        of the most relevant paragraph.

        Args:
            query (str): The input query to search in the vector store.

        Returns:
            tuple[str | None, float]: 
                - str | None: Joined text of the most relevant paragraphs if found; 
                  otherwise None if the vector store is empty or no results.
                - float: Similarity score of the top paragraph (0.0 to 1.0).
        """
        if not self.vector_db:
            return None, 0.0

        docs = self.vector_db.similarity_search_with_score(query, k=5)
        if not docs:
            return None, 0.0
        contexts = [d[0].page_content for d in docs]
        joined_context = "\n---\n".join(contexts)
        similarity = 1 - docs[0][1] 
        return joined_context, similarity
