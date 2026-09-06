import pytest

from src.legal_ai_engine import (
    ClauseFinding,
    ContractAnalysisReport,
    RiskLevel,
)
from src.citation_verifier import verify_citation_grounding


def test_risk_level_values():
    assert RiskLevel.LOW.value == "LOW"
    assert RiskLevel.MEDIUM.value == "MEDIUM"
    assert RiskLevel.HIGH.value == "HIGH"
    assert RiskLevel.CRITICAL.value == "CRITICAL"


def test_contract_analysis_report_schema():
    finding = ClauseFinding(
        clause_title="Limitation of Liability",
        risk_level=RiskLevel.HIGH,
        verbatim_quote="Liability shall not exceed $10,000.",
        risk_explanation="The liability cap may be restrictive.",
        suggested_redline="Increase the liability cap."
    )

    report = ContractAnalysisReport(
        contract_type="Vendor Agreement",
        overall_risk_score=75,
        findings=[finding]
    )

    assert report.contract_type == "Vendor Agreement"
    assert report.overall_risk_score == 75
    assert len(report.findings) == 1
    assert report.findings[0].risk_level == RiskLevel.HIGH


def test_valid_citation_is_grounded():
    raw_text = (
        "The parties agree that Liability shall not exceed $10,000."
    )

    finding = ClauseFinding(
        clause_title="Limitation of Liability",
        risk_level=RiskLevel.HIGH,
        verbatim_quote="Liability shall not exceed $10,000.",
        risk_explanation="The liability cap may be restrictive.",
        suggested_redline=None
    )

    report = ContractAnalysisReport(
        contract_type="Vendor Agreement",
        overall_risk_score=75,
        findings=[finding]
    )

    assert verify_citation_grounding(report, raw_text) is True


def test_invalid_citation_is_rejected():
    raw_text = "Liability shall not exceed $10,000."

    finding = ClauseFinding(
        clause_title="Limitation of Liability",
        risk_level=RiskLevel.HIGH,
        verbatim_quote="Liability shall not exceed $1,000,000.",
        risk_explanation="The quoted clause does not match.",
        suggested_redline=None
    )

    report = ContractAnalysisReport(
        contract_type="Vendor Agreement",
        overall_risk_score=75,
        findings=[finding]
    )

    with pytest.raises(ValueError, match="Citation Hallucination Detected"):
        verify_citation_grounding(report, raw_text)
