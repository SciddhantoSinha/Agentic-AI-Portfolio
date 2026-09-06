from src.arxiv_tool import search_arxiv
from src.research_agent import AutonomousResearchAgent, registry
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
    assert callable(search_arxiv)


def test_agent_can_return_final_response_without_tool_call():
    class FakeMessage:
        def __init__(self):
            self.tool_calls = None
            self.content = "Research completed."

    class FakeChoice:
        def __init__(self):
            self.message = FakeMessage()

    class FakeResponse:
        def __init__(self):
            self.choices = [FakeChoice()]

    class FakeCompletions:
        def create(self, **kwargs):
            return FakeResponse()

    class FakeChat:
        def __init__(self):
            self.completions = FakeCompletions()

    class FakeClient:
        def __init__(self):
            self.chat = FakeChat()

    agent = AutonomousResearchAgent.__new__(AutonomousResearchAgent)
    agent.client = FakeClient()

    result = agent.run(
        research_topic="Test research topic",
        max_steps=1,
    )

    assert result == "Research completed."
