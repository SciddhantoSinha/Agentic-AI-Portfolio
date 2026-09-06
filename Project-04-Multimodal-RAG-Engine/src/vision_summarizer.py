from openai import OpenAI


class VisionSummarizer:
    """
    Generates searchable textual summaries of visual
    document elements using a vision-capable LLM.
    """

    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)

    def summarize(
        self,
        image_bytes: bytes,
        element_type: str = "chart",
    ) -> str:
        """
        Analyze a visual element and generate a
        retrieval-friendly textual summary.

        Args:
            image_bytes: Raw image bytes.
            element_type: Type of visual element,
                such as chart, table, or diagram.

        Returns:
            Textual summary of the visual element.
        """

        import base64

        b64_image = base64.b64encode(
            image_bytes
        ).decode("utf-8")

        prompt = (
            f"Analyze this {element_type}. "
            "Describe all important data points, "
            "trends, labels, relationships, columns, "
            "values, and structural information. "
            "Preserve important quantitative details "
            "so this description can be used for "
            "semantic retrieval."
        )

        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt,
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": (
                                    "data:image/png;base64,"
                                    f"{b64_image}"
                                ),
                            },
                        },
                    ],
                },
            ],
            max_tokens=500,
        )

        return response.choices[0].message.content
