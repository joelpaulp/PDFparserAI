from retriever import model, split_markdown_into_chunks, build_faiss_index, extract_headings
import requests, os, time
from dotenv import load_dotenv
import numpy as np
load_dotenv()

MAX_RETRIES = 3
RETRY_WAIT_SECONDS = 5
TOP_K = 10  # Boosted from 5 to 10 for deeper retrieval

global_index = None
global_chunks = None
global_heading_index = None
global_headings = None
global_markdown_text = None

def init_retrieval(markdown_text):
    global global_index, global_chunks, global_heading_index, global_headings, global_markdown_text
    global_markdown_text = markdown_text

    chunks = split_markdown_into_chunks(markdown_text)
    index, _, chunks = build_faiss_index(chunks)
    global_index = index
    global_chunks = chunks

    headings = extract_headings(markdown_text)
    heading_index, _, headings = build_faiss_index(headings)
    global_heading_index = heading_index
    global_headings = headings

def retrieve_relevant_chunks(query, top_k=TOP_K):
    if global_index is None:
        return []

    query_embedding = model.encode([query])
    D, I = global_index.search(np.array(query_embedding).astype('float32'), top_k)
    return [global_chunks[i] for i in I[0] if i < len(global_chunks)]

def retrieve_relevant_headings(query, top_k=5):
    if global_heading_index is None:
        return []

    query_embedding = model.encode([query])
    D, I = global_heading_index.search(np.array(query_embedding).astype('float32'), top_k)
    return [global_headings[i] for i in I[0] if i < len(global_headings)]

def rag_prompt_with_history(user_question: str, retrieved_chunks: list, chat_history: list) -> str:
    prompt = "You are a helpful assistant.\n\n"

    if chat_history:
        prompt += "Previous Q&A:\n"
        for q, a in chat_history[-3:]:
            prompt += f"User: {q}\nAssistant: {a}\n\n"

    prompt += "Relevant Document Chunks:\n"
    prompt += "\n---\n".join(retrieved_chunks)

    prompt += f"\n\nUser: {user_question}\nAssistant:"
    return prompt

def answer_query_with_rag(user_question: str, chat_history: list) -> tuple:
    # First: retrieve relevant chunks
    relevant_chunks = retrieve_relevant_chunks(user_question)

    # If chunks are poor or missing, try headings-only fallback
    if not relevant_chunks or all(len(c.strip()) < 20 for c in relevant_chunks):
        fallback_headings = retrieve_relevant_headings(user_question)
        relevant_chunks = fallback_headings + ["(Used headings fallback — try rephrasing for deeper context.)"]

    prompt = rag_prompt_with_history(user_question, relevant_chunks, chat_history)

    api_key = os.getenv("OPENROUTER_API_KEY")
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    data = {
        "model": "google/gemma-3n-e4b-it:free",
        "prompt": prompt,
        "temperature": 0.7,
        "max_tokens": 1024
    }

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = requests.post("https://openrouter.ai/api/v1/completions", headers=headers, json=data)
            response.raise_for_status()
            output = response.json()["choices"][0]["text"].strip()
            chat_history.append((user_question, output))
            return output, chat_history

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                time.sleep(RETRY_WAIT_SECONDS * attempt)
            else:
                return f"❌ HTTP Error {e.response.status_code}: {e.response.text}", chat_history
        except Exception as e:
            return f"❌ General Error: {str(e)}", chat_history

    return "❌ Failed after retries", chat_history
