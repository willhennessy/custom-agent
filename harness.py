from llm import call_model
from tools import search_web, calculate_expression, get_current_time
import json

SYSTEM_PROMPT = """
You are a helpful AI assistant. Your job is to answer user input questions with pragmatic, warm, and
helpful responses.
You may use the web search tool when needed, but prefer at most one search.
If search results already answer the user's question, do not call the tool again; provide the final
answer.
"""

class AgentSession:
    def __init__(self, max_steps: int = 2):
        self.max_steps = max_steps
        self.messages = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]

    def reply(self, user_input: str) -> str:
        # 1) add user turn to session memory
        self.messages.append({"role": "user", "content": user_input})

        # 2) run one agent turn with tool calls where requested
        for step in range(self.max_steps):
            response = call_model(self.messages)

            # no tool call requested -> return final response
            if not response["tool_calls"]:
                assistant_text = response["output_text"]
                self.messages.append({"role": "assistant", "content": assistant_text})
                return assistant_text

            # tool calls requested -> append model output and tool output
            self.messages += response["output"]
            for tool_call in response["tool_calls"]:
                if tool_call.name == "search_web":
                    search_query = tool_call.arguments.get("search_query")
                    search_results = search_web(search_query)
                    self.messages.append({
                        "type": "function_call_output",
                        "call_id": tool_call.call_id,
                        "output": json.dumps(search_results)
                    })
                elif tool_call.name == "calculate_expression":
                    expression = tool_call.arguments.get("expression")
                    result = calculate_expression(expression)
                    self.messages.append({
                        "type": "function_call_output",
                        "call_id": tool_call.call_id,
                        "output": json.dumps(result)
                    })
                elif tool_call.name == "get_current_time":
                    self.messages.append({
                        "type": "function_call_output",
                        "call_id": tool_call.call_id,
                        "output": get_current_time()
                    })

        # TODO: when max steps reached, summarize what we found
        fallback = "max steps reached"
        self.messages.append({"role": "assistant", "content": fallback})
        return fallback
