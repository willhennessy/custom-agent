from openai import OpenAI
from openai.types.responses.response_output_item import ResponseOutputItem
from time import time
from tools import TOOL_SCHEMAS
import json
from dataclasses import dataclass
from typing import Any

@dataclass
class ToolCall:
    call_id: str
    name: str
    arguments: dict[str, Any]

# Extract tool calls from the model response and normalize them with arguments parsed into dicts.
def extract_tool_calls(output_items: list[ResponseOutputItem]) -> list[ToolCall]:
    tool_calls: list[ToolCall] = []
    for item in output_items:
        if item.type == "function_call":
            arguments = json.loads(item.arguments)
            tool_calls.append(
                ToolCall(
                    call_id=item.call_id,
                    name=item.name,
                    arguments=arguments,
                )
            )
    return tool_calls

def call_model(messages):
    client = OpenAI()
    start = time()
    response = client.responses.create(
        model="gpt-5-mini",
        tools=TOOL_SCHEMAS,
        input=messages
    )
    latency = time() - start

    tool_calls = extract_tool_calls(response.output)

    return {
        "output": response.output,
        "output_text": response.output_text,
        "tool_calls": tool_calls,
        "latency": latency
    }
