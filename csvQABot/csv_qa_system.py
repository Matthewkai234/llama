import pandas as pd
import torch
import re
from transformers import AutoModelForCausalLM, AutoTokenizer
from sentence_transformers import SentenceTransformer, util


class CSVQASystem:
    """
    A system that answers user questions based on the content of a CSV file using a language model (ALLaM)
    and semantic similarity from SentenceTransformer.
    """

    def __init__(
        self,
        language_model_name: str = "ALLaM-AI/ALLaM-7B-Instruct-preview",
        embedding_model_name: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
        similarity_threshold: float = 0.5,
        max_new_tokens: int = 512,
        temperature: float = 0.7,
        top_k: int = 50,
        top_p: float = 0.95,
    ):
        """
        Initialize models for QA and embedding.

        Args:
            language_model_name (str): Hugging Face model name for language generation.
            embedding_model_name (str): SentenceTransformer model name for embeddings.
            similarity_threshold (float): Minimum cosine similarity required to use a chunk.
            max_new_tokens (int): Maximum tokens in the generated response.
            temperature (float): Sampling temperature for generation.
            top_k (int): Top-k filtering parameter.
            top_p (float): Nucleus sampling parameter.
        """
        self.similarity_threshold = similarity_threshold
        self.max_new_tokens = max_new_tokens
        self.temperature = temperature
        self.top_k = top_k
        self.top_p = top_p

        # Load language model and tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(language_model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            language_model_name, device_map="auto", torch_dtype=torch.float16
        )

        # Load embedding model
        self.embedding_model = SentenceTransformer(embedding_model_name)

    def csv_to_paragraphs(self, file_path: str) -> list[str]:
        """
            Reads a CSV file and converts each row into a readable paragraph.

            Tries UTF-8 encoding first, then Windows-1256 for Arabic files.

            Args:
                file_path (str): Path to the CSV file.

            Returns:
                List[str]: Paragraphs representing each row.
        """
        try:
            # Attempt to read using UTF-8 encoding
            df = pd.read_csv(file_path, encoding='utf-8')
        except UnicodeDecodeError:
            # Retry using Windows-1256 encoding (often used for Arabic files)
            df = pd.read_csv(file_path, encoding='windows-1256')

        chunks = []
        for _, row in df.iterrows():
            # Format each row as: "column1: value1 - column2: value2 - ..."
            text = " - ".join([f"{col.strip()}: {str(row[col])}" for col in df.columns])
            # Remove excessive whitespace
            clean_text = re.sub(r'\s+', ' ', text.strip())
            chunks.append(clean_text)

        return chunks

    def get_best_chunk(self, question: str, chunks: list[str]) -> tuple[str | None, float]:
        """
        Find the most semantically similar chunk to the question.

        Args:
            question (str): User's question.
            chunks (list): List of paragraph strings from the CSV.

        Returns:
            Tuple containing best matching chunk or None, and its similarity score.
        """
        q_emb = self.embedding_model.encode(question, convert_to_tensor=True)
        chunks_emb = self.embedding_model.encode(chunks, convert_to_tensor=True)
        scores = util.cos_sim(q_emb, chunks_emb)[0]

        best_idx = torch.argmax(scores).item()
        best_score = scores[best_idx].item()

        if best_score < self.similarity_threshold:
            return None, best_score

        return chunks[best_idx], best_score

    def generate_answer(self, question: str, context: str) -> str:
        """
        Generate an answer from the ALLaM model based on context and question.

        Args:
            question (str): The question asked.
            context (str): The relevant CSV text chunk.

        Returns:
            Model's answer as a string.
        """
        messages = [
            {"role": "user", "content": f"السياق:\n{context}\n\nالسؤال:\n{question}"}
        ]

        input_text = self.tokenizer.apply_chat_template(messages, tokenize=False)
        inputs = self.tokenizer(input_text, return_tensors='pt', return_token_type_ids=False)
        device = self.model.device
        inputs = {k: v.to(device) for k, v in inputs.items()}

        output = self.model.generate(
            **inputs,
            max_new_tokens=self.max_new_tokens,
            temperature=self.temperature,
            top_k=self.top_k,
            top_p=self.top_p
        )

        decoded = self.tokenizer.decode(output[0], skip_special_tokens=True)

        # Extract answer portion after [/INST] if exists
        if '[/INST]' in decoded:
            decoded = decoded.split('[/INST]', 1)[-1].strip()

        return decoded

    def answer_question_from_csv(self, csv_path: str, question: str) -> tuple[str, str]:
        """
        The main pipeline that loads CSV, finds relevant content, and generates an answer.

        Args:
            csv_path (str): Path to the uploaded CSV file.
            question (str): The user's question.

        Returns:
            A tuple with the answer and similarity score string.
        """
        try:
            chunks = self.csv_to_paragraphs(csv_path)
            best_chunk, score = self.get_best_chunk(question, chunks)

            if best_chunk is None:
                return "❌ No relevant information found.", f"Similarity: {score:.2f}"

            answer = self.generate_answer(question, best_chunk)
            return answer, f"Similarity: {score:.2f}"
        except Exception as e:
            return f"⚠️ Error: {str(e)}", ""
