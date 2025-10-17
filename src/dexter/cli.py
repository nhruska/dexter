from dotenv import load_dotenv

# Load environment variables BEFORE importing any dexter modules
load_dotenv()

from dexter.agent import Agent
from dexter.tools import DEFAULT_TOOLS
from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory

def main():
    agent = Agent(tools=DEFAULT_TOOLS)

    # Create a prompt session with history support
    session = PromptSession(history=InMemoryHistory())

    while True:
        try:
            query = session.prompt(">> ")
            if query.lower() in ["exit", "quit"]:
                break
            if query:
                agent.run(query)
        except (KeyboardInterrupt, EOFError):
            break


if __name__ == "__main__":
    main()
