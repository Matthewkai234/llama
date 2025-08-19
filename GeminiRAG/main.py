
# main.py

"""
Main script to demonstrate the RAG model pipeline.

This script performs the following:
    - Loads a CSV file as the knowledge base.
    - Asks a question using the RAG pipeline.
    - Prints the question, the generated answer, and the similarity score.

Example:
    Run the script directly:
        $ python main.py
"""


from rag_model import RAGModel

if __name__ == "__main__":
    rag = RAGModel()
    rag.load_csv("data.csv")

    question =" your question "
    answer, score = rag.ask(question)

    print("Question:", question)
    print("Answer:", answer)
    print("Similarity:", f"{score:.2f}")

