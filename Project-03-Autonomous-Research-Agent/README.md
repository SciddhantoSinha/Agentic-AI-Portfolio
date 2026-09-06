# 🤖 Autonomous Research Agent

An autonomous Agentic AI system that investigates research topics through iterative tool calling, retrieves academic papers from ArXiv, evaluates research evidence, detects unsuccessful searches, reflects on its strategy, and safely terminates after bounded iterations.

## 📌 Project Overview

Traditional RAG systems generally follow a fixed retrieval pipeline:

```text
Query
  ↓
Retrieve
  ↓
Generate
````

This project introduces an autonomous research workflow where the agent can iteratively decide whether additional research is required.

The system combines:

* LLM-based tool calling
* Dynamic tool registration
* ArXiv research retrieval
* ReAct-style iterative execution
* Tool-call hashing
* Zero-yield observation detection
* Scratchpad reflection
* Maximum iteration safeguards
* Automated testing

The agent receives a research topic, decides whether to use the available research tool, retrieves academic evidence, feeds the observation back into the reasoning loop, and eventually produces a final research response.

---

## 🚀 Key Features

* **Autonomous Tool Calling** — Allows the LLM to decide when an external research tool is required.
* **ArXiv Integration** — Searches ArXiv for relevant academic papers and retrieves titles and abstracts.
* **Dynamic Tool Registry** — Provides a reusable mechanism for registering and dispatching agent tools.
* **ReAct-Style Loop** — Enables iterative Tool → Observation → Reasoning cycles.
* **Maximum Iteration Control** — Prevents uncontrolled autonomous execution.
* **Tool-Call Hashing** — Detects identical consecutive tool calls.
* **Zero-Yield Detection** — Identifies searches that return no useful evidence.
* **Scratchpad Reflection** — Forces a strategy reassessment after repeated unsuccessful searches.
* **Unknown Tool Protection** — Rejects tool requests that are not registered.
* **Deterministic Safety Logic** — Keeps critical loop-control mechanisms outside the LLM.

---

## 🛠️ Technologies Used

| Technology              | Purpose                                              |
| ----------------------- | ---------------------------------------------------- |
| Python                  | Core implementation                                  |
| OpenAI API              | LLM reasoning and tool calling                       |
| ArXiv API               | Academic research retrieval                          |
| LangGraph               | Production-oriented agent state management concept   |
| Pytest                  | Automated testing                                    |
| Python Standard Library | XML parsing, HTTP requests, hashing, JSON processing |
| GitHub                  | Version control and portfolio hosting                |

---

## 🏗️ Architecture

```text
                         ┌──────────────────────┐
                         │    Research Topic    │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │      OpenAI LLM      │
                         │                      │
                         │  Reason + Decide     │
                         └──────────┬───────────┘
                                    │
                              Tool Required?
                              ↙           ↘
                            No             Yes
                            │               │
                            ▼               ▼
                     Final Response   Tool Registry
                                            │
                                            ▼
                                     search_arxiv()
                                            │
                                            ▼
                                       ArXiv API
                                            │
                                            ▼
                                       Observation
                                            │
                                            ▼
                                           LLM
                                            │
                              ┌─────────────┴─────────────┐
                              │                           │
                       Useful Evidence              No Useful Evidence
                              │                           │
                              ▼                           ▼
                       Continue Loop              Reflection Trigger
                                                          │
                                                          ▼
                                                   Strategy Pivot
```

---

## 🔄 Workflow

The autonomous research workflow is:

```text
Research Topic
      ↓
LLM Reasoning
      ↓
Determine Whether Research Tool Is Required
      ↓
Tool Call
      ↓
ArXiv Search
      ↓
Research Observation
      ↓
Feed Observation Back to LLM
      ↓
Evaluate Evidence
      ↓
Continue / Reflect / Stop
      ↓
Final Research Response
```

### 1. Research Input

The system receives a research topic from the user.

Example:

```text
Investigate approaches to retrieval augmented generation.
```

### 2. Agent Reasoning

The OpenAI model determines whether it needs to invoke an available research tool.

The model receives an OpenAI-compatible tool definition for:

```text
search_arxiv
```

### 3. Tool Invocation

When research is required, the agent extracts:

* Tool name
* Query parameters
* Maximum number of results

The requested tool is then dispatched through the `ToolRegistry`.

### 4. Academic Retrieval

The ArXiv tool:

1. Constructs an ArXiv API query
2. Sends the request
3. Retrieves the XML response
4. Parses academic paper entries
5. Extracts titles
6. Extracts abstracts
7. Returns formatted research observations

### 5. Observation

The retrieved research evidence is added to the conversation as a tool observation.

The LLM can then use that evidence to determine whether additional research is required.

### 6. Iterative Research

The agent can continue through multiple iterations.

This creates a ReAct-style workflow:

```text
Thought
   ↓
Action
   ↓
Observation
   ↓
Thought
   ↓
Action
   ↓
Observation
   ↓
Final Answer
```

### 7. Final Response

When the model produces a response without requesting another tool call, the agent returns that response as the final research output.

---

## 🧰 Dynamic Tool Registry

The project implements a reusable `ToolRegistry`.

The registry stores:

1. Python functions used to execute tools.
2. OpenAI-compatible function definitions provided to the LLM.

Current registered tool:

```text
search_arxiv
```

The registry allows tools to be dynamically registered using:

```python
registry.register(
    name="tool_name",
    description="Tool description",
    parameters={...}
)(tool_function)
```

This separates tool registration from the core agent loop.

---

## 🔎 ArXiv Research Tool

The project integrates the ArXiv API using Python's standard library.

The tool is implemented in:

```text
src/arxiv_tool.py
```

It accepts:

```python
search_arxiv(
    query="retrieval augmented generation",
    max_results=3
)
```

The returned information contains:

```text
Title: <research paper title>
Abstract: <research paper abstract>
```

Multiple results are separated using:

```text
---
```

The implementation parses the ArXiv Atom XML response using Python's XML parser.

---

## 🧠 ReAct-Style Autonomous Loop

The agent implements an iterative reasoning and tool-execution loop.

Conceptually:

```text
┌──────────────┐
│    Agent     │
└──────┬───────┘
       │
       ▼
   Need Tool?
    /     \
  No       Yes
  │         │
  ▼         ▼
Final    Tool Call
Answer      │
            ▼
       Tool Execution
            │
            ▼
       Observation
            │
            ▼
          Agent
```

This differs from a fixed RAG pipeline because the number of tool interactions is determined dynamically within a bounded execution limit.

---

## 🛡️ Agent Safety Mechanisms

Autonomous loops require explicit safeguards to prevent uncontrolled execution.

### 1. Maximum Iteration Bound

The agent accepts:

```python
max_steps=5
```

This places an upper limit on the number of LLM iterations.

If the agent reaches the limit without producing a final response, it returns:

```text
Max iteration depth reached without complete convergence.
```

This prevents an autonomous loop from running indefinitely.

---

### 2. Tool-Call Hashing

Every tool invocation is converted into a deterministic SHA-256 hash.

The hash is based on:

```text
Tool Name
+
Tool Arguments
```

For example:

```python
{
    "tool": "search_arxiv",
    "arguments": {
        "query": "retrieval augmented generation",
        "max_results": 3
    }
}
```

The arguments are serialized with sorted keys before hashing.

This ensures that the same tool call produces the same hash even when the argument dictionary order changes.

---

### 3. Consecutive Tool-Call Detection

The agent stores the hash of the previous tool call.

If the next tool call produces the same hash, execution stops.

The agent returns:

```text
Agent stopped because the same tool call was requested consecutively.
```

This protects against repetitive tool invocation.

---

### 4. Unknown Tool Protection

Before executing a requested function, the agent verifies that the tool exists in the registry.

If an unregistered tool is requested, the system raises:

```text
ValueError
```

with:

```text
Unknown tool requested
```

This prevents arbitrary or unsupported tool execution.

---

### 5. Zero-Yield Observation Detection

The agent identifies observations that provide no useful research evidence.

Examples include:

```text
No papers found.
```

and:

```text
No papers found
```

An empty observation is also treated as zero-yield.

---

### 6. Scratchpad Reflection

If the agent receives two consecutive zero-yield observations, it triggers a reflection instruction.

The reflection tells the agent to:

* Re-evaluate its research strategy
* Identify missing information
* Avoid repeating the unsuccessful query
* Broaden or reformulate search terminology
* Consider alternative concepts
* Consider a narrower methodological angle

This creates a controlled strategy-pivot mechanism.

Conceptually:

```text
Search
  ↓
No Useful Evidence
  ↓
Search Again
  ↓
No Useful Evidence
  ↓
Reflection
  ↓
Re-evaluate Strategy
  ↓
Change Search Semantics
```

---

## 🧩 Core Components

The project consists of three primary source modules.

### `arxiv_tool.py`

Responsible for:

* ArXiv API communication
* Query construction
* XML parsing
* Paper extraction
* Research result formatting

### `tool_registry.py`

Responsible for:

* Tool registration
* Tool storage
* OpenAI-compatible tool definitions
* Dynamic tool dispatch

### `research_agent.py`

Responsible for:

* LLM interaction
* Tool calling
* Iterative execution
* Observation handling
* Tool-call hashing
* Loop protection
* Scratchpad reflection
* Final response generation

---

## 📂 Project Structure

```text
Project-03-Autonomous-Research-Agent/
│
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
├── pytest.ini
│
├── src/
│   ├── __init__.py
│   ├── arxiv_tool.py
│   ├── research_agent.py
│   └── tool_registry.py
│
└── tests/
    └── test_research_agent.py
```

---

## ⚙️ Requirements & Setup

### Requirements

* Python 3.10+
* OpenAI API key for live autonomous research
* pip
* Git
* Internet connection for ArXiv retrieval

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

Navigate to Project 03:

```bash
cd Agentic-AI-Portfolio/Project-03-Autonomous-Research-Agent
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

The agent can be initialized with an OpenAI API key:

```python
from src.research_agent import AutonomousResearchAgent

agent = AutonomousResearchAgent(
    api_key="your_openai_api_key"
)

result = agent.run(
    research_topic="Investigate retrieval augmented generation.",
    max_steps=5
)

print(result)
```

The agent can then:

```text
Research Topic
      ↓
OpenAI
      ↓
Tool Selection
      ↓
ArXiv
      ↓
Observation
      ↓
Further Reasoning
      ↓
Final Response
```

---

## 🧪 Testing

The project includes automated tests for:

* Dynamic tool registration
* Tool execution
* ArXiv tool registration
* OpenAI-compatible tool definitions
* Final-response behavior
* Deterministic tool-call hashing
* Hash changes when arguments change
* Unknown-tool rejection
* Zero-yield observation detection
* Non-empty observation handling
* Scratchpad reflection behavior

Run the complete test suite with:

```bash
pytest
```

Current test status:

```text
11 passed
```

The test suite does not require a live OpenAI API key.

---

## 🔬 Live ArXiv Integration

The ArXiv tool can be tested independently without invoking the OpenAI model.

Example:

```python
from src.arxiv_tool import search_arxiv

result = search_arxiv(
    "retrieval augmented generation",
    2
)

print(result)
```

This verifies that the project can communicate with ArXiv and parse returned academic research data.

---

## 🎯 Use Case

The project demonstrates how autonomous agents can be applied to research workflows where:

* Multiple research iterations may be required
* External academic evidence is needed
* Search strategies may need to change
* Tool calls must be controlled
* Autonomous execution requires safety boundaries
* Research findings need to be synthesized after evidence gathering

Potential applications include:

* Academic literature exploration
* Technology research
* Research trend discovery
* Literature review assistance
* Research gap identification
* Technical investigation

---

## 💡 Benefits

* Moves beyond fixed retrieval pipelines toward autonomous research workflows
* Demonstrates dynamic LLM tool calling
* Integrates a real academic research API
* Provides explicit safeguards for autonomous execution
* Detects repetitive tool calls
* Encourages strategy changes after unsuccessful searches
* Separates deterministic safety logic from LLM reasoning
* Provides automated tests for critical agent behavior

---

## 🧠 Skills Demonstrated

* Agentic Tool Calling
* ReAct State Loops
* Dynamic Tool Registration
* API Integration
* Academic Search
* XML Parsing
* LLM Application Architecture
* Tool-Call Hashing
* Infinite Loop Mitigation
* Scratchpad Reflection
* Iterative Evidence Gathering
* Python Testing

---

## 📈 Project Progression

This project represents the **third layer** of the Agentic AI portfolio:

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

The portfolio progressively moves from:

```text
Fixed Retrieval
      ↓
Domain-Constrained AI
      ↓
Autonomous Tool Calling
      ↓
Multimodal Intelligence
      ↓
Real-Time Agentic Systems
```

---

## 🏭 Production Architecture

The project handbook describes a production-oriented LangGraph architecture for managing autonomous research state.

The production design includes:

* Agent nodes
* Tool nodes
* Synthesis nodes
* Conditional transitions
* Conversation history
* Scratchpad notes
* Retrieved papers
* Iteration counters
* Persistent checkpoints
* Human-in-the-Loop state management

The current repository implements the autonomous research prototype and its loop-safety mechanisms. The full production LangGraph state graph is not yet implemented.

---

## ⚠️ Important Disclaimer

This project is a technical demonstration of autonomous AI research architecture.

LLM-generated research outputs should be independently verified before being used for academic, professional, scientific, or other high-stakes decisions.

---

## 👨‍💻 Author

**Sciddhanto Sinha**

B.Tech – Computer Science Engineering (AI & Analytics)


Then tell me **“done”**.
