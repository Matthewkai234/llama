# main.py

"""
Runs an example question through the RAG model using a CSV file.
"""

from rag_model import RAGModel

if __name__ == "__main__":
    rag = RAGModel()
    rag.load_csv("data.csv") 

    question =" your question "
    answer, score = rag.ask(question)

    print("Question:", question)
    print("Answer:", answer)
    print("Similarity", score)
