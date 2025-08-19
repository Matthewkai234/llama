# RAG Project with Gemini Model

This project is a **Retrieval-Augmented Generation (RAG)** system.  
It uses a CSV file as knowledge, finds similar text with **FAISS + HuggingFace embeddings**, and then sends the context to the **Google Gemini model** to generate answers.

---

##  What It Does
1. **Read a CSV file** (example: dataset or table).
2. **Convert each row into a text paragraph.**
3. **Create embeddings** for all paragraphs using HuggingFace.
4. **Search the most similar paragraph** for a user question.
5. **Generate an answer** with the Gemini model, using the context.

---

## Project Structure
```
rag/
├── api.py             # FastAPI app (REST API for asking questions)
├── config.py          # Config file: model name, similarity threshold
├── gemini_model.py    # Gemini model (Google API)
├── main.py            # Simple demo script
├── rag_model.py       # RAG pipeline (retrieve + generate)
├── utils.py           # CSV → text paragraphs
├── vector.py          # Vector store with FAISS
├── requirements.txt   # Python dependencies
```

---

## Setup Gemini API Key
This project needs a **Google Gemini API key**.

1. Create a file named `.env` in the project folder.  
2. Inside it, add:

```env
GEMINI_API_KEY=your_api_key_here
```

Replace `your_api_key_here` with your real Gemini API key.

---

## Requirements
Install dependencies with:

```bash
pip install -r requirements.txt
```

---

##  Run the Project

### 1. Simple test
- Put your CSV file in the project folder (example: `data.csv`).  
- Run:

```bash
python main.py
```

You will see the question, the answer, and the similarity score.

---

### 2. Run with FastAPI
Start the API server with:

```bash
uvicorn api:app --reload
```

Open in your browser:  
 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

Use the `/ask` endpoint to send a question.  

The API will return:
- **answer** → the generated text from Gemini  
- **similarity** → score between 0.0 and 1.0  

---

## Notes
- The **similarity score** shows how close the context is to your question.  
- If the score is low, the answer may not be correct.  
- You can change the embedding model or threshold in `config.py`.  
