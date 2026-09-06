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
    """

    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)

    def run(
        self,
        research_topic: str,
        max_steps: int = 5,
    ) -> str:

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

        for step in range(max_steps):

            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                tools=registry.definitions,
                tool_choice="auto",
            )

            msg = response.choices[0].message
            messages.append(msg)

            if not msg.tool_calls:
                return msg.content

            for tool_call in msg.tool_calls:
                fn_name = tool_call.function.name
                fn_args = json.loads(tool_call.function.arguments)

                if fn_name not in registry.tools:
                    raise ValueError(
                        f"Unknown tool requested: {fn_name}"
                    )

                tool_output = registry.tools[fn_name](**fn_args)

                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": tool_output,
                    }
                )

        return "Max iteration depth reached without complete convergence."
        
