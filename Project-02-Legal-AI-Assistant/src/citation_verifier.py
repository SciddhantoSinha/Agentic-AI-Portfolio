from .legal_ai_engine import ContractAnalysisReport


def verify_citation_grounding(
    report: ContractAnalysisReport,
    raw_text: str
) -> bool:
    """
    Verify that every quoted contract passage exists
    exactly within the original contract text.
    """

    for finding in report.findings:
        quote = finding.verbatim_quote.strip()

        if quote not in raw_text:
            raise ValueError(
                f"Citation Hallucination Detected: {quote}"
            )

    return True
