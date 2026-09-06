from src.router import Route, SemanticRouter


def test_current_query_routes_to_live():
    router = SemanticRouter()

    result = router.route(
        "What is the current stock price?"
    )

    assert result == Route.LIVE


def test_latest_news_routes_to_live():
    router = SemanticRouter()

    result = router.route(
        "What is the latest news about AI?"
    )

    assert result == Route.LIVE


def test_internal_knowledge_query_routes_internal():
    router = SemanticRouter()

    result = router.route(
        "Explain our internal deployment policy."
    )

    assert result == Route.INTERNAL


def test_empty_query_raises_error():
    router = SemanticRouter()

    try:
        router.route("")
        assert False
    except ValueError:
        assert True
