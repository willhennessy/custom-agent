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

    return {
        "message": response.output_text,
        "tool_call": None,
        "latency": latency
    }
