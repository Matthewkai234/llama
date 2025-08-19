# config.py

"""
Configuration module for the embedding model and similarity threshold.

This module defines constants used in the RAG pipeline to configure:
    - The embedding model for converting text to vectors.
    - The similarity threshold for considering a match relevant during retrieval.

Constants:
    EMBEDDING_MODEL_NAME (str): Name of the HuggingFace embedding model to use.
    SIMILARITY_THRESHOLD (float): Minimum similarity score (0.0 to 1.0) to consider
        a retrieved vector as relevant.
"""

# Embedding Model
EMBEDDING_MODEL_NAME = "mixedbread-ai/mxbai-embed-large-v1"  

# Similarity threshold
SIMILARITY_THRESHOLD = 0.3  # Minimum similarity score to consider a match relevant.
