
#  RAG Module – Retrieval-Augmented Generation with ALLaM

This project demonstrates a complete **Retrieval-Augmented Generation (RAG)** pipeline using a local CSV knowledge base. It combines a semantic search engine with a powerful language model (ALLaM-7B) to answer user questions based on the information in your CSV files.

---

##  What It Does

1. **Reads a CSV file** (e.g., a dataset, report, or table).
2. **Converts each row into a text paragraph.**
3. **Creates embeddings** (numeric representations) for all paragraphs using `sentence-transformers`.
4. **Performs semantic search** to find the most relevant paragraph for a user’s question.
5. **Generates an answer** using the ALLaM-7B language model with the retrieved paragraph as context.

---

##  Project Structure

```
rag_module/
├── ALLaM.py              # Loads and uses the ALLaM-7B model
├── config.py             # Configuration file (model names, parameters, thresholds)
├── main.py               # Entry point: runs a sample question
├── rag_model.py          # Main RAG pipeline (retrieve + generate)
├── requirements.txt      # Python dependencies
├── utils.py              # Converts CSV rows into paragraph text
├── vector.py             # Vector store logic using FAISS
```

---

##  Getting Started

You can run this project locally or in **Google Colab**.

###  Requirements

- Python 3.9+
- A GPU (recommended for running ALLaM efficiently)

###  Installation

1. **Clone or upload the repo:**

```bash
git clone https://github.com/your-username/allam-rag-pipeline.git
cd allam-rag-pipeline
```

2. **Install dependencies:**

```bash
pip install -r requirements.txt
```

3. **Prepare your data:**

Put your CSV file in the same directory and name it `data.csv`, or change the path in `main.py`.

4. **Run the pipeline:**

```bash
python main.py
```

---

##  Example Output

```
Question: your question
Answer: ...generated answer...
Similarity: 0.85
```

If no relevant context is found, the model will respond with:

```
No relevant context found
```

---

##  Customization

You can modify parameters like model names, temperature, or similarity threshold in `config.py`:

```python
ALLaM_MODEL_NAME = "ALLaM-AI/ALLaM-7B-Instruct-preview"
SIMILARITY_THRESHOLD = 0.2
```

Or change the embedding model:

```python
EMBEDDING_MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
```

---

## How to Use in Colab

If you’re using **Google Colab**, follow this snippet:

```python
import zipfile

# Unzip your uploaded file
with zipfile.ZipFile("allam-rag-pipeline.zip", 'r') as zip_ref:
    zip_ref.extractall("project")

%cd project/allam-rag-pipeline
!pip install -r requirements.txt
!python main.py
```

---

##  Acknowledgements

- [ALLaM-7B](https://huggingface.co/ALLaM-AI/ALLaM-7B-Instruct-preview)
- [FAISS](https://github.com/facebookresearch/faiss)
- [LangChain](https://github.com/langchain-ai/langchain)
- [Sentence Transformers](https://www.sbert.net/)



