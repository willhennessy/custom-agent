from llm import call_model
from tools import search_web
import json

MAX_STEPS = 5

def run_agent(user_input):
    context = [{
        "role": "user",
        "content": user_input
    }]
    for step in range(MAX_STEPS):
        response = call_model(context)

        context += response["output"]

        if not response["tool_call"]:
            return response["message"]

        print("calling tools")
        for tool_call in response["tool_call"]:
            print("TYPE:", tool_call.type)
            print(tool_call)
            search_results = search_web("query")
            context.append({
                "type": "function_call_output",
                "call_id": tool_call.call_id,
                "output": json.dumps({
                    "search_results": search_results
                })
            })
            print("appended", tool_call.call_id)

    return "max steps reached"