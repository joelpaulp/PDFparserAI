# 📄 PDF Content Labeling + RAG Query Assistant

This project is an AI-powered PDF assistant that:

✅ Extracts and labels structured content from any PDF using LLMs (Mistral 3.2B)

✅ Allows you to query the PDF using natural language

✅ Uses RAG (Retrieval-Augmented Generation) to handle large PDFs by breaking them into semantic chunks and retrieving only relevant parts

🎥 [Watch Demo Video](https://youtu.be/9J9taSUDIUo)

---

## 🚀 Features

- 🧠 **LLM-Based PDF Labeling**: Uses `mistralai/mistral-small-3.2-24b-instruct:free` from OpenRouter to label PDF content into markdown sections (titles, subtitles, paragraphs)
- 📚 **RAG (Retrieval-Augmented Generation)**: Splits labeled content into chunks, creates embeddings, and retrieves only relevant parts for answering
- 💬 **Chat with PDF**: Tries to Maintains context through chat history.
- 🧱 **Structure-Aware Chunking**: Keeps headings with content to improve LLM understanding

---

## 🧰 Tech Stack

- [Streamlit](https://streamlit.io/) - UI
- [OpenRouter](https://openrouter.ai/) - LLM API (Mistral)
- [SentenceTransformers](https://www.sbert.net/) - Embeddings
- [FAISS](https://github.com/facebookresearch/faiss) - Vector search index
- [pdfplumber](https://github.com/jsvine/pdfplumber) - PDF text extraction

---


## 📦 Setup

### 1. Clone the repository
```bash
git clone https://https://github.com/joelpaulp/PDFparserAI/
```

### 2. Create and activate virtual environment
```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate   # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Create `.env` file
```bash
touch .env
```
Add this to your `.env` file:
```
OPENROUTER_API_KEY="replace this with your API Key without quoutes or whitespaces after equal sign"
```
> Get your key from [https://openrouter.ai](https://openrouter.ai)

---

## 🖥️ Run the App
```bash
streamlit run main.py
```
Then open: http://localhost:8501

---

## 📁 Project Structure
```
├── main.py                 # Streamlit UI
├── pdf_parser.py           # PDF to plain text
├── pdf_labeler.py          # LLM labeling to markdown
├── user_query.py           # RAG query logic + chat history
├── retriever.py            # Chunking, embedding, FAISS
├── requirements.txt
├── .env                    # Your API key
└── README.md
```

---

## ✅ Example Questions
- "What is the objective of Task 1?"
- "Summarize the submission instructions."
- "List all evaluation criteria."

---

## 🔒 Security Notes
- Your `.env` contains your API key. **Do not commit it**.
- You can add `.env` to `.gitignore`

---

## 🙌 Credits
Created by joelpaulp as part of an AI developer assignment.
