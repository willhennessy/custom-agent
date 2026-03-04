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

        if response["tool_call"]:
            print("calling tools")
        else:
            # TODO: implement tool calls
            # TODO: append tool result to context
            return response["message"]

    return "max steps reached"