from openai import OpenAI
from time import time

def call_model(messages):
    client = OpenAI()
    start = time()
    response = client.responses.create(
        model="gpt-5-mini",
        input=messages
    )
    latency = time() - start

    return {
        "message": response.output_text,
        "tool_call": None,
        "latency": latency
    }

# Questions
# why is messages plural? use case?
# when a tool call is requested, what does OpenAI put in the message? who reads the message? ex) for web search tool call is the message the search query?