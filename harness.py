from time import sleep
from llm import call_model

MAX_STEPS = 5

def run_agent(user_input):
    context = [{
        "role": "user",
        "content": user_input
    }]
    for step in range(MAX_STEPS):
        response = call_model(context)
        sleep(1)

        search_web("what is one news story from today?")

        if response["tool_call"]:
            print("calling tools")
            # TODO: implement tool calls
            # search_web("query")
            # TODO: append tool result to context
        else:
            return response["message"]

    return "max steps reached"