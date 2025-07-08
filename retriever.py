from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Default model — upgradeable
model = SentenceTransformer("all-MiniLM-L6-v2")

def split_markdown_into_chunks(markdown_text, max_chunk_tokens=300):
    """
    Structure-aware chunking: starts new chunk at headings and maintains logical grouping.
    """
    chunks = []
    current = []
    current_token_count = 0

    for line in markdown_text.splitlines():
        # New section starts at heading
        if line.strip().startswith(("#", "##", "###")) and current:
            chunks.append("\n".join(current).strip())
            current = []
            current_token_count = 0

        current.append(line)
        current_token_count += len(line.split())

        if current_token_count >= max_chunk_tokens:
            chunks.append("\n".join(current).strip())
            current = []
            current_token_count = 0

    if current:
        chunks.append("\n".join(current).strip())

    return chunks

def extract_headings(markdown_text):
    return [line.strip() for line in markdown_text.splitlines() if line.strip().startswith(("#", "##", "###"))]

def build_faiss_index(text_list):
    embeddings = model.encode(text_list)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(np.array(embeddings).astype('float32'))
    return index, embeddings, text_list
