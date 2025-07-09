# config.py

"""
Configuration for models and RAG pipeline.
"""

# ALLaM Model Config
ALLaM_MODEL_NAME = "ALLaM-AI/ALLaM-7B-Instruct-preview"
ALLaM_MAX_NEW_TOKENS = 512
ALLaM_TEMPERATURE = 0.7
ALLaM_TOP_K = 50
ALLaM_TOP_P = 0.95

# Embedding Model
EMBEDDING_MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

# Similarity threshold
SIMILARITY_THRESHOLD = 0.2
