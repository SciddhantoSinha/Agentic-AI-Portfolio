import pytest

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
                "query": {
                    "type": "string",
                },
            },
            "required": ["query"],
        },
    )(sample_tool)

    assert "sample_tool" in registry_instance.tools

    assert (
        registry_instance.tools["sample_tool"]("AI")
        == "Result for AI"
    )

    assert len(registry_instance.definitions) == 1

    assert (
        registry_instance.definitions[0]["function"]["name"]
        == "sample_tool"
    )


def test_arxiv_tool_is_registered():
    assert "search_arxiv" in registry.tools


def test_arxiv_tool_definition():
    definition = next(
        item
        for item in registry.definitions
        if item["function"]["name"] == "search_arxiv"
    )

    assert definition["type"] == "function"

    assert (
        "query"
        in definition["function"]["parameters"]["properties"]
    )

    assert (
        "query"
        in definition["function"]["parameters"]["required"]
    )


def test_search_arxiv_returns_callable():
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

    agent = AutonomousResearchAgent.__new__(
        AutonomousResearchAgent
    )

    agent.client = FakeClient()

    result = agent.run(
        research_topic="Test research topic",
        max_steps=1,
    )

    assert result == "Research completed."


def test_tool_call_hash_is_deterministic():

    hash_one = AutonomousResearchAgent._tool_call_hash(
        "search_arxiv",
        {
            "query": "retrieval augmented generation",
            "max_results": 3,
        },
    )

    hash_two = AutonomousResearchAgent._tool_call_hash(
        "search_arxiv",
        {
            "max_results": 3,
            "query": "retrieval augmented generation",
        },
    )

    assert hash_one == hash_two


def test_tool_call_hash_changes_when_arguments_change():

    hash_one = AutonomousResearchAgent._tool_call_hash(
        "search_arxiv",
        {
            "query": "retrieval augmented generation",
            "max_results": 3,
        },
    )

    hash_two = AutonomousResearchAgent._tool_call_hash(
        "search_arxiv",
        {
            "query": "retrieval augmented generation",
            "max_results": 5,
        },
    )

    assert hash_one != hash_two


def test_unknown_tool_is_rejected():

    class FakeToolCallFunction:
        name = "unknown_tool"
        arguments = "{}"

    class FakeToolCall:
        id = "test-tool-call"
        function = FakeToolCallFunction()

    class FakeMessage:
        def __init__(self):
            self.tool_calls = [FakeToolCall()]
            self.content = None

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

    agent = AutonomousResearchAgent.__new__(
        AutonomousResearchAgent
    )

    agent.client = FakeClient()

    with pytest.raises(
        ValueError,
        match="Unknown tool requested",
    ):
        agent.run(
            research_topic="Test research topic",
            max_steps=1,
        )


def test_zero_yield_observation_is_detected():
    assert (
        AutonomousResearchAgent._is_zero_yield_observation(
            "No papers found."
        )
        is True
    )

    assert (
        AutonomousResearchAgent._is_zero_yield_observation(
            "No papers found"
        )
        is True
    )

    assert (
        AutonomousResearchAgent._is_zero_yield_observation("")
        is True
    )


def test_non_empty_observation_is_not_zero_yield():
    observation = (
        "Title: Retrieval Augmented Generation\n"
        "Abstract: A research paper about RAG."
    )

    assert (
        AutonomousResearchAgent._is_zero_yield_observation(
            observation
        )
        is False
    )


def test_reflection_message_contains_strategy_change():
    message = AutonomousResearchAgent._reflection_message()

    assert "SCRATCHPAD REFLECTION" in message
    assert "Re-evaluate" in message
    assert "avoid" in message
    assert "unsuccessful query" in message
