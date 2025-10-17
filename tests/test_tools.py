from dexter.tools import search_web

def test_search_web():
    """
    Tests that the search_web tool returns the expected string.
    """
    query = "test query"
    result = search_web.run(query)
    assert result == f"Search results for: {query}"