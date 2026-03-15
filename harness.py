from llm import call_model
from tools import search_web
import json

MAX_STEPS = 2

def run_agent(user_input):
    messages = [
        {
            "role": "system",
            "content":  """
                You may use the web search tool when needed, but prefer at most one search.
                If search results already answer the user's question, do not call the tool again; provide the final answer.
            """
        },
        {
        "role": "user",
        "content": user_input
        }
    ]
    for step in range(MAX_STEPS):
        print("messages:", step, " - ", messages)
        response = call_model(messages)

        if not response["tool_calls"]:
            return response["message"]

        messages += response["output"]
        print("calling tools")
        for tool_call in response["tool_calls"]:
            print(tool_call.arguments)

            search_query = tool_call.arguments.get("search_query")
            search_results = search_web(search_query)
            messages.append({
                "type": "function_call_output",
                "call_id": tool_call.call_id,
                "output": json.dumps(search_results)
            })

    return "max steps reached"
