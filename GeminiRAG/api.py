"""
FastAPI application exposing a RAG (Retrieval-Augmented Generation) API
based on CSV knowledge data.

This API allows users to submit a question and receive a generated answer
along with a similarity score computed from the knowledge base.
"""

from fastapi import FastAPI
from pydantic import BaseModel
from rag_model import RAGModel

app = FastAPI(title="CSV RAG API")

# Initialize RAG model and load CSV knowledge
rag = RAGModel()
rag.load_csv("arabic_data.csv")


class QueryRequest(BaseModel):
    """
    Request model for the /ask endpoint.

    Attributes:
        question (str): The user's question to be answered by the RAG model.
    """
    question: str


class QueryResponse(BaseModel):
    """
    Response model for the /ask endpoint.

    Attributes:
        answer (str): Generated answer text from the RAG model.
        similarity (float): Similarity score of the retrieved context (0.0 to 1.0).
    """
    answer: str
    similarity: float


@app.post("/ask", response_model=QueryResponse)
def ask_question(request: QueryRequest):
    """
    Endpoint to ask a question to the RAG model.

    Args:
        request (QueryRequest): Contains the user's question.

    Returns:
        QueryResponse: The generated answer and similarity score.
    """
    answer, score = rag.ask(request.question)
    return QueryResponse(answer=answer, similarity=score)
