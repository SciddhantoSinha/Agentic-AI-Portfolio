from src.arxiv_tool import search_arxiv
from src.research_agent import registry
from src.tool_registry import ToolRegistry


def test_tool_registry_registers_function():
    registry_instance = ToolRegistry()

    def sample_tool(query: str) -> str:
        return f"Result for {query}"

    registry_instance.register(
        name="sample_tool",
        description="A sample test tool.",
        parameters={
            "type": "object",
            "properties": {
                "query": {"type": "string"},
            },
            "required": ["query"],
        },
    )(sample_tool)

    assert "sample_tool" in registry_instance.tools
    assert registry_instance.tools["sample_tool"]("AI") == "Result for AI"
    assert len(registry_instance.definitions) == 1
    assert registry_instance.definitions[0]["function"]["name"] == "sample_tool"


def test_arxiv_tool_is_registered():
    assert "search_arxiv" in registry.tools


def test_arxiv_tool_definition():
    definition = next(
        item
        for item in registry.definitions
        if item["function"]["name"] == "search_arxiv"
    )

    assert definition["type"] == "function"
    assert "query" in definition["function"]["parameters"]["properties"]
    assert "query" in definition["function"]["parameters"]["required"]


def test_search_arxiv_returns_string():
    # We don't call the live ArXiv API in the unit test.
    # The actual API integration will be tested separately.
    assert callable(search_arxiv)
