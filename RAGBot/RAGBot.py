import os
import re
import torch
import logging
import numpy as np
import pdfplumber

from sentence_transformers import SentenceTransformer, util, CrossEncoder
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from unsloth import FastLanguageModel

logging.getLogger("pdfminer").setLevel(logging.ERROR)


class RAGBot:
    
    # Model & Embedding Parameters 
    MODEL_ID = "unsloth/llama-3-8b-bnb-4bit"
    EMBEDDING_MODEL = "BAAI/bge-large-en-v1.5"
    SBERT_MODEL = "all-MiniLM-L6-v2"
    CROSS_ENCODER_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"

    # Generation Parameters 
    MAX_SEQ_LENGTH = 2048
    MAX_NEW_TOKENS = 256
    LOAD_IN_4BIT = True
    TEMPERATURE = 0.7

    # Similarity Thresholds 
    RETRIEVAL_THRESHOLD = 30.0
    TOP_K = 5

    def __init__(self):
        self.tokenizer = None
        self.model = None
        self.vector_db = None

        self.load_models()

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=400,
            chunk_overlap=50,
            separators=["\n\n", "\n", ". "]
        )

        self.embeddings = HuggingFaceEmbeddings(
            model_name=self.EMBEDDING_MODEL,
            model_kwargs={"device": "cuda" if torch.cuda.is_available() else "cpu"},
            encode_kwargs={"normalize_embeddings": True}
        )

        self.cross_encoder = CrossEncoder(self.CROSS_ENCODER_MODEL)
        self.sbert_model = SentenceTransformer(self.SBERT_MODEL)

    def load_models(self):
        self.model, self.tokenizer = FastLanguageModel.from_pretrained(
            model_name=self.MODEL_ID,
            max_seq_length=self.MAX_SEQ_LENGTH,
            load_in_4bit=self.LOAD_IN_4BIT,
        )

    def load_document(self, file_path):
        if file_path.endswith(".pdf"):
            with pdfplumber.open(file_path) as pdf:
                text = "\n".join([page.extract_text() or '' for page in pdf.pages])
        else:
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()

        if not text.strip():
            raise ValueError(" Document is empty or could not be parsed.")

        return text

    def create_vector_db(self, text):
        chunks = self.text_splitter.split_text(text)
        self.vector_db = FAISS.from_texts(chunks, self.embeddings, distance_strategy="METRIC_INNER_PRODUCT")

    def normalize_text(self, text):
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[\•\-\–\*]\s+', '', text)
        text = re.sub(r'\b\d+\.\s+', '', text)
        text = re.sub(r'\.(\S)', r'. \1', text)
        return text.strip()

    def extract_relevant_sentence(self, question, context):
        sentences = re.split(r'(?<=[.!?])\s+', context)
        question_keywords = set(re.findall(r'\w+', question.lower()))
        best_sent = ""
        best_score = 0
        for sent in sentences:
            sent_keywords = set(re.findall(r'\w+', sent.lower()))
            overlap = question_keywords & sent_keywords
            if len(overlap) > best_score:
                best_score = len(overlap)
                best_sent = sent
        return best_sent if best_sent else context

    def compute_semantic_similarity(self, text1, text2):
        emb1 = self.sbert_model.encode(text1, convert_to_tensor=True)
        emb2 = self.sbert_model.encode(text2, convert_to_tensor=True)
        return util.cos_sim(emb1, emb2).item()

    def retrieve_context(self, question):
        relevant_docs = self.vector_db.similarity_search_with_score(question, k=self.TOP_K)
        chunks = [doc.page_content for doc, _ in relevant_docs]

        pairs = [(question, chunk) for chunk in chunks]
        rerank_scores = self.cross_encoder.predict(pairs, batch_size=8)

        reranked = sorted(zip(chunks, rerank_scores), key=lambda x: x[1], reverse=True)
        top_chunk, top_score = reranked[0]
        confidence = 1 / (1 + np.exp(-top_score)) * 100

        if confidence < self.RETRIEVAL_THRESHOLD:
            return "No relevant clause found.", confidence

        return self.normalize_text(top_chunk), confidence

    def generate_answer(self, instruction, context):
        prompt = f"### Instruction:\n{instruction}\n\n### Input:\n{context}\n\n### Response:\n"
        inputs = self.tokenizer([prompt], return_tensors="pt").to(self.model.device)
        outputs = self.model.generate(
            **inputs,
            max_new_tokens=self.MAX_NEW_TOKENS,
            temperature=self.TEMPERATURE
        )
        answer = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        if "### Response:" in answer:
            answer = answer.split("### Response:")[-1].strip()

        return answer

    def answer_question(self, question):
        context, score = self.retrieve_context(question)
        if context == "No relevant clause found.":
            return "I couldn't find any relevant information.", score, 0.0

        short_context = self.extract_relevant_sentence(question, context)
        answer = self.generate_answer(question, short_context)
        semantic_sim = self.compute_semantic_similarity(question, answer)
        return answer, score, semantic_sim
