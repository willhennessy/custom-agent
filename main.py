from harness import run_agent

def main():
    user_input = input("> ")
    response = run_agent(user_input)
    print("Agent: ", response)

if __name__ == "__main__":
    main()