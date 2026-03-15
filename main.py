from harness import AgentSession
import argparse

MAX_STEPS = 2

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "query",
        nargs="?",
        help="Run the agent with a query string.",
    )
    arg_input = parser.parse_args().query

    agent = AgentSession(max_steps = MAX_STEPS)

    while True:
        if arg_input is not None:
            user_input = arg_input
            arg_input = None
        else:
            user_input = input("> ").strip()

        if user_input.lower() in {"exit", "quit"}:
            break
        if not user_input:
            continue # skip empty turns

        response = agent.reply(user_input)
        print("Agent: ", response)

if __name__ == "__main__":
    main()
