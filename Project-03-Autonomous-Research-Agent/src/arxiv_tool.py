import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET


def search_arxiv(query: str, max_results: int = 3) -> str:
    """
    Search ArXiv for research papers matching a scientific query.

    Args:
        query: Scientific search terms.
        max_results: Maximum number of papers to return.

    Returns:
        A formatted string containing paper titles and abstracts.
    """

    url = (
        "http://export.arxiv.org/api/query"
        f"?search_query=all:{urllib.parse.quote(query)}"
        f"&start=0&max_results={max_results}"
    )

    with urllib.request.urlopen(url) as response:
        xml_data = response.read()

    root = ET.fromstring(xml_data)

    namespace = {
        "atom": "http://www.w3.org/2005/Atom"
    }

    results = []

    for entry in root.findall("atom:entry", namespace):
        title_element = entry.find("atom:title", namespace)
        summary_element = entry.find("atom:summary", namespace)

        title = (
            title_element.text.strip().replace("\n", " ")
            if title_element is not None and title_element.text
            else "Unknown Title"
        )

        summary = (
            summary_element.text.strip().replace("\n", " ")
            if summary_element is not None and summary_element.text
            else "No abstract available."
        )

        results.append(
            f"Title: {title}\n"
            f"Abstract: {summary}\n"
        )

    return "\n---\n".join(results) if results else "No papers found."
