import os
from tavily import TavilyClient

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# Web search tool
def search_web(query):
    tavily_client = TavilyClient(api_key=TAVILY_API_KEY)
    results = tavily_client.search(query)
    return results

# Calculator tool
def calculate_expression(expression: str):
    # TODO: evaluate expression
    return 0

# Tool Schemas
TOOL_SCHEMAS = [
    {
        "type": "function",
        "name": "search_web",
        "description": """
            Search the public web for current or external information.
            Use this tool only when the answer requires fresh, external, or source-backed information.
            Do not use this tool for general reasoning questions that can be answered from existing context.
            If previous search results already contain enough information to answer the user’s core question, do not call this tool again.
            Prefer one high-quality search before attempting additional searches.
        
        """,
        "parameters": {
            "type": "object",
            "properties": {
                "search_query": {
                    "type": "string",
                    "description": "the searcy query"
                },
            },
            "required": ["search_query"],
        },
    },
    {
        "type": "function",
        "name": "calculator",
        "description": "Evaluate a mathematical expression. Use this tool any time you need to compute arithmetic.",
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "Arithmetic expression such as '2 * (3 + 4)'",
                }
            }
        },
        "required": ["expression"],
    }
]
