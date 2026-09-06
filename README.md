Absolutely. The **root `README.md`** should represent the entire portfolio, not any individual project.

It should present the five projects as a **progressive Agentic AI engineering journey**, with the same professional depth and formatting style as your Project 04 README.

Based on the project architecture we've built, the portfolio progression is:

```text
Project 01 → RAG Fundamentals
Project 02 → Enterprise Legal AI
Project 03 → Autonomous Research Agent
Project 04 → Multimodal RAG
Project 05 → Real-Time Agentic RAG
```

The Project 05 architecture specifically adds dynamic routing, corrective retrieval, live information, and verification as the final layer. 

---

# 🌐 ROOT `README.md`

Go to:

```text
Agentic-AI-Portfolio/README.md
```

Replace the entire contents with this:

````markdown
# 🤖 Agentic AI Portfolio

### A Progressive Portfolio of Retrieval-Augmented Generation, Autonomous Agents, Multimodal AI, and Real-Time Agentic Systems

---

## 📌 Portfolio Overview

This repository contains a progressive collection of **Agentic AI projects** designed to demonstrate the evolution from foundational Retrieval-Augmented Generation (RAG) systems to increasingly autonomous, multimodal, corrective, and real-time AI architectures.

The portfolio consists of five projects.

Each project introduces a new architectural capability while building upon concepts demonstrated in the previous project.

The progression is:

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
Real-Time Agentic RAG System
````

The portfolio therefore demonstrates a progression from:

```text
Fixed Retrieval
      ↓
Structured Enterprise AI
      ↓
Autonomous Tool Use
      ↓
Multimodal Intelligence
      ↓
Real-Time Corrective Agentic Systems
```

---

# 🎯 Portfolio Objective

The objective of this portfolio is to demonstrate practical understanding of modern AI application architecture rather than focusing only on isolated model calls.

The projects explore how AI systems can be designed to:

* Retrieve external knowledge
* Ground generated responses
* Produce structured outputs
* Verify citations
* Use tools autonomously
* Iterate on research tasks
* Understand visual information
* Retrieve across multimodal content
* Route queries dynamically
* Evaluate retrieval quality
* Correct poor retrieval
* Integrate live external information
* Cache responses
* Track system telemetry

The portfolio focuses on **system design, orchestration, retrieval, verification, and agentic behavior**.

---

# 🧠 Portfolio Architecture

The five projects form an architectural progression.

```text
                         ┌─────────────────────────────┐
                         │      Agentic AI Portfolio   │
                         └──────────────┬──────────────┘
                                        │
          ┌─────────────────────────────┼─────────────────────────────┐
          │                             │                             │
          ▼                             ▼                             ▼
 ┌──────────────────┐         ┌──────────────────┐         ┌──────────────────┐
 │ Project 01       │         │ Project 02       │         │ Project 03       │
 │ RAG Fundamentals │ ──────► │ Legal AI         │ ──────► │ Research Agent   │
 └──────────────────┘         └──────────────────┘         └────────┬─────────┘
                                                                      │
                                                                      ▼
                                                            ┌──────────────────┐
                                                            │ Project 04       │
                                                            │ Multimodal RAG   │
                                                            └────────┬─────────┘
                                                                     │
                                                                     ▼
                                                            ┌──────────────────┐
                                                            │ Project 05       │
                                                            │ Real-Time        │
                                                            │ Agentic RAG      │
                                                            └──────────────────┘
```

---

# 📚 Projects

## 01 — RAG From Scratch

### Retrieval-Augmented Generation Fundamentals

The first project establishes the foundation of the portfolio by implementing a RAG pipeline from the ground up.

### Core Concepts

* Document ingestion
* Text processing
* Chunking
* Embeddings
* Vector indexing
* Similarity retrieval
* Context assembly
* LLM generation
* Retrieval testing

### Architecture

```text
Documents
    ↓
Text Processing
    ↓
Chunking
    ↓
Embeddings
    ↓
Vector Index
    ↓
Similarity Search
    ↓
Relevant Context
    ↓
LLM
    ↓
Generated Answer
```

### Technologies

* Python
* OpenAI API
* FAISS
* Pytest
* python-dotenv

### Primary Learning Outcome

Understanding the internal mechanics of a RAG system rather than treating retrieval as a black-box component.

---

# ⚖️ 02 — Enterprise Legal AI Assistant

### Structured Contract Analysis with Citation Grounding

The second project introduces domain-specific AI and structured generation.

The system analyzes contract text and produces structured legal-risk findings.

### Core Capabilities

* Contract analysis
* Risk classification
* Structured output
* Clause extraction
* Verbatim citation extraction
* Citation grounding verification
* Suggested redlining

### Architecture

```text
Contract
    ↓
LLM Analysis
    ↓
Structured Contract Report
    ↓
Risk Findings
    ↓
Verbatim Contract Quotes
    ↓
Citation Verification
    ↓
Validated Analysis
```

### Risk Levels

```text
LOW
MEDIUM
HIGH
CRITICAL
```

### Technologies

* Python
* OpenAI API
* Pydantic
* Pytest
* python-dotenv

### Primary Learning Outcome

Demonstrating how generative AI can be constrained using structured schemas and deterministic validation.

---

# 🔬 03 — Autonomous Research Agent

### Iterative Tool-Using Research System

The third project moves from a fixed pipeline toward an autonomous agent.

The agent can decide when to use a research tool, execute the tool, observe the returned information, and continue its investigation.

### Core Capabilities

* Autonomous tool selection
* Tool registry
* Function calling
* Iterative research loop
* ArXiv integration
* Observation handling
* Repeated-tool-call detection
* Zero-yield reflection
* Iteration limits
* Research synthesis

### Architecture

```text
Research Question
        ↓
      LLM
        ↓
   Tool Decision
        ↓
   ┌────┴────┐
   │         │
 Search    Final
 ArXiv     Answer
   │
   ▼
Observation
   │
   ▼
LLM Re-evaluation
   │
   ▼
Additional Tool Call
   │
   ▼
Final Synthesis
```

### Technologies

* Python
* OpenAI API
* LangGraph
* ArXiv API
* Pytest
* python-dotenv

### Primary Learning Outcome

Understanding how an AI system can move from a single request-response interaction toward iterative autonomous tool use.

---

# 🖼️ 04 — Multimodal RAG Engine

### Cross-Modal Retrieval Across Text, Tables, Charts, and Technical Schematics

The fourth project introduces visual intelligence into the RAG architecture.

Traditional OCR-based pipelines can flatten visual structures such as financial tables, charts, and technical diagrams.

This project instead uses a **Dual-Representation Multi-Vector Architecture**.

The original visual asset is preserved while a Vision LLM creates a searchable textual representation.

### Core Capabilities

* Vision LLM understanding
* Visual summarization
* Dual representation
* Visual asset preservation
* Multimodal querying
* PDF processing
* Image extraction
* Document-store management
* Cross-modal retrieval
* Multimodal generation

### Architecture

```text
                    Visual Document
                           │
                           ▼
                  Extract / Segment
                           │
              ┌────────────┴────────────┐
              │                         │
              ▼                         ▼
       Textual Summary           Original Asset
              │                         │
              ▼                         ▼
        Vector Index              Document Store
              │                         │
              └────────────┬────────────┘
                           │
                           ▼
                       User Query
                           │
                           ▼
                  Retrieve Visual
                     Representation
                           │
                           ▼
                  Resolve Original
                       Asset
                           │
                           ▼
                  Multimodal LLM
                           │
                           ▼
                     Final Answer
```

### Technologies

* Python
* OpenAI Vision
* PyMuPDF
* Base64
* Pytest
* python-dotenv

### Primary Learning Outcome

Understanding how retrieval representation and generation representation can be separated when important information exists inside visual structures.

---

# ⚡ 05 — Real-Time Agentic RAG System

### Dynamic Query Routing, Corrective RAG, Live Search, Caching, and Telemetry

The fifth project represents the final stage of the portfolio.

It combines internal knowledge retrieval with live external information and introduces **Corrective RAG (CRAG)**.

Instead of assuming that retrieved context is correct, the system evaluates the retrieval before generation.

If internal evidence is insufficient, the pipeline can perform corrective live search.

### Core Capabilities

* Dynamic query routing
* Internal knowledge retrieval
* Live search
* Retrieval evaluation
* Corrective RAG
* Automatic fallback
* Grounded generation
* Hallucination mitigation
* Redis response caching
* Pipeline telemetry

### Architecture

```text
                         User Query
                              │
                              ▼
                     ┌──────────────────┐
                     │ Semantic Router  │
                     └────────┬─────────┘
                              │
                 ┌────────────┴────────────┐
                 │                         │
                 ▼                         ▼
          Internal Retrieval          Live Search
                 │                    (Tavily)
                 ▼                         │
          Retrieval Evaluator              │
                 │                         │
           ┌─────┴─────┐                   │
           │           │                   │
        Relevant    Irrelevant             │
           │           │                   │
           │           └───────────────────┘
           │
           ▼
      Context Assembly
           │
           ▼
     Answer Generation
           │
           ▼
      Grounding Check
           │
           ▼
      Audited Response
```

### Technologies

* Python
* OpenAI API
* Tavily
* Redis
* Pytest
* python-dotenv

### Primary Learning Outcome

Demonstrating how a RAG system can become a conditional agentic workflow that dynamically chooses information sources, evaluates retrieval quality, performs corrective retrieval, and verifies generated responses.

---

# 🧩 Cross-Project Capability Matrix

| Capability             | Project 01 | Project 02 | Project 03 | Project 04 | Project 05 |
| ---------------------- | ---------: | ---------: | ---------: | ---------: | ---------: |
| RAG                    |          ✅ |          ✅ |          ✅ |          ✅ |          ✅ |
| Vector Retrieval       |          ✅ |          — |          — |          ✅ |          ✅ |
| Structured Output      |          — |          ✅ |          — |          — |          — |
| Citation Grounding     |          — |          ✅ |          — |          — |          — |
| Tool Calling           |          — |          — |          ✅ |          — |          ✅ |
| Autonomous Loop        |          — |          — |          ✅ |          — |          ✅ |
| Vision                 |          — |          — |          — |          ✅ |          — |
| Multimodal Retrieval   |          — |          — |          — |          ✅ |          — |
| Dynamic Routing        |          — |          — |          — |          — |          ✅ |
| Retrieval Evaluation   |          — |          — |          — |          — |          ✅ |
| Corrective RAG         |          — |          — |          — |          — |          ✅ |
| Live Search            |          — |          — |      ArXiv |          — |     Tavily |
| Redis Cache            |          — |          — |          — |          — |          ✅ |
| Telemetry              |          — |          — |          — |          — |          ✅ |
| Grounding Verification |          — |          ✅ |          — |          — |          ✅ |

---

# 🏗️ Architectural Evolution

The portfolio demonstrates a progression in system complexity.

## Stage 1 — Fixed RAG

```text
Query
 ↓
Retrieve
 ↓
Generate
```

The system learns the fundamental RAG workflow.

---

## Stage 2 — Structured Enterprise AI

```text
Query
 ↓
Domain Analysis
 ↓
Structured Output
 ↓
Deterministic Validation
```

The system becomes constrained by schemas and validation rules.

---

## Stage 3 — Autonomous Tool Use

```text
Query
 ↓
Agent
 ↓
Tool Decision
 ↓
Tool Execution
 ↓
Observation
 ↓
Agent Re-evaluation
 ↓
Final Answer
```

The system gains iterative behavior.

---

## Stage 4 — Multimodal Intelligence

```text
Visual Document
 ↓
Vision Understanding
 ↓
Search Representation
 +
Original Visual Representation
 ↓
Multimodal Retrieval
 ↓
Multimodal Generation
```

The system expands beyond text.

---

## Stage 5 — Real-Time Agentic RAG

```text
Query
 ↓
Dynamic Routing
 ↓
Retrieve
 ↓
Evaluate
 ↓
Correct if Necessary
 ↓
Generate
 ↓
Verify
 ↓
Response
```

The system becomes conditional, corrective, and capable of integrating live information.

---

# 🔄 Complete Portfolio Learning Path

```text
                    ┌─────────────────────┐
                    │ RAG Fundamentals    │
                    │ Project 01          │
                    └──────────┬──────────┘
                               ↓
                    ┌─────────────────────┐
                    │ Structured AI       │
                    │ Project 02          │
                    └──────────┬──────────┘
                               ↓
                    ┌─────────────────────┐
                    │ Autonomous Agents   │
                    │ Project 03          │
                    └──────────┬──────────┘
                               ↓
                    ┌─────────────────────┐
                    │ Multimodal AI       │
                    │ Project 04          │
                    └──────────┬──────────┘
                               ↓
                    ┌─────────────────────┐
                    │ Real-Time Agents    │
                    │ Project 05          │
                    └─────────────────────┘
```

---

# 🛠️ Technologies Across the Portfolio

| Technology    | Portfolio Usage                       |
| ------------- | ------------------------------------- |
| Python        | Core programming language             |
| OpenAI API    | LLM generation and reasoning          |
| FAISS         | Vector retrieval                      |
| Pydantic      | Structured AI outputs                 |
| LangGraph     | Agentic workflow orchestration        |
| ArXiv API     | Research retrieval                    |
| PyMuPDF       | PDF and document processing           |
| Tavily        | Live web search                       |
| Redis         | Response caching                      |
| Pytest        | Unit and integration testing          |
| python-dotenv | Environment configuration             |
| GitHub        | Version control and portfolio hosting |

---

# 🧪 Testing Philosophy

Testing is incorporated throughout the portfolio rather than treating validation as an afterthought.

The projects contain tests for:

* Retrieval behavior
* Data processing
* Structured outputs
* Citation verification
* Tool registration
* Agent behavior
* Visual ingestion
* Document storage
* Query routing
* Retrieval evaluation
* Corrective fallback
* Cache behavior
* Telemetry collection
* Integration workflows

Where external APIs are involved, deterministic components are isolated and external services are mocked where appropriate.

This allows core application behavior to be validated without requiring every test to make a live API request.

---

# 🔐 Environment & Security

API credentials are intentionally excluded from version control.

Projects use `.env.example` files as configuration templates.

Typical configuration variables include:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

Additional projects may use service-specific credentials such as:

```env
TAVILY_API_KEY=your_tavily_api_key_here
REDIS_URL=redis://localhost:6379
```

Real credentials should never be committed to GitHub.

---

# 📂 Repository Structure

```text
Agentic-AI-Portfolio/
│
├── Project-01-RAG-From-Scratch/
│   ├── data/
│   ├── src/
│   ├── tests/
│   ├── .env.example
│   ├── .gitignore
│   ├── README.md
│   └── requirements.txt
│
├── Project-02-Legal-AI-Assistant/
│   ├── data/
│   ├── src/
│   ├── tests/
│   ├── .env.example
│   ├── .gitignore
│   ├── pytest.ini
│   ├── README.md
│   └── requirements.txt
│
├── Project-03-Autonomous-Research-Agent/
│   ├── src/
│   ├── tests/
│   ├── .env.example
│   ├── .gitignore
│   ├── pytest.ini
│   ├── README.md
│   └── requirements.txt
│
├── Project-04-Multimodal-RAG-Engine/
│   ├── data/
│   ├── src/
│   ├── tests/
│   ├── .env.example
│   ├── .gitignore
│   ├── pytest.ini
│   ├── README.md
│   └── requirements.txt
│
├── Project-05-Realtime-Agentic-RAG/
│   ├── data/
│   ├── src/
│   ├── tests/
│   ├── .env.example
│   ├── .gitignore
│   ├── pytest.ini
│   ├── README.md
│   └── requirements.txt
│
└── README.md
```

---

# 🚀 How to Explore the Portfolio

The recommended order is:

### 1️⃣ Start with Project 01

Understand the fundamentals of:

```text
Documents
 ↓
Embeddings
 ↓
Vector Search
 ↓
Context
 ↓
Generation
```

### 2️⃣ Continue to Project 02

See how RAG concepts can be applied to a specialized enterprise domain with structured outputs and deterministic citation verification.

### 3️⃣ Continue to Project 03

Study how tool calling and iterative reasoning transform a fixed application into an autonomous research workflow.

### 4️⃣ Continue to Project 04

Explore how Vision LLMs and dual representations extend RAG beyond text.

### 5️⃣ Finish with Project 05

Understand how dynamic routing, retrieval evaluation, corrective retrieval, live search, caching, and telemetry can be combined into a more production-oriented agentic RAG architecture.

---

# 🎯 Skills Demonstrated

This portfolio demonstrates practical experience with:

### Generative AI

* Large Language Models
* Prompt Engineering
* Structured Generation
* Vision LLMs
* Multimodal Generation

### Retrieval-Augmented Generation

* Document Retrieval
* Embeddings
* Vector Search
* Context Assembly
* Citation Grounding
* Retrieval Evaluation
* Corrective RAG

### Agentic AI

* Tool Calling
* Function Calling
* Tool Registries
* Autonomous Loops
* Conditional Workflows
* Agent Reflection
* Dynamic Routing

### Multimodal AI

* Image Understanding
* Visual Summarization
* Chart Understanding
* Table Understanding
* Technical Diagram Understanding
* Cross-Modal Retrieval

### Engineering

* Python
* API Integration
* Redis
* Automated Testing
* Modular Architecture
* Error Handling
* Environment Configuration
* Telemetry

---

# 📊 Architecture Complexity Progression

```text
Project 01
────────────────────────
RAG Pipeline
Retrieval → Generation


Project 02
────────────────────────
Structured Enterprise AI
Analysis → Schema → Validation


Project 03
────────────────────────
Autonomous Agent
Reason → Tool → Observe → Iterate


Project 04
────────────────────────
Multimodal RAG
Vision → Representation → Retrieval → Generation


Project 05
────────────────────────
Real-Time Agentic RAG
Route → Retrieve → Evaluate → Correct → Generate → Verify
```

---

# 🔬 Engineering Principles

The portfolio emphasizes several important AI engineering principles.

## 1. Retrieval Before Generation

Relevant evidence should be retrieved before asking the model to generate an answer.

---

## 2. Structured Outputs

Where possible, model outputs should be represented using explicit schemas instead of relying entirely on free-form text.

---

## 3. Deterministic Validation

Important behaviors should have deterministic checks wherever practical.

---

## 4. Separation of Responsibilities

Major system responsibilities are separated into components such as:

```text
Router
Retriever
Evaluator
Generator
Verifier
Cache
Telemetry
```

This improves maintainability and makes individual components easier to test.

---

## 5. External Services Should Be Isolated

External API calls are wrapped behind dedicated components.

This allows core application logic to be tested independently.

---

## 6. Prototype vs Production

The portfolio intentionally distinguishes between:

```text
Working Prototype
```

and:

```text
Production Extension
```

Production-grade systems would require additional considerations such as:

* Security
* Authentication
* Authorization
* Monitoring
* Reliability
* Scaling
* Persistent storage
* Rate limiting
* Failure recovery
* Evaluation
* Cost management

The portfolio does not claim production benchmark results that have not actually been measured.

---

# 🏭 Production-Oriented Extensions

The projects provide foundations that could be extended into production systems.

Potential extensions include:

```text
                    Production AI System
                            │
          ┌─────────────────┼─────────────────┐
          │                 │                 │
          ▼                 ▼                 ▼
    Vector Database      Model Layer      Observability
          │                 │                 │
          ▼                 ▼                 ▼
    Persistent State    Guardrails        Telemetry
          │                 │                 │
          └─────────────────┼─────────────────┘
                            │
                            ▼
                    Agentic Orchestration
```

Potential technologies include:

* FAISS
* Pinecone
* Redis
* LangGraph
* LangSmith
* Arize Phoenix
* RAGAS
* TruLens

---

# 📈 Evaluation

The portfolio can be evaluated using different criteria depending on the project.

### Retrieval Systems

* Retrieval relevance
* Context relevance
* Retrieval precision
* Retrieval recall

### Generation Systems

* Answer relevance
* Groundedness
* Faithfulness

### Agentic Systems

* Tool-selection accuracy
* Successful task completion
* Iteration efficiency
* Failure recovery

### Multimodal Systems

* Visual understanding
* Cross-modal retrieval accuracy
* Table/chart interpretation

The final Real-Time Agentic RAG architecture can additionally be evaluated using RAG-specific metrics such as Context Relevance, Groundedness/Faithfulness, and Answer Relevance. 

---

# 🧠 What This Portfolio Demonstrates

Rather than demonstrating five unrelated AI projects, this repository demonstrates a single evolving engineering story:

```text
How do we build increasingly capable AI systems?
```

The answer demonstrated through the portfolio is:

```text
Start with Retrieval
        ↓
Add Structure
        ↓
Add Validation
        ↓
Add Tools
        ↓
Add Autonomy
        ↓
Add Vision
        ↓
Add Multimodal Retrieval
        ↓
Add Dynamic Routing
        ↓
Evaluate Retrieval
        ↓
Correct Failures
        ↓
Integrate Live Information
        ↓
Cache Responses
        ↓
Track System Behavior
```

---

# 🏆 Final Portfolio Architecture

```text
                         AGENTIC AI PORTFOLIO
                                  │
                                  ▼
                    ┌─────────────────────────┐
                    │     RAG FOUNDATION      │
                    │       PROJECT 01        │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │   STRUCTURED DOMAIN AI  │
                    │       PROJECT 02        │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │   AUTONOMOUS TOOL USE   │
                    │       PROJECT 03        │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │    MULTIMODAL RAG       │
                    │       PROJECT 04        │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │  REAL-TIME AGENTIC RAG  │
                    │       PROJECT 05        │
                    └─────────────────────────┘
```

---

# 👨‍💻 Author

**Sciddhanto Sinha**

B.Tech – Computer Science Engineering (AI & Analytics)

### Agentic AI Portfolio

Python • RAG • Agentic AI • Generative AI • Multimodal AI • LLM Applications

**For now, only create/update this root `README.md`. Don't touch the Project 05 local pull issue yet.**
