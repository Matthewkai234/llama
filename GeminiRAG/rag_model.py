# rag_model.py

"""
Orchestrates the full RAG (Retrieval-Augmented Generation) pipeline using a vector store
for retrieval and the gemini model for answer generation.
"""

from vector import VectorStore
from gemini_model import GeminiModel


class RAGModel:
    """
    End-to-end RAG system: retrieve relevant context and generate an answer.
    """

    def __init__(self):
        """
        Initializes the RAGModel.

        Creates instances of the vector store for retrieval
        and the gemini model for text generation.
        """
        self.vector_store = VectorStore()
        self.model = GeminiModel()

    def load_csv(self, file_path: str):
        """
        Loads and embeds a CSV file into the vector store.

        Args:
            file_path (str): Path to the CSV file containing knowledge data.
        """
        self.vector_store.load_csv(file_path)

    def ask(self, question: str) -> tuple[str, str]:

        """
        Processes the input question by retrieving relevant context
        and generating an answer using the Gemini model.

        Args:
            question (str): The input question to be answered.

        Returns:
            tuple[str, str]:
                - str: Generated answer text, or a message if no relevant context found.
                - str: Similarity score formatted as a string with 2 decimal places.
        """
        
        context, score = self.vector_store.retrieve(question)
        if context is None:
            return " No relevant context found", f"Similarity: {score:.2f}"

        answer = self.model.generate(question, context)
        return answer, score 

