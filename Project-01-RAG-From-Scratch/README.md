# RAG from Scratch – Fixed Pipeline

A foundational Retrieval-Augmented Generation (RAG) system built from scratch using dense embeddings, recursive chunking, FAISS vector search, and an LLM for context-aware question answering.

## 📌 Project Overview

The **RAG from Scratch** project implements a fixed RAG pipeline that retrieves the most relevant document chunks before sending them to a Large Language Model (LLM).

The system converts document text into smaller chunks, generates dense vector embeddings for those chunks, stores them in a **FAISS vector index**, and retrieves the most relevant chunks for a user's query using similarity search.

The retrieved context is then formatted into a prompt and passed to the LLM to generate the final answer.

## 🚀 Key Features

* 📄 Supports ingestion of raw text documents
* ✂️ Splits documents using recursive character chunking
* 🧠 Generates dense vector embeddings for document chunks
* 🔎 Performs top-k nearest-neighbor retrieval
* 📊 Uses cosine similarity through normalized vectors
* 🗂️ Stores document chunks alongside the FAISS index
* 💬 Sends retrieved context to an LLM for answer generation
* ⚡ Uses a fixed retrieval-and-generation pipeline
* 🔄 Supports configurable chunk size and chunk overlap
* 🎯 Returns similarity scores for retrieved chunks

## 🛠️ Technologies Used

* **Python**
* **OpenAI API**
* **FAISS**
* **NumPy**
* **LangChain Text Splitters**
* **RecursiveCharacterTextSplitter**
* **Dense Embeddings**
* **Large Language Model (LLM)**
* **Cosine Similarity**

## 🔄 Workflow

```text
Raw Document
     ↓
Text Extraction
     ↓
Recursive Character Chunking
     ↓
Dense Embeddings
     ↓
FAISS Vector Index
     ↓
User Query
     ↓
Query Embedding
     ↓
Top-k Nearest Neighbor Search
     ↓
Retrieve Relevant Chunks
     ↓
Prompt Formatting
     ↓
LLM
     ↓
Generated Answer
```

## 🧩 RAG Architecture

The project follows two main flows.

### Ingestion Flow

```text
Raw Files
    ↓
Text Extraction
    ↓
Recursive Chunking
    ↓
Dense Embeddings
    ↓
FAISS Vector Index
```

During ingestion, the document is divided into smaller chunks using recursive character splitting.

Each chunk is converted into a dense embedding vector and added to the FAISS index.

### Inference Flow

```text
User Query
    ↓
Query Embedding
    ↓
Top-k Nearest Neighbor Search
    ↓
Retrieved Context
    ↓
Prompt Formatting
    ↓
LLM
    ↓
Answer
```

When a user submits a query, the query is converted into an embedding and compared against the vectors stored in FAISS.

The most relevant chunks are retrieved and provided as context to the LLM.

## 📋 Chunking Configuration

The pipeline uses `RecursiveCharacterTextSplitter`.

| Parameter     |     Default Value | Description                                    |
| ------------- | ----------------: | ---------------------------------------------- |
| Chunk Size    |               600 | Maximum size used when splitting text          |
| Chunk Overlap |               100 | Overlapping content between consecutive chunks |
| Top-k         |                 4 | Number of relevant chunks retrieved            |
| Similarity    | Cosine Similarity | Similarity measure used for vector retrieval   |

The splitter uses the following separators:

```text
\n\n
\n
. 
(space)
(empty string)
```

This allows the splitter to progressively fall back to smaller boundaries when necessary.

## 🔎 Vector Retrieval

The system uses **FAISS `IndexFlatIP`** for vector search.

The embeddings are L2-normalized before being added to the index:

```text
Normalized Embeddings
        ↓
FAISS IndexFlatIP
        ↓
Inner Product
        ↓
Cosine Similarity
```

For normalized vectors, inner product is equivalent to cosine similarity.

The retrieval process returns:

| Field   | Description                        |
| ------- | ---------------------------------- |
| `chunk` | Retrieved document chunk           |
| `score` | Similarity score returned by FAISS |

## 🤖 LLM Generation

After retrieving the relevant document chunks, the system combines them into a context block.

The resulting prompt follows this structure:

```text
CONTEXT:
<retrieved document chunks>

QUERY:
<user query>

ANSWER:
```

The LLM then generates the final response using the retrieved context.

## 📂 Project Structure

```text
project-01-rag-from-scratch/
│
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
│
├── data/
│   └── .gitkeep
│
├── src/
│   ├── __init__.py
│   └── rag_pipeline.py
│
└── tests/
    └── test_rag.py
```

## 📄 Core Implementation

The main RAG pipeline is implemented in:

```text
src/rag_pipeline.py
```

The `ScratchRAGPipeline` class handles:

* OpenAI client initialization
* Embedding generation
* Embedding normalization
* Recursive document chunking
* FAISS index creation
* Document ingestion
* Similarity-based retrieval
* Context construction
* LLM-based answer generation

## 🧪 Testing

The project includes unit tests in:

```text
tests/test_rag.py
```

The current tests verify:

* Pipeline initialization
* FAISS index configuration
* Embedding dimension configuration
* Initial document storage behavior

The tests are designed so that these basic checks **do not require an OpenAI API call**.

## ⚙️ Requirements & Setup

Before running the project, make sure the following are installed:

* **Python 3.12+**
* **pip**
* An **OpenAI API key** for running the actual embedding and generation pipeline

Required Python packages are listed in:

```text
requirements.txt
```

## 📥 Setup

### Clone the repository

```bash
git clone https://github.com/SciddhantoSinha/agentic-ai-portfolio.git
```

### Navigate to Project 01

```bash
cd agentic-ai-portfolio/project-01-rag-from-scratch
```

### Create a virtual environment

```bash
python -m venv .venv
```

### Activate the virtual environment

**Windows:**

```bash
.venv\Scripts\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

## 🔐 Environment Configuration

Create a `.env` file using `.env.example` as a reference.

```text
OPENAI_API_KEY=your_openai_api_key_here
```

The API key is required for:

* Generating document embeddings
* Generating query embeddings
* Generating final LLM responses

**Do not commit the `.env` file to GitHub.**

The repository's `.gitignore` excludes it from version control.

## ▶️ How to Run

Once the environment is configured, the `ScratchRAGPipeline` can be initialized with an OpenAI API key.

The general execution flow is:

1. Initialize the `ScratchRAGPipeline`.
2. Provide document text to the ingestion pipeline.
3. Split the document into chunks.
4. Generate embeddings for the chunks.
5. Add the embeddings to the FAISS index.
6. Submit a user query.
7. Generate an embedding for the query.
8. Retrieve the top-k relevant chunks.
9. Format the retrieved chunks as context.
10. Send the context and query to the LLM.
11. Return the generated answer.

## 🧪 Run Tests

From the Project 01 directory:

```bash
pytest
```

The current test suite validates the core pipeline configuration without requiring live API calls.

## ⚠️ Known Failure Modes

The fixed RAG pipeline can encounter several retrieval-related issues.

### Lost in the Middle

When multiple retrieved chunks are included in a prompt, important information positioned in the middle of the context may receive less attention from the LLM.

### Vector Inversion / Negation

Embedding-based retrieval can struggle with certain concepts involving negation or semantically opposing statements.

### Chunk Boundary Truncation

Important information may be split across chunk boundaries, causing the retrieved chunk to contain incomplete context.

These limitations are important considerations when designing more advanced RAG systems.

## 🎯 Use Case

The project demonstrates the foundational architecture behind a Retrieval-Augmented Generation system.

It can serve as a starting point for applications where an LLM needs to answer questions using information retrieved from a document collection rather than relying only on its pretrained knowledge.

The project also establishes the foundation for the more advanced Agentic AI systems developed in the later projects of this portfolio.

## 💡 Benefits

* Provides a clear implementation of the core RAG pipeline
* Demonstrates dense vector embeddings
* Demonstrates semantic similarity search using FAISS
* Shows how recursive chunking affects document retrieval
* Separates document ingestion from query inference
* Provides similarity scores for retrieved results
* Uses retrieved context to support LLM responses
* Establishes a foundation for more advanced Agentic RAG architectures

## 📈 Project Progression

This project represents the **first layer** of the Agentic AI portfolio:

```text
Project 01
RAG from Scratch
        ↓
Project 02
Enterprise Legal AI Assistant
        ↓
Project 03
Autonomous Research Agent
        ↓
Project 04
Multimodal RAG Engine
        ↓
Project 05
Real-Time Agentic RAG
```

The progression moves from a fixed RAG pipeline toward increasingly autonomous, multimodal, and real-time Agentic AI architectures.

## 👨‍💻 Author

**Sciddhanto Sinha**

B.Tech – Computer Science Engineering (AI & Analytics)
