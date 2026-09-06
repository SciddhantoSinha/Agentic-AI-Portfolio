from .arxiv_tool import search_arxiv
from .tool_registry import ToolRegistry


registry = ToolRegistry()


registry.register(
    name="search_arxiv",
    description="Searches ArXiv for relevant research papers given a query.",
    parameters={
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The scientific search terms",
            },
            "max_results": {
                "type": "integer",
                "default": 3,
            },
        },
        "required": ["query"],
    },
)(search_arxiv)
