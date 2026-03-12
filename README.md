PRIVATE RAG AI DOCUMENT ASSISTANT - COMPLETE PROJECT GUIDE
Author: Sajith Kumar


This file contains EVERYTHING needed to understand and run the project:

1. Project Overview
2. Project Structure
3. README Documentation
4. Requirements.txt
5. .gitignore
6. Installation Guide
7. Running the Server
8. GitHub Upload Instructions

============================================================
1. PROJECT OVERVIEW
============================================================

This project is a PRIVATE AI DOCUMENT ASSISTANT.

It can:

- Read large PDF documents
- Understand document content
- Summarize contracts
- Answer questions from documents
- Run completely offline
- Work inside company networks

The system uses RAG (Retrieval Augmented Generation).

RAG works like this:

1. Convert document text into embeddings
2. Store embeddings in a vector database
3. Retrieve relevant parts when a question is asked
4. Use a language model to generate an answer


============================================================
2. SYSTEM ARCHITECTURE
============================================================

User / Fiori App
        ↓
FastAPI AI Server
        ↓
ChromaDB Vector Database
        ↓
Ollama (Llama3 Model)


============================================================
3. PROJECT STRUCTURE
============================================================

rag-ai-document-assistant/
│
├── ai_server.py
├── requirements.txt
├── README.md
├── .gitignore
│
└── chroma_db/
    (auto generated vector database)


============================================================
4. README DOCUMENTATION
============================================================

# Private RAG AI Document Assistant

This project is a private AI system that can read large PDF documents,
summarize them, and answer questions using a local AI model.

The system runs fully inside an enterprise network and does not send
any data to external AI providers.

Features:

- Upload large PDF contracts
- Extract text from documents
- Convert text into embeddings
- Store embeddings in vector database
- Retrieve relevant document sections
- Generate answers using Llama3
- Fully private AI system

Example Questions:

- What is the payment term?
- What is the penalty clause?
- Does the contract auto renew?
- What is the termination policy?

Technology Stack:

Python
FastAPI
Uvicorn
ChromaDB
Sentence Transformers
Torch
pdfplumber
Ollama
Llama3

Minimum Server Requirements:

CPU: 8 cores
RAM: 16 GB
Disk: 50 GB
GPU: Optional


============================================================
5. REQUIREMENTS.TXT
============================================================

fastapi==0.110.0
uvicorn==0.29.0
chromadb==0.4.24
sentence-transformers==2.7.0
torch==2.2.2
pdfplumber==0.11.0
requests==2.31.0
python-multipart==0.0.9
pydantic==2.6.4


============================================================
6. .GITIGNORE
============================================================

__pycache__/
*.pyc
*.pdf
chroma_db/
.env


============================================================
7. INSTALLATION GUIDE
============================================================

STEP 1: Install Python 3.10

Download:
https://www.python.org/downloads/release/python-31011/

IMPORTANT:
Enable "Add Python to PATH"


STEP 2: Install Python Dependencies

Run:

pip install -r requirements.txt


STEP 3: Install Ollama

Download:
https://ollama.com


STEP 4: Download Llama3 Model

Run:

ollama pull llama3


STEP 5: Start AI Server

Run:

uvicorn ai_server:app --host 0.0.0.0 --port 8000


============================================================
8. TEST THE API
============================================================

Open browser:

http://127.0.0.1:8000/docs

FastAPI will show interactive API documentation.

Upload a PDF and test the AI assistant.


============================================================
9. API ENDPOINTS
============================================================

Upload Document

POST /upload

Form Data:
file: PDF

Response:

{
 "docId": "unique-id"
}


Ask Question

POST /ask

Request:

{
 "question": "What is payment term?",
 "docId": "document-id"
}


Response:

{
 "answer": "Payment term is 30 days"
}


============================================================
10. HOW THE AI WORKS
============================================================

DOCUMENT UPLOAD FLOW

PDF Uploaded
↓
Text Extracted
↓
Text Split into Chunks
↓
Chunks Converted into Embeddings
↓
Stored in ChromaDB


QUESTION FLOW

User Question
↓
Convert question to embedding
↓
Search vector database
↓
Retrieve relevant chunks
↓
Send context to Llama3
↓
Generate answer


============================================================
11. GITHUB UPLOAD INSTRUCTIONS
============================================================

STEP 1

Install Git

https://git-scm.com/downloads


STEP 2

Open terminal inside project folder


STEP 3

Initialize repository

git init


STEP 4

Add files

git add .


STEP 5

Commit

git commit -m "Initial commit - RAG AI Document Assistant"


STEP 6

Create repository on GitHub

https://github.com/new


STEP 7

Connect GitHub repository

git remote add origin https://github.com/YOUR_USERNAME/rag-ai-document-assistant.git


STEP 8

Push code

git branch -M main
git push -u origin main


============================================================
END OF DOCUMENT
============================================================
