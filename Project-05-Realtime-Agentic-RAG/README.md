# ⚡ Real-Time Agentic RAG System

### Dynamic Query Routing, Corrective RAG (CRAG), and Live API Telemetry Integration

## 📌 Project Overview

Traditional Retrieval-Augmented Generation (RAG) systems generally depend on a fixed retrieval pipeline.

However, real-world enterprise questions can require information from multiple sources:

- Private internal knowledge
- Current web information
- News
- Market information
- Weather
- Live system information
- Other external APIs

A static RAG pipeline can struggle when its retrieved context is irrelevant, incomplete, or outdated.

This project addresses that limitation by implementing a **Real-Time Agentic RAG architecture** based on **Dynamic Query Routing and Corrective RAG (CRAG)**.

The system can:

1. Determine whether a query requires internal or live information.
2. Retrieve information from the appropriate source.
3. Evaluate the relevance of retrieved context.
4. Automatically trigger live-search fallback when internal retrieval is insufficient.
5. Generate a response using the selected evidence.
6. Perform a lightweight grounding check before returning the response.
7. Cache responses using Redis.
8. Record pipeline telemetry such as routing, retrieval, fallback, and execution time.

---

## 🚀 Key Features

- **Dynamic Query Routing** — Determines whether a query should use internal knowledge or live search.
- **Corrective RAG (CRAG)** — Evaluates retrieved context before generation.
- **Internal Knowledge Retrieval** — Searches an internal knowledge collection.
- **Live Web Search** — Uses Tavily for fresh external information.
- **Automatic Retrieval Fallback** — Performs corrective live search when internal evidence is insufficient.
- **Grounded Generation** — Generates responses using retrieved evidence.
- **Hallucination Protection** — Performs a lightweight grounding check before releasing the generated response.
- **Redis Response Cache** — Stores previously generated responses with configurable TTL.
- **Pipeline Telemetry** — Records routing, retrieval, fallback, and completion events.
- **Testable Architecture** — External APIs are isolated so the core workflow can be tested without live services.

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core implementation |
| OpenAI API | Response generation |
| Tavily | Live web search |
| Redis | Response caching |
| Pytest | Automated testing |
| python-dotenv | Environment configuration |
| GitHub | Version control and portfolio hosting |

---

## 🏗️ Architecture

```text
                         ┌──────────────────────┐
                         │      User Query      │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │   Semantic Router    │
                         └──────────┬───────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    │                               │
                    ▼                               ▼
          ┌──────────────────┐            ┌──────────────────┐
          │ Internal         │            │ Live Search API  │
          │ Retriever        │            │ Tavily           │
          └────────┬─────────┘            └────────┬─────────┘
                   │                               │
                   ▼                               │
          ┌──────────────────┐                     │
          │ Retrieval        │                     │
          │ Evaluator        │                     │
          └────────┬─────────┘                     │
                   │                               │
                   ▼                               │
             ┌───────────┐                         │
             │ Relevant? │                         │
             └─────┬─────┘                         │
                   │                               │
              ┌────┴────┐                          │
              │         │                          │
             YES        NO                         │
              │         │                          │
              │         └──────────────────────────┘
              │
              ▼
       ┌──────────────────┐
       │ Context Assembly │
       └────────┬─────────┘
                │
                ▼
       ┌──────────────────┐
       │ Answer Generator │
       └────────┬─────────┘
                │
                ▼
       ┌──────────────────┐
       │ Grounding Check  │
       └────────┬─────────┘
                │
                ▼
       ┌──────────────────┐
       │ Audited Response │
       └──────────────────┘
````

---

## 🔄 Workflow

The Real-Time Agentic RAG workflow is:

```text
                         User Query
                              ↓
                       Semantic Router
                              ↓
                 ┌────────────┴────────────┐
                 │                         │
                 ▼                         ▼
             INTERNAL                    LIVE
                 │                         │
                 ▼                         ▼
        Internal Retrieval          Tavily Search
                 │                         │
                 ▼                         │
        Retrieval Evaluation              │
                 │                         │
            ┌────┴────┐                    │
            │         │                    │
        Relevant   Irrelevant              │
            │         │                    │
            │         └────────────────────┘
            │
            ▼
       Context Assembly
            ↓
      Answer Generation
            ↓
       Grounding Check
            ↓
       Final Response
```

---

## 1. Query Intake

The system receives a natural-language query from the user.

Example:

```text
What is the latest news about AI?
```

or:

```text
Explain our internal deployment policy.
```

The query is then passed to the routing layer.

---

## 2. Dynamic Query Routing

The `SemanticRouter` determines which retrieval path should handle the request.

The two available routes are:

```text
INTERNAL
LIVE
```

Queries containing signals associated with current information are routed toward live search.

Examples include:

```text
Latest
Current
Today
Recent
Live
News
Stock
Weather
Market
```

An internal knowledge query is routed toward the internal retriever.

Example:

```text
Explain our internal deployment policy.
```

Expected route:

```text
INTERNAL
```

A current-information query such as:

```text
What is the current stock price?
```

is routed toward:

```text
LIVE
```

The current implementation uses deterministic semantic signals so that the routing behavior remains transparent and testable.

---

## 3. Internal Retrieval

The `InternalRetriever` provides access to the internal knowledge collection.

The current prototype stores knowledge chunks in memory.

Each document contains:

```text
Document ID
Content
Metadata
```

The retriever performs lightweight token-overlap scoring.

Conceptually:

```text
User Query
    ↓
Tokenization
    ↓
Compare with Knowledge Chunks
    ↓
Calculate Overlap
    ↓
Rank Results
    ↓
Return Top-K
```

The retrieval interface is intentionally isolated so that the prototype can later be connected to:

* FAISS
* Pinecone
* Another vector database
* Embedding-based retrieval

without changing the CRAG orchestration layer.

---

## 4. Live Search

Queries requiring current external information can be routed to Tavily.

The `LiveSearch` component provides a simple interface:

```python
search(
    query,
    max_results
)
```

The external search response is normalized into:

```text
Title
Content
URL
Score
```

This allows live search results to enter the same downstream generation workflow.

---

## 5. Retrieval Evaluation

One of the key differences between this architecture and a fixed RAG pipeline is the explicit evaluation of retrieved evidence.

The `RetrievalEvaluator` calculates a normalized relevance score.

The prototype uses:

```text
Relevance Score =
Matching Query Tokens
────────────────────────
Total Query Tokens
```

The resulting score is between:

```text
0.0
```

and:

```text
1.0
```

A configurable threshold determines whether the retrieved internal context is sufficiently relevant.

---

## 6. Corrective RAG (CRAG)

The central architectural concept is **Corrective RAG**.

Instead of assuming that the first retrieval result is correct, the system evaluates the retrieved context.

```text
Internal Retrieval
        ↓
Evaluate Relevance
        ↓
 ┌──────┴──────┐
 │             │
Good          Poor
 │             │
 ▼             ▼
Generate    Live Search
              ↓
           Generate
```

If the internal context is sufficiently relevant:

```text
Internal Context
       ↓
   Generation
```

If the internal context fails the relevance threshold:

```text
Internal Context
       ↓
  Low Relevance
       ↓
Corrective Fallback
       ↓
  Live Search
       ↓
  Generation
```

This allows the system to recover from poor internal retrieval.

---

## 7. Live Search Fallback

When internal retrieval does not provide sufficiently relevant evidence, the CRAG pipeline automatically triggers the live-search path.

Example:

```text
User Query
    ↓
Internal Retrieval
    ↓
Low Relevance
    ↓
Tavily Search
    ↓
Fresh External Evidence
    ↓
Answer Generation
```

The pipeline records whether this corrective fallback occurred.

Example result field:

```python
{
    "fallback_triggered": True
}
```

---

## 8. Context Assembly

Retrieved evidence is converted into a structured generation context.

For internal documents:

```text
Document ID
Content
Metadata
```

For live search:

```text
Title
Content
URL
Score
```

The context is then passed to the generation model together with the original user query.

---

## 9. Grounded Generation

The generation layer uses the OpenAI API.

The model is instructed to:

* Answer from supplied context.
* Avoid inventing unsupported information.
* State when evidence is insufficient.
* Use retrieved evidence as the basis for the response.

Conceptually:

```text
User Query
     +
Retrieved Evidence
     ↓
Generation Model
     ↓
Candidate Answer
```

---

## 10. Hallucination / Grounding Check

Before returning the generated answer, the system performs a lightweight grounding check.

The current prototype compares meaningful answer tokens with tokens contained in the retrieved evidence.

```text
Generated Answer
       ↓
Grounding Check
       ↓
 ┌─────┴─────┐
 │           │
Pass        Fail
 │           │
 ▼           ▼
Return     Withhold
Answer     Response
```

If the answer does not pass the grounding check, the pipeline withholds the response.

This implementation is intentionally lightweight and should not be considered a replacement for production-grade faithfulness or hallucination evaluation.

---

# 💾 Redis Response Cache

## Cache Architecture

The project includes a Redis-backed `SemanticCache`.

The current prototype uses normalized-query hashing rather than embedding-based similarity.

```text
User Query
    ↓
Normalize Query
    ↓
SHA-256 Hash
    ↓
Redis Key
    ↓
Cached Response
```

The cache supports:

* `get()`
* `set()`
* `delete()`
* `clear()`
* TTL-based expiration

Example:

```python
cache.set(
    "What is AI?",
    {
        "answer": "Cached response"
    }
)
```

A production implementation can replace the normalized-query key with embedding-based semantic similarity.

---

## 📡 Pipeline Telemetry

The `TelemetryTracker` provides lightweight observability for the pipeline.

It can record events such as:

```text
Routing
Retrieval
Fallback
Generation
Pipeline Completion
```

Each event can contain metadata.

Example:

```python
tracker.record(
    event="retrieval",
    metadata={
        "source": "internal"
    }
)
```

The tracker also measures execution time.

```text
Pipeline Start
      ↓
Record Events
      ↓
Pipeline Complete
      ↓
Execution Time
```

The telemetry layer provides a foundation for connecting the system to observability platforms such as:

* LangSmith
* Arize Phoenix

---

# 🧩 Core Components

## `router.py`

Responsible for:

* Query classification
* Internal/live route selection
* Detection of current-information signals

Main component:

```python
SemanticRouter
```

---

## `retriever.py`

Responsible for:

* Internal knowledge storage
* Document ingestion
* Query matching
* Relevance ranking

Main component:

```python
InternalRetriever
```

---

## `live_search.py`

Responsible for:

* Tavily API integration
* Live web search
* External result normalization

Main component:

```python
LiveSearch
```

---

## `evaluator.py`

Responsible for:

* Retrieval relevance scoring
* Relevance threshold evaluation
* CRAG decision support

Main component:

```python
RetrievalEvaluator
```

---

## `crag_pipeline.py`

Responsible for the central orchestration workflow:

* Routing
* Retrieval
* Relevance evaluation
* Corrective fallback
* Context assembly
* Generation
* Grounding verification

Main component:

```python
CRAGPipeline
```

---

## `cache.py`

Responsible for:

* Redis response caching
* Query normalization
* Cache key generation
* TTL management
* Cache invalidation

Main component:

```python
SemanticCache
```

---

## `telemetry.py`

Responsible for:

* Pipeline event tracking
* Metadata collection
* Execution-time measurement
* Telemetry summaries

Main component:

```python
TelemetryTracker
```

---

# 📂 Project Structure

```text
Project-05-Realtime-Agentic-RAG/
│
├── data/
│   └── .gitkeep
│
├── src/
│   ├── __init__.py
│   ├── router.py
│   ├── retriever.py
│   ├── live_search.py
│   ├── evaluator.py
│   ├── crag_pipeline.py
│   ├── cache.py
│   └── telemetry.py
│
├── tests/
│   ├── test_router.py
│   ├── test_retriever.py
│   ├── test_live_search.py
│   ├── test_evaluator.py
│   ├── test_cache.py
│   ├── test_telemetry.py
│   ├── test_crag_pipeline.py
│   └── test_document_flow.py
│
├── .env.example
├── .gitignore
├── pytest.ini
├── README.md
└── requirements.txt
```

---

# ⚙️ Requirements & Setup

## Requirements

* Python 3.10+
* OpenAI API key for live generation
* Tavily API key for live search
* Redis for response caching
* pip
* Git
* Internet connection for external API requests

---

## Environment Configuration

Create a local `.env` file based on:

```text
.env.example
```

Configure:

```env
OPENAI_API_KEY=your_openai_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
REDIS_URL=redis://localhost:6379
```

Do not commit real API credentials to GitHub.

The `.gitignore` file excludes:

```text
.env
```

from version control.

---

# 📥 Setup

## 1. Clone the Repository

```bash
git clone https://github.com/SciddhantoSinha/Agentic-AI-Portfolio.git
```

## 2. Navigate to Project 05

```bash
cd Agentic-AI-Portfolio/Project-05-Realtime-Agentic-RAG
```

## 3. Create a Virtual Environment

```bash
python -m venv .venv
```

## 4. Activate the Environment on Windows

```bash
.venv\Scripts\activate
```

## 5. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ How to Run

The CRAG pipeline can be initialized with the required services:

```python
from src.crag_pipeline import CRAGPipeline
from src.live_search import LiveSearch
from src.retriever import InternalRetriever

live_search = LiveSearch(
    api_key="your_tavily_api_key"
)

retriever = InternalRetriever()

retriever.add_document(
    document_id="policy-1",
    content=(
        "The deployment process uses Docker "
        "containers for production."
    )
)

pipeline = CRAGPipeline(
    api_key="your_openai_api_key",
    live_search=live_search,
    internal_retriever=retriever,
)
```

A query can then be executed:

```python
result = pipeline.run(
    "How does the deployment process use Docker?"
)

print(result["answer"])
```

The returned structure contains information such as:

```python
{
    "route": "...",
    "documents": [...],
    "relevance_score": 0.0,
    "fallback_triggered": False,
    "answer": "...",
    "grounded": True,
}
```

---

# 🧪 Testing

The project includes automated tests for:

* Query routing
* Internal document ingestion
* Internal retrieval
* Retrieval ranking
* Live search normalization
* Retrieval evaluation
* Redis cache behavior
* Telemetry collection
* CRAG orchestration
* Corrective fallback
* Grounding behavior
* End-to-end document flow

The test architecture mocks external dependencies where appropriate.

This allows the core pipeline behavior to be tested without requiring:

* A live OpenAI request
* A live Tavily request
* A running Redis instance

Run the complete test suite with:

```bash
pytest
```

---

# 🎯 Example Routing Scenarios

## Internal Knowledge Query

```text
Explain our internal deployment policy.
```

Expected route:

```text
INTERNAL
```

Workflow:

```text
Query
 ↓
Semantic Router
 ↓
Internal Retriever
 ↓
Retrieval Evaluator
 ↓
Generation
 ↓
Grounding Check
 ↓
Response
```

---

## Live Information Query

```text
What is the latest news about AI?
```

Expected route:

```text
LIVE
```

Workflow:

```text
Query
 ↓
Semantic Router
 ↓
Tavily Search
 ↓
Generation
 ↓
Grounding Check
 ↓
Response
```

---

## Corrective Retrieval Query

A query may initially enter the internal retrieval path but fail the relevance threshold.

Workflow:

```text
Query
 ↓
Internal Retrieval
 ↓
Low Relevance
 ↓
CRAG Fallback
 ↓
Tavily Search
 ↓
Fresh Evidence
 ↓
Generation
 ↓
Grounding Check
 ↓
Response
```

This is the core corrective behavior of the project.

---

# 📊 CRAG Decision Logic

```text
                    User Query
                        │
                        ▼
                 Semantic Router
                        │
             ┌──────────┴──────────┐
             │                     │
             ▼                     ▼
         INTERNAL                  LIVE
             │                     │
             ▼                     ▼
      Internal Retrieval       Tavily Search
             │                     │
             ▼                     │
     Retrieval Evaluator            │
             │                     │
        ┌────┴────┐                │
        │         │                │
    Relevant   Irrelevant          │
        │         │                │
        │         └────────────────┘
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

---

# 📈 Evaluation Framework

The architecture can be evaluated using RAG-specific metrics such as:

| Metric                      | Purpose                                                        |
| --------------------------- | -------------------------------------------------------------- |
| Context Relevance           | Measures whether retrieved context is relevant to the query    |
| Groundedness / Faithfulness | Measures whether the answer is supported by retrieved evidence |
| Answer Relevance            | Measures whether the final response addresses the query        |

Potential evaluation frameworks include:

* RAGAS
* TruLens

The current repository focuses on implementing the core architecture rather than claiming benchmark results that have not been measured.

---

# 🔬 Architecture Trade-Offs

## Fixed RAG vs Corrective RAG

A fixed RAG system follows:

```text
Query
 ↓
Retrieve
 ↓
Generate
```

The CRAG architecture adds an explicit evaluation stage:

```text
Query
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
```

This provides an additional control layer between retrieval and generation.

---

## Internal Knowledge vs Live Search

### Internal Retrieval

Advantages:

* Private knowledge access
* Controlled information source
* Predictable knowledge boundary

Limitations:

* Information can become outdated
* Retrieval may return irrelevant context
* Knowledge may be incomplete

### Live Search

Advantages:

* Access to current information
* Useful for news and dynamic topics
* Can recover from missing internal evidence

Limitations:

* External dependency
* Network latency
* Search-result variability
* Additional API cost

The dynamic router and corrective fallback allow the system to combine both approaches.

---

# 💾 Caching Trade-Off

The current prototype uses normalized-query hashing.

Advantages:

* Deterministic
* Simple
* Fast
* Easy to test
* Redis compatible

Limitation:

Two semantically equivalent but differently worded questions may not produce the same cache key.

For example:

```text
What is the current AI market?
```

and:

```text
How is the AI market doing right now?
```

would produce different normalized-query hashes.

A production semantic cache can instead use:

```text
Query
 ↓
Embedding
 ↓
Similarity Search
 ↓
Similarity Threshold
 ↓
Cache Hit / Miss
```

---

# 🏭 Production Architecture

A production version of this project can extend the prototype with:

```text
                    ┌──────────────────┐
                    │    User Query    │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Semantic Router  │
                    └────────┬─────────┘
                             │
                ┌────────────┴────────────┐
                │                         │
                ▼                         ▼
        ┌───────────────┐         ┌───────────────┐
        │ Vector Store  │         │ Live APIs/Web │
        │               │         │               │
        └───────┬───────┘         └───────┬───────┘
                │                         │
                └────────────┬────────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ CRAG Evaluator   │
                    └────────┬─────────┘
                             │
                    ┌────────┴────────┐
                    │                 │
                  PASS              FAIL
                    │                 │
                    │                 ▼
                    │          Corrective Search
                    │                 │
                    └────────┬────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Generation Model │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Faithfulness     │
                    │ Verification     │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Final Response   │
                    └──────────────────┘
```

Potential production enhancements include:

* Embedding-based semantic routing
* Production vector databases
* Embedding-based semantic caching
* Redis persistence
* LLM-based retrieval grading
* Advanced hallucination detection
* RAGAS evaluation
* TruLens evaluation
* LangSmith tracing
* Arize Phoenix observability
* Authentication and authorization
* Rate limiting
* Retry handling
* API failure recovery
* Persistent conversation state

---

# 📡 Production Observability

The current telemetry layer can be extended to track:

```text
Query
 ↓
Routing Decision
 ↓
Retrieval Source
 ↓
Retrieved Documents
 ↓
Relevance Score
 ↓
Fallback Decision
 ↓
Generation
 ↓
Grounding Result
 ↓
Latency
```

Production observability can additionally track:

* Latency
* Tool calls
* Token consumption
* Retrieval quality
* Failure rates
* Fallback frequency
* Cache hit rate
* API errors

This provides visibility into the behavior of an agentic RAG system.

---

# 🎯 Use Cases

Potential applications include:

* Enterprise knowledge assistants
* Real-time business intelligence
* Financial information assistants
* Internal company copilots
* News-aware research assistants
* Technical support systems
* Operations monitoring
* Dynamic knowledge assistants
* Current-information research workflows

---

# 💡 Benefits

* Combines internal and external knowledge sources
* Handles time-sensitive queries
* Evaluates retrieval before generation
* Automatically recovers from poor internal retrieval
* Adds a grounding layer before response release
* Provides Redis-backed response caching
* Records pipeline telemetry
* Separates routing, retrieval, evaluation, and generation responsibilities
* Provides a foundation for production agentic RAG systems

---

# 🧠 Skills Demonstrated

* Agentic RAG
* Retrieval-Augmented Generation
* Corrective RAG (CRAG)
* Dynamic Query Routing
* Retrieval Evaluation
* Live API Integration
* Tavily Search
* OpenAI API Integration
* Redis Caching
* Grounding Verification
* Hallucination Mitigation
* Pipeline Telemetry
* Python
* API Design
* Unit Testing
* Integration Testing
* Agentic Workflow Architecture

---

# 📈 Project Progression

This project represents the **fifth and final layer** of the Agentic AI portfolio:

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

# 🔥 Portfolio Architecture Progression

Across the five projects, the portfolio demonstrates increasingly sophisticated AI system design:

```text
┌──────────────────────────────────────────────┐
│ Project 01                                   │
│ RAG Fundamentals                             │
│ Retrieval + Generation                       │
└──────────────────────┬───────────────────────┘
                       ↓
┌──────────────────────────────────────────────┐
│ Project 02                                   │
│ Legal AI                                     │
│ Structured Output + Citation Grounding       │
└──────────────────────┬───────────────────────┘
                       ↓
┌──────────────────────────────────────────────┐
│ Project 03                                   │
│ Autonomous Research                         │
│ Tool Calling + Iterative Agent Loop          │
└──────────────────────┬───────────────────────┘
                       ↓
┌──────────────────────────────────────────────┐
│ Project 04                                   │
│ Multimodal RAG                               │
│ Vision + Dual Representation                │
└──────────────────────┬───────────────────────┘
                       ↓
┌──────────────────────────────────────────────┐
│ Project 05                                   │
│ Real-Time Agentic RAG                        │
│ Routing + CRAG + Live Search + Verification  │
└──────────────────────────────────────────────┘
```

---

# 🧪 Current Prototype vs Production System

The current repository intentionally focuses on demonstrating the architecture and control flow.

| Component          | Current Prototype              | Production Extension                |
| ------------------ | ------------------------------ | ----------------------------------- |
| Routing            | Deterministic semantic signals | Embedding/LLM semantic router       |
| Internal Retrieval | In-memory token overlap        | Vector database                     |
| Live Search        | Tavily                         | Multiple live APIs/search providers |
| Evaluation         | Token-overlap relevance        | LLM/RAG evaluation                  |
| Cache              | Redis + query hash             | Embedding-based semantic cache      |
| Grounding          | Lightweight token overlap      | Faithfulness evaluator              |
| Telemetry          | Local event tracker            | LangSmith / Arize Phoenix           |
| State              | In-memory                      | Persistent state/checkpointing      |

This distinction keeps the portfolio implementation technically honest while providing a clear path toward production architecture.

---

# ⚠️ Important Disclaimer

This project is an educational and portfolio implementation demonstrating an agentic RAG architecture.

The current relevance evaluator, cache key strategy, and grounding check are intentionally lightweight prototypes.

The system should not be considered production-ready without additional:

* Security controls
* Evaluation
* Monitoring
* Reliability engineering
* Authentication
* Authorization
* Rate limiting
* Failure handling
* Domain-specific validation

Live search results and generated responses should also be independently verified before being used for high-stakes decisions.

---

# 👨‍💻 Author

**Sciddhanto Sinha**

B.Tech – Computer Science Engineering (AI & Analytics)

**Stop here.** Tell me `done`.
