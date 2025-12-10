#  Chat with PDF — Question Answering Application

This project is an interactive **AI-powered application that allows users to chat with PDF documents**.  
Users upload a PDF file and ask questions in natural language, and the system returns answers  
**based only on the content of the uploaded PDF**.

The application uses **semantic search (FAISS + sentence embeddings)** combined with a  
**text generation model** to produce accurate, document-grounded answers.

 **Live demo (Hugging Face Spaces):**  
https://salmaoumarir-chat-with-pdf.hf.space

---

##  Features

- Upload PDF documents
- Ask questions in natural language
- Semantic search using vector embeddings
- Answers generated **only from the PDF content**
- Displays source text used to generate each answer
- Simple and clean Streamlit interface
- Dockerized for easy deployment

---

##  How It Works (Architecture)

1. **PDF text extraction**
   - Text is extracted from the uploaded PDF using `pypdf`.

2. **Text chunking**
   - The document is split into overlapping chunks for better retrieval.

3. **Embedding & indexing**
   - Each chunk is embedded using `all-MiniLM-L6-v2`.
   - Embeddings are indexed with **FAISS** for fast similarity search.

4. **Retrieval**
   - The most relevant chunks are retrieved based on the user question.

5. **Answer generation**
   - A text-to-text generation model (`flan-t5-base`) generates an answer  
     using only the retrieved context.

---

##  Project Structure

```
├── app.py              # Streamlit application
├── pdf_qa.py           # PDF processing, indexing, retrieval, QA logic
├── requirements.txt    # Python dependencies
├── Dockerfile          # Docker configuration
├── .dockerignore
└── README.md
```

---

##  Technologies Used

- Python
- Streamlit
- PyPDF
- FAISS (CPU)
- Sentence Transformers
- Hugging Face Transformers
- PyTorch
- Docker

---

##  Run Locally

### 1 Create and activate a virtual environment (optional)

```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
```

### 2 Install dependencies

```bash
pip install -r requirements.txt
```

### 3 Run the application

```bash
streamlit run app.py
```

---

##  Run with Docker

### Build the image

```bash
docker build -t chat-with-pdf .
```

### Run the container

```bash
docker run -p 7860:7860 chat-with-pdf
```


---

##  Final Verdict

This project demonstrates a complete **Document Question Answering pipeline**, from PDF ingestion  
to semantic retrieval and answer generation, wrapped in a user-friendly web application.  
It is suitable for **GitHub portfolios, internships, and applied AI demonstrations**.
