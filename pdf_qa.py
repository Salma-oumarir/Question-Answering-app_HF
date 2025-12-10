import io
import numpy as np
import faiss
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
from transformers import pipeline

EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
GEN_MODEL = "google/flan-t5-base"   # good CPU model

embedder = SentenceTransformer(EMBED_MODEL)
generator = pipeline("text2text-generation", model=GEN_MODEL)

def extract_text_from_pdf(file) -> str:
    data = file.read()
    reader = PdfReader(io.BytesIO(data))
    pages = []
    for p in reader.pages:
        pages.append(p.extract_text() or "")
    return "\n".join(pages)

def chunk_text(text: str, chunk_size: int = 900, overlap: int = 150):
    text = " ".join(text.split())
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

def build_faiss_index(vectors: np.ndarray):
    dim = vectors.shape[1]
    index = faiss.IndexFlatIP(dim)  # cosine if vectors normalized
    index.add(vectors.astype(np.float32))
    return index

def build_index_from_pdf(uploaded_file):
    text = extract_text_from_pdf(uploaded_file)
    if len(text.strip()) < 50:
        raise ValueError("PDF text extraction failed (maybe it's scanned). Try another PDF.")

    chunks = chunk_text(text)
    emb = embedder.encode(chunks, normalize_embeddings=True, show_progress_bar=False)
    index = build_faiss_index(np.array(emb))
    return index, chunks

def retrieve(question: str, index, chunks, k: int = 4):
    q_emb = embedder.encode([question], normalize_embeddings=True)
    scores, ids = index.search(np.array(q_emb).astype(np.float32), k)
    picked = [chunks[i] for i in ids[0] if i != -1]
    return picked

def answer_question(question: str, index, chunks):
    context_chunks = retrieve(question, index, chunks, k=4)
    context = "\n\n".join(context_chunks)

    prompt = (
        "Answer the question using ONLY the context. "
        "If the answer is not in the context, say 'I don't know based on the PDF.'\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {question}\nAnswer:"
    )

    out = generator(prompt, max_new_tokens=220, do_sample=False)
    answer = out[0]["generated_text"]
    return answer, context_chunks
