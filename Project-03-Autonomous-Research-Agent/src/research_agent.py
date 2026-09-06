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
    Autonomous research agent using an iterative ReAct-style loop.

    The agent can:
    - decide when to use a research tool,
    - execute registered tools,
    - feed observations back into the conversation,
    - reflect when repeated searches produce no useful evidence,
    - stop after a maximum number of iterations,
    - detect repeated identical tool calls.
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

    @staticmethod
    def _is_zero_yield_observation(
        tool_output: str,
    ) -> bool:
        """
        Determine whether a tool returned no useful research evidence.
        """

        normalized = tool_output.strip().lower()

        zero_yield_markers = {
            "",
            "no papers found.",
            "no papers found",
        }

        return normalized in zero_yield_markers

    @staticmethod
    def _reflection_message() -> str:
        """
        Generate a strategy-pivot instruction after repeated
        zero-yield observations.
        """

        return (
            "SCRATCHPAD REFLECTION: The previous research attempts "
            "did not produce useful evidence. Re-evaluate the current "
            "research strategy. Identify what information is missing, "
            "broaden or reformulate the search semantics, and avoid "
            "repeating the same unsuccessful query. If appropriate, "
            "search using related terminology, alternative concepts, "
            "or a narrower methodological angle."
        )

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
        zero_yield_observations = 0

        for step in range(max_steps):

            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                tools=registry.definitions,
                tool_choice="auto",
            )

            msg = response.choices[0].message

            messages.append(msg)

            # The model has produced a final answer.
            if not msg.tool_calls:
                return msg.content

            for tool_call in msg.tool_calls:

                fn_name = tool_call.function.name

                fn_args = json.loads(
                    tool_call.function.arguments
                )

                # Reject tools that are not registered.
                if fn_name not in registry.tools:
                    raise ValueError(
                        f"Unknown tool requested: {fn_name}"
                    )

                # Generate deterministic hash for this tool call.
                current_tool_hash = self._tool_call_hash(
                    fn_name,
                    fn_args,
                )

                # Prevent identical consecutive tool calls.
                if current_tool_hash == previous_tool_hash:
                    return (
                        "Agent stopped because the same tool call "
                        "was requested consecutively."
                    )

                previous_tool_hash = current_tool_hash

                # Execute the tool.
                tool_output = registry.tools[fn_name](
                    **fn_args
                )

                # Track whether the observation produced evidence.
                if self._is_zero_yield_observation(tool_output):
                    zero_yield_observations += 1
                else:
                    zero_yield_observations = 0

                # Add the tool observation to the conversation.
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": tool_output,
                    }
                )

                # After two consecutive zero-yield observations,
                # force the agent to reflect and change strategy.
                if zero_yield_observations >= 2:
                    messages.append(
                        {
                            "role": "system",
                            "content": self._reflection_message(),
                        }
                    )

                    zero_yield_observations = 0

        return (
            "Max iteration depth reached without "
            "complete convergence."
        )
