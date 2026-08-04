from brain.search.models.search_query import SearchQuery


def test_search_query_defaults():

    query = SearchQuery("Hello")

    assert query.text == "Hello"
    assert query.top_k == 5
    assert query.min_score == 0.0