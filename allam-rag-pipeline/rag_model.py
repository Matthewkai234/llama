# rag_model.py

"""
Orchestrates the full RAG pipeline using vector store and ALLaM generation.
"""

from vector import VectorStore
from allam import ALLaMModel


class RAGModel:
    """
    End-to-end RAG system: retrieve + generate.
    """

    def __init__(self):
        self.vector_store = VectorStore()
        self.allam = ALLaMModel()

    def load_csv(self, file_path: str):
        """
        Loads and embeds a CSV file.
        """
        self.vector_store.load_csv(file_path)

    def ask(self, question: str) -> tuple[str, str]:
        """
        Processes the question and returns generated answer and similarity score.
        """
        context, score = self.vector_store.retrieve(question)
        if context is None:
            return " No relevant context found", f"Similarity: {score:.2f}"

        answer = self.allam.generate(question, context)
        return answer, f"Similarity: {score:.2f}"
