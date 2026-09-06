# ⚖️ Enterprise Legal AI Assistant

A domain-constrained Legal AI system that analyzes contract text, produces strictly validated structured findings, assigns risk levels, and verifies that every cited clause is grounded in the original contract text.

## 📌 Project Overview

Standard conversational chatbots can be unreliable in high-stakes legal workflows because ambiguous outputs and hallucinated clauses can create serious liability.

This project addresses that problem by combining:

- Pydantic structured outputs
- Strict schema enforcement
- Domain-specific legal prompting
- Risk-level classification
- Automated citation grounding
- Deterministic auditing

The system analyzes contract text and returns a structured `ContractAnalysisReport` containing identified clause risks, exact contract quotations, explanations, suggested redlines, and an overall risk score.

## 🚀 Key Features

- **Strict Structured Output** — Uses Pydantic models to enforce a predictable response schema.
- **Risk Classification** — Classifies findings as `LOW`, `MEDIUM`, `HIGH`, or `CRITICAL`.
- **Exact Clause Citations** — Requires verbatim contract quotations for every finding.
- **Citation Grounding** — Verifies that every quoted clause exists exactly in the original contract text.
- **Risk Scoring** — Produces an overall contract risk score from 1 to 100.
- **Suggested Redlines** — Allows the system to provide proposed counter-drafting.
- **Deterministic Auditing** — Rejects findings whose cited text cannot be found in the source contract.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core implementation |
| OpenAI API | Contract analysis and structured generation |
| Pydantic | Schema validation and structured outputs |
| Pytest | Automated testing |
| python-dotenv | Environment configuration |
| GitHub | Version control and portfolio hosting |

## 🏗️ Architecture

```text
                    ┌──────────────────────┐
                    │   Contract Text      │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Legal AI Engine    │
                    │                      │
                    │ Domain Prompting     │
                    │ Structured Output    │
                    └──────────┬───────────┘
                               │
                               ▼
                ┌─────────────────────────────┐
                │ ContractAnalysisReport       │
                │                             │
                │ Contract Type              │
                │ Overall Risk Score         │
                │ Clause Findings             │
                └──────────────┬──────────────┘
                               │
                               ▼
                ┌─────────────────────────────┐
                │   Citation Verifier          │
                │                             │
                │ Exact substring verification│
                └──────────────┬──────────────┘
                               │
                     ┌─────────┴─────────┐
                     │                   │
                  Valid                Invalid
                     │                   │
                     ▼                   ▼
              Return Report       Raise Verification
                                  Error
````

## 🔄 Workflow

The Legal AI workflow is:

```text
Contract Text
     ↓
Domain-Constrained Prompt
     ↓
LLM Structured Analysis
     ↓
Pydantic Validation
     ↓
Risk Findings
     ↓
Verbatim Citation Verification
     ↓
Validated Legal Analysis Report
```

### 1. Contract Input

The system receives raw contract text as input.

### 2. Domain-Constrained Analysis

The Legal AI engine is instructed to identify liability risks and non-standard indemnities while preserving exact quotations from the contract.

### 3. Structured Output

The model returns a structured `ContractAnalysisReport` instead of unconstrained prose.

### 4. Risk Classification

Each identified finding receives one of four risk levels:

```text
LOW
MEDIUM
HIGH
CRITICAL
```

### 5. Citation Verification

Every `verbatim_quote` is checked against the original contract text.

If the exact quotation cannot be found, the system raises a citation hallucination error.

### 6. Final Report

Only grounded findings are accepted as a valid report.

## 🧩 Data Model

The system uses the following hierarchy:

```text
ContractAnalysisReport
│
├── contract_type
├── overall_risk_score
│
└── findings
      │
      ├── clause_title
      ├── risk_level
      ├── verbatim_quote
      ├── risk_explanation
      └── suggested_redline
```

### Risk Levels

| Level    | Meaning                                               |
| -------- | ----------------------------------------------------- |
| LOW      | Lower-severity contractual concern                    |
| MEDIUM   | Moderate contractual concern                          |
| HIGH     | Significant potential liability                       |
| CRITICAL | Severe contractual risk requiring immediate attention |

## 🔐 Citation Grounding

A key safety mechanism in this project is deterministic citation verification.

The verifier checks:

```python
finding.verbatim_quote.strip() in raw_text
```

If the quotation is not present in the original contract, the system raises:

```text
Citation Hallucination Detected
```

This creates an auditable link between each finding and the source contract.

## 🧪 Testing

The project includes automated tests for:

* Risk-level enumeration
* Pydantic schema construction
* Contract analysis report validation
* Valid citation grounding
* Invalid citation rejection

Run the tests with:

```bash
pytest
```

Expected result:

```text
4 passed
```

The current test suite does not require a live OpenAI API call.

## 📂 Project Structure

```text
Project-02-Legal-AI-Assistant/
│
├── data/
│   └── .gitkeep
│
├── src/
│   ├── __init__.py
│   ├── legal_ai_engine.py
│   └── citation_verifier.py
│
├── tests/
│   └── test_legal_ai.py
│
├── .env.example
├── .gitignore
├── pytest.ini
├── README.md
└── requirements.txt
```

## ⚙️ Requirements & Setup

### Requirements

* Python 3.10+
* OpenAI API key for live contract analysis
* pip
* Git

### Environment Configuration

Create a `.env` file locally:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

Do not commit the real API key to GitHub.

The repository includes `.env.example` as a configuration template.

## 📥 Setup

Clone the repository:

```bash
git clone https://github.com/SciddhantoSinha/Agentic-AI-Portfolio.git
```

Navigate to Project 02:

```bash
cd Agentic-AI-Portfolio/Project-02-Legal-AI-Assistant
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

## ▶️ How to Run

The core engine can be initialized with an OpenAI API key:

```python
from src.legal_ai_engine import LegalAIEngine

engine = LegalAIEngine(
    api_key="your_openai_api_key"
)

report = engine.analyze_contract(
    contract_text="Your contract text here"
)

print(report)
```

Before returning the report to a user, citation grounding can be performed with:

```python
from src.citation_verifier import verify_citation_grounding

verify_citation_grounding(
    report,
    contract_text
)
```

## 📊 Example Structured Output

A valid analysis follows the project schema:

```text
ContractAnalysisReport
│
├── contract_type: "Vendor Agreement"
├── overall_risk_score: 75
│
└── findings:
      └── ClauseFinding
            ├── clause_title: "Limitation of Liability"
            ├── risk_level: "HIGH"
            ├── verbatim_quote: "..."
            ├── risk_explanation: "..."
            └── suggested_redline: "..."
```

## 🎯 Use Case

The project demonstrates how structured AI systems can be applied to legal contract analysis where:

* Output format must be predictable
* Risk information must be explicitly categorized
* Source quotations must be auditable
* Hallucinated citations must be rejected
* Downstream systems require validated data

## 💡 Benefits

* Provides deterministic validation around LLM-generated legal findings
* Reduces ambiguity in model output
* Creates auditable source references
* Separates AI generation from deterministic verification
* Demonstrates domain-constrained prompt engineering
* Demonstrates Pydantic schema validation
* Provides automated tests for critical validation logic

## 🧠 Skills Demonstrated

* Domain Prompt Engineering
* Pydantic Schema Validation
* Structured LLM Outputs
* Risk Classification
* Automated Fact-Checking
* Deterministic Auditing
* Python Testing
* API Integration

## 📈 Project Progression

This project represents the **second layer** of the Agentic AI portfolio:

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

The portfolio progresses from a fixed RAG pipeline toward increasingly autonomous, multimodal, and real-time Agentic AI architectures.

## ⚠️ Important Disclaimer

This project is a technical demonstration of AI-assisted contract analysis.

It is **not a substitute for qualified legal advice or professional legal review**.

## 👨‍💻 Author

**Sciddhanto Sinha**

B.Tech – Computer Science Engineering (AI & Analytics)
