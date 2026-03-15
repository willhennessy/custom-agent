from harness import run_agent
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "query",
        nargs="?",
        help="Run the agent with a query string.",
    )
    args = parser.parse_args()

    user_input = args.query if args.query else input("> ")

    response = run_agent(user_input)
    print("Agent: ", response)

if __name__ == "__main__":
    main()
