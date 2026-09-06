from enum import Enum
from typing import List, Optional

from openai import OpenAI
from pydantic import BaseModel, Field


class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class ClauseFinding(BaseModel):
    clause_title: str = Field(
        description="Name of clause, e.g. Limitation of Liability"
    )
    risk_level: RiskLevel = Field(
        description="Evaluated risk severity"
    )
    verbatim_quote: str = Field(
        description="Exact quote from contract text"
    )
    risk_explanation: str = Field(
        description="Explanation of potential liability"
    )
    suggested_redline: Optional[str] = Field(
        default=None,
        description="Proposed counter-drafting"
    )


class ContractAnalysisReport(BaseModel):
    contract_type: str
    overall_risk_score: int = Field(
        description="Score from 1 to 100"
    )
    findings: List[ClauseFinding]


class LegalAIEngine:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)

    def analyze_contract(
        self,
        contract_text: str
    ) -> ContractAnalysisReport:

        system_prompt = """
You are an elite enterprise legal counsel.

Analyze the contract text.

Identify all liability risks and non-standard indemnities.

You MUST extract exact verbatim quotes for every finding.
Do NOT paraphrase the quoted contract language.
"""

        completion = self.client.beta.chat.completions.parse(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": (
                        "Analyze this contract:\n\n"
                        f"{contract_text}"
                    )
                }
            ],
            response_format=ContractAnalysisReport,
            temperature=0.0
        )

        return completion.choices[0].message.parsed
