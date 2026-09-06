from src.vision_summarizer import VisionSummarizer


def test_vision_summarizer_initializes():

    summarizer = VisionSummarizer.__new__(
        VisionSummarizer
    )

    summarizer.client = None

    assert summarizer.client is None


def test_summarize_sends_image_to_vision_model():

    class FakeMessage:
        content = (
            "A chart showing increasing revenue "
            "from Q1 to Q4."
        )

    class FakeChoice:
        message = FakeMessage()

    class FakeResponse:
        choices = [FakeChoice()]

    class FakeCompletions:

        def __init__(self):
            self.called = False
            self.kwargs = None

        def create(self, **kwargs):
            self.called = True
            self.kwargs = kwargs
            return FakeResponse()

    class FakeChat:

        def __init__(self):
            self.completions = FakeCompletions()

    class FakeClient:

        def __init__(self):
            self.chat = FakeChat()

    summarizer = VisionSummarizer.__new__(
        VisionSummarizer
    )

    summarizer.client = FakeClient()

    result = summarizer.summarize(
        image_bytes=b"test-image-data",
        element_type="chart",
    )

    assert (
        result
        == "A chart showing increasing revenue "
        "from Q1 to Q4."
    )

    assert (
        summarizer.client.chat.completions.called
        is True
    )

    request = (
        summarizer.client
        .chat
        .completions
        .kwargs
    )

    assert request["model"] == "gpt-4o"

    assert request["max_tokens"] == 500

    message_content = request["messages"][0]["content"]

    assert message_content[0]["type"] == "text"

    assert "chart" in (
        message_content[0]["text"].lower()
    )

    assert message_content[1]["type"] == "image_url"

    assert (
        message_content[1]["image_url"]["url"]
        .startswith("data:image/png;base64,")
    )


def test_summarize_supports_different_visual_types():

    class FakeMessage:
        content = "A financial table."

    class FakeChoice:
        message = FakeMessage()

    class FakeResponse:
        choices = [FakeChoice()]

    class FakeCompletions:

        def create(self, **kwargs):
            return FakeResponse()

    class FakeChat:

        def __init__(self):
            self.completions = FakeCompletions()

    class FakeClient:

        def __init__(self):
            self.chat = FakeChat()

    summarizer = VisionSummarizer.__new__(
        VisionSummarizer
    )

    summarizer.client = FakeClient()

    result = summarizer.summarize(
        image_bytes=b"table-data",
        element_type="table",
    )

    assert result == "A financial table."
