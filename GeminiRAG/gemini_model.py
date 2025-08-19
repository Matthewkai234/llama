#gemini_model
"""
Loads the Gemini model and performs generation using given context and question.

"""

import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()


class GeminiModel:
    """Wrapper class for Google Gemini Flash model.

    This class provides an interface to the Google Gemini Flash model,
    configured with an API key from environment variables, to generate
    text responses based on a given context and question.
    """

    def __init__(self, model_name: str = "gemini-2.0-flash"):
        """Initializes the GeminiModel.

        Args:
            model_name (str, optional): Name of the Gemini model to use.
                Defaults to "gemini-2.0-flash".

        Raises:
            ValueError: If the environment variable `GEMINI_API_KEY`
                is not set in `.env` or system environment.
        """
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found. Set it via setx or .env")

        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(
            model_name=model_name,
            generation_config={
                "temperature": 0.7,
                "max_output_tokens": 512,
            },
        )

    def generate(self, question: str, context: str) -> str:
        """Generates a response from the Gemini Flash model.

        Args:
            question (str): The user question to be answered.
            context (str): The supporting context retrieved from the CSV
                or other knowledge source.

        Returns:
            str: The generated answer text from the model.
        """
        prompt = f"""السياق:
{context}

السؤال:
{question}
"""
        resp = self.model.generate_content(prompt)
        return (resp.text or "").strip()
