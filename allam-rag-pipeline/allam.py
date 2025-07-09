# ALLaM.py

"""
Loads the ALLaM model and performs generation using given context and question.
"""

from transformers import AutoModelForCausalLM, AutoTokenizer
from config import (
    ALLaM_MODEL_NAME,
    ALLaM_MAX_NEW_TOKENS,
    ALLaM_TEMPERATURE,
    ALLaM_TOP_K,
    ALLaM_TOP_P
)
import torch


class ALLaMModel:
    """
    ALLaM model wrapper to handle loading and generation.
    """

    def __init__(self):
        self.model = AutoModelForCausalLM.from_pretrained(
            ALLaM_MODEL_NAME,
            device_map="auto",
            torch_dtype=torch.float16
        )
        self.tokenizer = AutoTokenizer.from_pretrained(ALLaM_MODEL_NAME)

    def generate(self, question: str, context: str) -> str:
        """
        Generates an answer using the given question and context.
        """
        messages = [{"role": "user", "content": f"السياق:\n{context}\n\nالسؤال:\n{question}"}]
        input_text = self.tokenizer.apply_chat_template(messages, tokenize=False)
        inputs = self.tokenizer(input_text, return_tensors='pt', return_token_type_ids=False)
        inputs = {k: v.to(self.model.device) for k, v in inputs.items()}

        output = self.model.generate(
            **inputs,
            max_new_tokens=ALLaM_MAX_NEW_TOKENS,
            temperature=ALLaM_TEMPERATURE,
            top_k=ALLaM_TOP_K,
            top_p=ALLaM_TOP_P
        )

        decoded = self.tokenizer.decode(output[0], skip_special_tokens=True)
        return decoded.split('[/INST]', 1)[-1].strip() if '[/INST]' in decoded else decoded.strip()
