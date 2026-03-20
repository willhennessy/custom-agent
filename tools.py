import os
import ast
from tavily import TavilyClient
from datetime import datetime

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

ALLOWED_BINARY_OPS = {
    ast.Add: lambda a, b: a + b,
    ast.Sub: lambda a, b: a - b,
    ast.Mult: lambda a, b: a * b,
    ast.Div: lambda a, b: a / b,
    ast.FloorDiv: lambda a, b: a // b,
    ast.Mod: lambda a, b: a % b,
    ast.Pow: lambda a, b: a ** b,
}

ALLOWED_UNARY_OPS = {
    ast.UAdd: lambda a: +a,
    ast.USub: lambda a: -a,
}

def _eval(node):
    if isinstance(node, ast.Expression):
        return _eval(node.body)

    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value

    if isinstance(node, ast.BinOp):
        op_type = type(node.op)
        if op_type not in ALLOWED_BINARY_OPS:
            raise ValueError(f"Unsupported operator: {op_type.__name__}")
        return ALLOWED_BINARY_OPS[op_type](_eval(node.left), _eval(node.right))

    if isinstance(node, ast.UnaryOp):
        op_type = type(node.op)
        if op_type not in ALLOWED_UNARY_OPS:
            raise ValueError(f"Unsupported operator: {op_type.__name__}")
        return ALLOWED_UNARY_OPS[op_type](_eval(node.operand))

    raise ValueError(f"Unsupported expression: {type(node).__name__}")

# Web search tool
def search_web(query):
    tavily_client = TavilyClient(api_key=TAVILY_API_KEY)
    results = tavily_client.search(query)
    return results

# Calculator tool: safely evaluate an arithmetic expression
def calculate_expression(expression: str):
    try:
        parsed = ast.parse(expression, mode="eval")
        print(parsed)
        return _eval(parsed)
    except SyntaxError as e:
        raise ValueError("Invalid expression syntax") from e

def get_current_time() -> str:
    return datetime.now().isoformat()

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
        "name": "calculate_expression",
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
    },
    {
        "type": "function",
        "name": "get_current_time",
        "description": "Get the current time in the user's local timezone.",
        "parameters": {},
        "required": [],
    }
]
