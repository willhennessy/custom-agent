from time import sleep
from llm import call_model

MAX_STEPS = 3

def run_agent(user_input):
    for step in range(MAX_STEPS):
        response = call_model(user_input)
        if response["tool_call"]:
            print("calling tools")
        else:
            print("Agent: ", response["message"])
        sleep(1)

    return "max steps reached"