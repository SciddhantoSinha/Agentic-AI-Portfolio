import hashlib
import json

from openai import OpenAI

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


class AutonomousResearchAgent:
    """
    Autonomous research agent using iterative tool calling.

    The agent:
    1. Receives a research topic.
    2. Asks the LLM what action to take.
    3. Executes requested tools.
    4. Feeds observations back to the LLM.
    5. Continues until a final answer is produced.
    6. Stops when the maximum iteration limit is reached.
    7. Detects repeated identical tool calls.
    """

    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)

    @staticmethod
    def _tool_call_hash(
        tool_name: str,
        arguments: dict,
    ) -> str:
        """
        Create a deterministic hash for a tool call and its arguments.
        """

        payload = json.dumps(
            {
                "tool": tool_name,
                "arguments": arguments,
            },
            sort_keys=True,
        )

        return hashlib.sha256(
            payload.encode("utf-8")
        ).hexdigest()

    def run(
        self,
        research_topic: str,
        max_steps: int = 5,
    ) -> str:
        """
        Run the autonomous research loop.

        Args:
            research_topic: Topic that the agent should investigate.
            max_steps: Maximum number of LLM/tool iterations.

        Returns:
            Final synthesized research response.
        """

        messages = [
            {
                "role": "system",
                "content": (
                    "You are an autonomous research scientist. "
                    "Investigate using tools, iterate on evidence, "
                    "synthesize findings, and highlight open research gaps."
                ),
            },
            {
                "role": "user",
                "content": research_topic,
            },
        ]

        previous_tool_hash = None

        for step in range(max_steps):

            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                tools=registry.definitions,
                tool_choice="auto",
            )

            msg = response.choices[0].message

            messages.append(msg)

            # If the model does not request a tool,
            # it has produced the final answer.
            if not msg.tool_calls:
                return msg.content

            for tool_call in msg.tool_calls:

                fn_name = tool_call.function.name

                fn_args = json.loads(
                    tool_call.function.arguments
                )

                # Prevent execution of unknown tools.
                if fn_name not in registry.tools:
                    raise ValueError(
                        f"Unknown tool requested: {fn_name}"
                    )

                # Generate deterministic hash for this tool call.
                current_tool_hash = self._tool_call_hash(
                    fn_name,
                    fn_args,
                )

                # Detect identical consecutive tool calls.
                if current_tool_hash == previous_tool_hash:
                    return (
                        "Agent stopped because the same tool call "
                        "was requested consecutively."
                    )

                previous_tool_hash = current_tool_hash

                # Execute the registered tool.
                tool_output = registry.tools[fn_name](
                    **fn_args
                )

                # Feed the observation back to the model.
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": tool_output,
                    }
                )

        return (
            "Max iteration depth reached without "
            "complete convergence."
        )
