import os
from tavily import TavilyClient

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

web_search_tool = {
    "type": "function",
    "name": "search_web",
    "description": "Search the web",
    "parameters": {
        "type": "object",
        "properties": {
            "sign": {
                "type": "string",
                "description": "the search query"
            },
        },
        "required": ["query"],
    },
}

# Web search tool
def search_web(query):
    tavily_client = TavilyClient(api_key=TAVILY_API_KEY)
    response = tavily_client.search(query)
    return response