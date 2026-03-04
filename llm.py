from time import time

def call_model(messages):
    start = time()
    # TODO: implement Model API call
    latency = time() - start
    return {
        "message": "test",
        "tool_call": None,
        "latency": latency
    }

# Questions
# why is messages plural? use case?
# when a tool call is requested, what does OpenAI put in the message? who reads the message? ex) for web search tool call is the message the search query?