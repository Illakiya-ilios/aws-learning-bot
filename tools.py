import os
from tavily import TavilyClient

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")


def get_tavily_client():
    """
    Lazy-load Tavily client.
    Prevents app crash if API key missing.
    """
    if not TAVILY_API_KEY:
        return None

    return TavilyClient(api_key=TAVILY_API_KEY)


def search_aws(query: str):
    """
    Safe Tavily search wrapper.
    """

    client = get_tavily_client()

    if not client:
        return {
            "success": False,
            "error": "Tavily API key not configured"
        }

    try:
        result = client.search(query=query, search_depth="advanced")
        return {
            "success": True,
            "data": result
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
