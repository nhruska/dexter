from langchain.tools import tool

@tool
def search_web(query: str) -> str:
    """Searches the web for the given query."""
    # This is a placeholder. A real implementation would use a search API.
    return f"Search results for: {query}"

DEFAULT_TOOLS = [search_web]