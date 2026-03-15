from llm import call_model
from tools import search_web
import json

MAX_STEPS = 2

def run_agent(user_input):
    context = [{
        "role": "user",
        "content": user_input
    }]
    for step in range(MAX_STEPS):
        print("context:", step, " - ", context)
        response = call_model(context)

        context += response["output"]

        if not response["tool_calls"]:
            return response["message"]

        print("calling tools")
        for tool_call in response["tool_calls"]:
            print(tool_call.arguments)

            search_query = tool_call.arguments.get("search_query")
            search_results = search_web(search_query)
            print("args:", search_query)
            context.append({
                "type": "function_call_output",
                "call_id": tool_call.call_id,
                "output": json.dumps({
                    "search_results": search_results
                })
            })
            # context.append({
            #     "role": "system",
            #     "content": "If previous search results already contain enough information to answer the user’s core question, do not call this tool again."
            # })

    return "max steps reached"
