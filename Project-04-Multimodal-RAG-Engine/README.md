# 🖼️ Multimodal RAG Engine

A multimodal Retrieval-Augmented Generation system designed to retrieve and reason across text, complex financial tables, charts, and technical schematics by combining visual understanding with searchable textual representations.

## 📌 Project Overview

Traditional document RAG pipelines often rely heavily on OCR and plain-text extraction.

This creates a major limitation for documents containing:

- Financial tables
- Balance sheets
- Cash-flow grids
- Architecture diagrams
- Electrical circuits
- Scatter plots
- Heatmaps
- Performance charts

OCR can convert these visual structures into flattened text and lose important spatial relationships such as rows, columns, merged cells, chart trends, and relationships between visual elements.

This project addresses that limitation using a **Dual-Representation Multi-Vector Architecture**.

Instead of indexing raw image pixels directly, the system:

1. Preserves the original visual asset.
2. Uses a Vision LLM to generate a rich textual summary.
3. Stores the textual representation for semantic retrieval.
4. Resolves the original visual asset when answering a query.
5. Passes the original visual context to a multimodal generation model.

---

## 🚀 Key Features

- **Vision-Based Understanding** — Uses a vision-capable LLM to analyze charts, tables, and diagrams.
- **Dual Representation** — Separates searchable textual representations from original visual assets.
- **Visual Asset Preservation** — Stores the original image in a document store.
- **Semantic Summarization** — Converts visual information into searchable natural-language descriptions.
- **Multimodal Querying** — Sends the original visual context to the generation model.
- **Dynamic Document IDs** — Assigns unique identifiers to ingested visual elements.
- **Base64 Image Encoding** — Converts image bytes into a format suitable for multimodal API requests.
- **Deterministic Validation** — Tests the core ingestion and storage behavior without requiring a live API call.

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core implementation |
| OpenAI API | Vision-based summarization and multimodal generation |
| PyMuPDF | PDF/document processing foundation |
| Pytest | Automated testing |
| python-dotenv | Environment configuration |
| Base64 | Image encoding for multimodal requests |
| GitHub | Version control and portfolio hosting |

---

## 🏗️ Architecture

```text
                         ┌──────────────────────┐
                         │   Document / Image   │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ Extract / Segment    │
                         │                      │
                         │ Text                 │
                         │ Tables               │
                         │ Images / Diagrams    │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │    Vision LLM        │
                         │                      │
                         │ Visual Summarization │
                         └──────────┬───────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    │                               │
                    ▼                               ▼
          ┌──────────────────┐             ┌──────────────────┐
          │ Textual Summary  │             │ Original Visual  │
          │                  │             │ Asset            │
          └────────┬─────────┘             └────────┬─────────┘
                   │                                │
                   ▼                                ▼
          ┌──────────────────┐             ┌──────────────────┐
          │ Vector Index     │             │ Document Store   │
          │                  │             │                  │
          │ Searchable       │             │ High-Resolution  │
          │ Representation   │             │ Parent Asset     │
          └────────┬─────────┘             └────────┬─────────┘
                   │                                │
                   └───────────────┬────────────────┘
                                   │
                                   ▼
                         ┌──────────────────────┐
                         │ Multimodal Query    │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ Vision-Capable LLM   │
                         │                      │
                         │ Final Answer         │
                         └──────────────────────┘
````

---

## 🔄 Workflow

The Multimodal RAG workflow is:

```text
Visual Document
      ↓
Extract / Segment
      ↓
Visual Element
      ↓
Vision LLM
      ↓
Semantic Summary
      ↓
Dual Representation
   ↙              ↘
Vector Index    Document Store
   │              │
   └──────┬───────┘
          ↓
     User Query
          ↓
  Retrieve Matching
   Visual Element
          ↓
 Resolve Original Asset
          ↓
 Multimodal Generation
          ↓
      Final Answer
```

### 1. Visual Input

The system receives an image or visual document element such as:

```text
Chart
Table
Diagram
Technical Schematic
```

### 2. Visual Summarization

The image is encoded as Base64 and supplied to the Vision LLM together with an instruction describing the visual element.

For example:

```python
summarize_visual_element(
    image_bytes,
    element_type="chart"
)
```

The model is instructed to describe:

* Important data points
* Trends
* Relationships
* Columns
* Labels
* Structural information

### 3. Dual Representation

The system creates two representations of the same visual element.

```text
                    Visual Element
                         │
              ┌──────────┴──────────┐
              │                     │
              ▼                     ▼
       Textual Summary        Original Asset
              │                     │
              ▼                     ▼
       Vector Index            Document Store
```

The textual summary is designed for semantic search, while the original visual asset is preserved for multimodal generation.

### 4. Document Storage

Each visual element receives a unique document ID.

The document store retains:

```text
Document ID
Element Type
Base64 Visual Asset
```

### 5. Query

When a multimodal query is received, the system resolves the parent visual asset and passes it to the multimodal generation model.

### 6. Final Generation

The model receives:

```text
User Query
+
Original Visual Context
```

and generates the final answer.

---

## 🧠 Dual-Representation Multi-Vector Pattern

The central architectural concept is the **Dual-Representation Multi-Vector Pattern**.

The pipeline separates:

```text
Search Representation
        ≠
Generation Representation
```

### Search Representation

The Vision LLM creates a rich textual description of the visual element.

This representation can be used for semantic retrieval.

### Generation Representation

The original high-resolution visual asset is preserved.

When the corresponding element is retrieved, the original asset can be passed directly into the multimodal generation context.

This avoids relying exclusively on flattened OCR text.

---

## 📊 Why Visual Summarization?

Consider a financial table:

```text
              Q1       Q2       Q3
Revenue      120      150      180
Expenses      80       95      110
Profit        40       55       70
```

A conventional OCR pipeline may flatten the spatial structure into a sequence of tokens.

The relationships between:

```text
Row
Column
Quarter
Metric
```

can become harder to retrieve accurately.

A Vision LLM can instead produce a semantic description containing the relationships between the values.

This makes the visual information more compatible with semantic retrieval.

---

## 🔎 Cross-Modal Retrieval

The architecture is designed for queries such as:

```text
"What was the revenue trend across the reported quarters?"
```

or:

```text
"Which component is connected to the main processing unit in this diagram?"
```

or:

```text
"Which quarter had the highest operating expense?"
```

The important distinction is that the system can preserve the original visual context instead of depending exclusively on OCR-derived text.

---

## 🧩 Core Components

### `multimodal_rag_engine.py`

Responsible for:

* OpenAI client initialization
* Base64 image encoding
* Vision-based visual summarization
* Visual element ingestion
* Document-store management
* Search-representation storage
* Multimodal querying

### Document Store

The in-memory document store preserves the original visual assets.

```python
docstore
```

### Vector Index

The current prototype maintains an in-memory searchable representation containing:

```text
Document ID
Summary
Element Type
```

```python
vector_index
```

The architecture can later be connected to a production vector database such as FAISS or Pinecone.

---

## 📂 Project Structure

```text
Project-04-Multimodal-RAG-Engine/
│
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
├── pytest.ini
│
├── src/
│   ├── __init__.py
│   └── multimodal_rag_engine.py
│
└── tests/
    └── test_multimodal_rag.py
```

---

## ⚙️ Requirements & Setup

### Requirements

* Python 3.10+
* OpenAI API key for live Vision inference
* pip
* Git
* Internet connection for API requests

### Environment Configuration

Create a local `.env` file:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

Do not commit the real API key to GitHub.

The repository contains:

```text
.env.example
```

as the configuration template.

---

## 📥 Setup

Clone the repository:

```bash
git clone https://github.com/SciddhantoSinha/Agentic-AI-Portfolio.git
```

Navigate to Project 04:

```bash
cd Agentic-AI-Portfolio/Project-04-Multimodal-RAG-Engine
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the environment on Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## ▶️ How to Run

The engine can be initialized with an OpenAI API key:

```python
from src.multimodal_rag_engine import MultimodalRAGEngine

engine = MultimodalRAGEngine(
    api_key="your_openai_api_key"
)
```

A visual element can then be ingested:

```python
with open("chart.png", "rb") as image_file:
    image_bytes = image_file.read()

doc_id = engine.ingest_image_element(
    image_bytes=image_bytes,
    element_type="chart"
)

print(doc_id)
```

A multimodal query can then be submitted:

```python
answer = engine.query_multimodal(
    "What trend is visible in the chart?"
)

print(answer)
```

---

## 🧪 Testing

The project includes automated tests for:

* Base64 image encoding
* Empty document-store initialization
* Empty-index query protection
* Visual element ingestion
* Document-store persistence
* Original image preservation
* Unique document IDs
* Multiple visual-element handling

Run the test suite with:

```bash
pytest
```

The tests do not require a live OpenAI API key because API-dependent behavior is isolated from the deterministic storage and ingestion tests.

---

## 🎯 Use Case

The project demonstrates how multimodal RAG can be applied to documents where important information exists outside conventional text.

Potential applications include:

* Financial report analysis
* Engineering document analysis
* Technical blueprint understanding
* Chart and dashboard analysis
* Scientific document analysis
* Architecture diagram interpretation
* Business intelligence workflows

---

## 💡 Benefits

* Preserves information contained in visual document elements
* Avoids relying exclusively on flattened OCR text
* Separates retrieval representation from generation representation
* Enables Vision LLM-based semantic understanding
* Maintains access to the original visual asset
* Supports cross-modal question answering
* Demonstrates multi-vector retrieval architecture
* Provides a foundation for production multimodal RAG systems

---

## 🧠 Skills Demonstrated

* Multimodal RAG
* Vision LLMs
* GPT-4o Vision
* Dual-Representation Architecture
* Multi-Vector Retrieval
* Document Decomposition
* Table Understanding
* Chart Understanding
* Technical Diagram Understanding
* Base64 Image Encoding
* Multimodal Prompting
* Cross-Modal Synthesis
* Python Testing
* API Integration

---

## 📈 Project Progression

This project represents the **fourth layer** of the Agentic AI portfolio:

```text
Project 01
RAG From Scratch
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

The architecture progressively evolves from:

```text
Fixed Retrieval
      ↓
Domain-Constrained AI
      ↓
Autonomous Tool Calling
      ↓
Cross-Modal Intelligence
      ↓
Real-Time Agentic Systems
```

---

## 🔬 Architecture Trade-Off

An alternative approach is direct vision embedding, such as ColPali-style document-page representations.

The dual-representation approach used in this project instead separates:

```text
Vision Understanding
        ↓
Textual Semantic Representation
        ↓
Vector Retrieval
        ↓
Original Visual Resolution
        ↓
Multimodal Generation
```

This approach is more interpretable and can leverage conventional vector databases, although it introduces an additional Vision LLM preprocessing cost during ingestion.

---

## 🏭 Production Architecture

The handbook's production architecture uses document decomposition to identify:

* Text blocks
* Table blocks
* Image elements

Vision LLMs then generate searchable descriptions, while the original visual or table representation is retained for generation-time context.

A production implementation can extend this prototype with:

* PyMuPDF / Unstructured document parsing
* Production vector databases
* Persistent document stores
* Multi-vector retrieval
* Table-specific representations
* Image and diagram extraction
* Retrieval ranking
* Metadata filtering
* Production observability

The current repository implements the core multimodal prototype and dual-representation storage pattern.

---

## ⚠️ Important Disclaimer

This project is a technical demonstration of multimodal Retrieval-Augmented Generation architecture.

Vision LLM outputs can contain errors. Visual information should be independently verified before being used for financial, engineering, scientific, medical, legal, or other high-stakes decisions.

---

## 👨‍💻 Author

**Sciddhanto Sinha**

B.Tech – Computer Science Engineering (AI & Analytics)

````

The README reflects the handbook's central Project 04 architecture and its stated trade-off between direct vision embedding and dual-representation indexing. :contentReference[oaicite:0]{index=0} :contentReference[oaicite:1]{index=1}

**Commit message:**

```text
Document Project 04 multimodal RAG engine
````

Then stop here and tell me **“done”**.
