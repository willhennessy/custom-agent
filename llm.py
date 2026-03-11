from openai import OpenAI
from time import time
from tools import web_search_tool

def call_model(messages):
    client = OpenAI()
    start = time()
    response = client.responses.create(
        model="gpt-5-mini",
        tools=[
            web_search_tool
        ],
        input=messages
    )
    latency = time() - start

    tool_calls = []
    for item in response.output:
        if item.type == "function_call":
            tool_calls.append(item)

    return {
        "output": response.output,
        "message": response.output_text,
        "tool_call": tool_calls,
        "latency": latency
    }
