# Autonomous Research Agent

This project provides a powerful and flexible autonomous agent that can be configured to perform a wide range of research tasks. By providing a custom set of tools, you can adapt the agent to any domain, from scientific research to data analysis.

## Overview

This agent takes complex questions and turns them into clear, step-by-step research plans. It runs those tasks using a customizable toolset, checks its own work, and refines the results until it has a confident, data-backed answer.

**Key Capabilities:**
- **Intelligent Task Planning**: Automatically decomposes complex queries into structured research steps.
- **Pluggable Tool Architecture**: Easily extend the agent's capabilities by adding new tools.
- **Autonomous Execution**: Selects and executes the right tools to gather and process information.
- **Self-Validation**: Checks its own work and iterates until tasks are complete.
- **Safety Features**: Built-in loop detection and step limits to prevent runaway execution.

## Quick Start

### Prerequisites

- Python 3.10 or higher
- [uv](https://github.com/astral-sh/uv) package manager
- OpenAI API key

### Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/your-username/your-repo.git
    cd your-repo
    ```

2.  Install dependencies with uv:
    ```bash
    uv sync
    ```

3.  Set up your environment variables:
    ```bash
    # Copy the example environment file
    cp env.example .env

    # Edit .env and add your API key
    # OPENAI_API_KEY=your-openai-api-key
    ```

### Usage

To run the agent, you'll need to create a toolset and pass it to the `Agent` class.

**1. Create a Toolset**

Create a file named `my_tools.py` and define a list of tools:

```python
# my_tools.py
from langchain.tools import tool

@tool
def search_web(query: str) -> str:
    """Searches the web for the given query."""
    # Your web search implementation here
    return f"Search results for: {query}"

my_tool_list = [search_web]
```

**2. Run the Agent**

Now, create a script to run the agent with your custom toolset:

```python
# run_agent.py
from dexter.agent import Agent
from my_tools import my_tool_list

# Initialize the agent with your toolset
agent = Agent(tools=my_tool_list)

# Run the agent with a query
query = "What are the latest advancements in AI?"
result = agent.run(query)

print(result)
```

## How to Contribute

1.  Fork the repository
2.  Create a feature branch
3.  Commit your changes
4.  Push to the branch
5.  Create a Pull Request