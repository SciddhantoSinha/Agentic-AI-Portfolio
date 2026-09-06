from typing import Callable, Dict


class ToolRegistry:
    """
    Registry for dynamically dispatchable agent tools.

    Stores both:
    1. Python callables used to execute tools.
    2. OpenAI-compatible function definitions used by the LLM.
    """

    def __init__(self):
        self.tools: Dict[str, Callable] = {}
        self.definitions = []

    def register(
        self,
        name: str,
        description: str,
        parameters: dict
    ):
        """
        Register a Python function as an agent tool.
        """

        def decorator(func: Callable):
            self.tools[name] = func

            self.definitions.append(
                {
                    "type": "function",
                    "function": {
                        "name": name,
                        "description": description,
                        "parameters": parameters,
                    },
                }
            )

            return func

        return decorator
