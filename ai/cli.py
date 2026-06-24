from graph.workflow_graph import app

def main():
    print("\nPrompt2Terminal Agent Ready\n")

    while True:
        goal = input(">>> ")

        if goal.lower() in ["exit", "quit"]:
            break

        result = app.invoke({"goal": goal})

        print("\n--- OUTPUT ---")

        print(result)

        print("\n--------------\n")


if __name__ == "__main__":
    main()