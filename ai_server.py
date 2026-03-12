from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import requests
import uuid
import pdfplumber
import os
import base64

app = FastAPI()

# =========================
# Simple Chat Memory (per document)
# =========================
chat_memory = {}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# Load embedding model once
# =========================
embedding_model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

# =========================
# Persistent ChromaDB
# =========================
chroma_client = chromadb.Client(
    Settings(
        persist_directory="chroma_db",
        is_persistent=True
    )
)

collection = chroma_client.get_or_create_collection("documents")

# =========================
# Utility Functions
# =========================
def extract_text(path):
    text = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

def chunk_text(text, size=1000):
    return [text[i:i+size] for i in range(0, len(text), size)]

# =========================
# Upload PDF (File Upload)
# =========================
@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    doc_id = str(uuid.uuid4())
    temp_file = f"{doc_id}.pdf"

    with open(temp_file, "wb") as f:
        f.write(await file.read())

    text = extract_text(temp_file)
    chunks = chunk_text(text)

    embeddings = embedding_model.encode(chunks).tolist()
    ids = [f"{doc_id}_{i}" for i in range(len(chunks))]

    collection.add(
        documents=chunks,
        embeddings=embeddings,
        ids=ids,
        metadatas=[{"doc_id": doc_id}] * len(chunks)
    )

    os.remove(temp_file)

    return {"docId": doc_id}

# =========================
# Upload PDF via Base64 (SAP XSTRING)
# =========================
class Base64Upload(BaseModel):
    fileName: str
    fileContent: str

@app.post("/upload_base64")
async def upload_base64(data: Base64Upload):

    doc_id = str(uuid.uuid4())

    try:
        clean_base64 = data.fileContent.strip()

        # Remove header if exists
        if "base64," in clean_base64:
            clean_base64 = clean_base64.split("base64,")[1]

        # Fix missing padding
        missing_padding = len(clean_base64) % 4
        if missing_padding:
            clean_base64 += "=" * (4 - missing_padding)

        pdf_bytes = base64.b64decode(clean_base64)

    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid Base64 format")

    temp_file = f"{doc_id}.pdf"

    with open(temp_file, "wb") as f:
        f.write(pdf_bytes)

    text = extract_text(temp_file)
    chunks = chunk_text(text)

    embeddings = embedding_model.encode(chunks).tolist()
    ids = [f"{doc_id}_{i}" for i in range(len(chunks))]

    collection.add(
        documents=chunks,
        embeddings=embeddings,
        ids=ids,
        metadatas=[{"doc_id": doc_id}] * len(chunks)
    )

    os.remove(temp_file)

    return {"docId": doc_id}

# =========================
# Ask Question (With Memory)
# =========================
class AskRequest(BaseModel):
    question: str
    docId: str

@app.post("/ask")
async def ask(req: AskRequest):

    # Check if document exists
    results_check = collection.get(
        where={"doc_id": req.docId}
    )

    if not results_check["ids"]:
        raise HTTPException(status_code=404, detail="Document not found")

    # Create embedding for question
    question_embedding = embedding_model.encode([req.question]).tolist()

    results = collection.query(
        query_embeddings=question_embedding,
        n_results=5,
        where={"doc_id": req.docId}
    )

    if not results["documents"] or not results["documents"][0]:
        raise HTTPException(status_code=404, detail="No relevant context found")

    context = "\n".join(results["documents"][0])

    # Initialize memory for this document
    if req.docId not in chat_memory:
        chat_memory[req.docId] = []

    # Build previous conversation
    previous_conversation = ""
    for chat in chat_memory[req.docId]:
        previous_conversation += f"Q: {chat['question']}\nA: {chat['answer']}\n"

    prompt = f"""
Previous Conversation:
{previous_conversation}

Use ONLY this document context:
{context}

If answer not found say "Not found in document".

Question: {req.question}
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }
    )

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="LLM generation failed")

    answer_text = response.json()["response"]

    # Save to memory
    chat_memory[req.docId].append({
        "question": req.question,
        "answer": answer_text
    })

    return {"answer": answer_text}