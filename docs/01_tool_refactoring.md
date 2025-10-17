# 1. Tool Refactoring Guide

This document outlines the plan for refactoring the `tools` directory to create a more generic, domain-agnostic agent. The goal is to move from a hardcoded set of financial tools to a flexible, pluggable architecture.

## Current Architecture

The `tools` directory currently contains a set of highly specialized financial tools. These tools are hardcoded into the `Agent` class, making it difficult to adapt the agent for other use cases.

## Proposed Architecture

We will introduce a pluggable tool system that allows tools to be passed to the `Agent` at runtime. This will decouple the agent from any specific domain and allow it to be configured with different toolsets for different tasks.

### Key Changes

1.  **Create a Generic Tool Protocol:**
    We will define a `Tool` protocol (or base class) that all tools must adhere to. This will ensure that the agent can interact with any tool in a consistent way. The protocol should define:
    *   `name`: A unique name for the tool.
    *   `description`: A clear description of the tool's purpose and functionality.
    *   `run()`: The method that executes the tool's logic.

2.  **Refactor Existing Tools:**
    The existing financial tools will be refactored to conform to the new `Tool` protocol. This will involve updating their class definitions and ensuring they implement all the required methods.

3.  **Create a Tool Loader:**
    We will create a `ToolLoader` class responsible for discovering and loading tools from a specified directory. This will allow us to add new tools to the agent without modifying the core codebase.

4.  **Update the Agent Class:**
    The `Agent` class will be modified to accept a list of tools as a parameter in its constructor. The agent will then use this list of tools to perform its tasks, rather than relying on a hardcoded list.

### Example

```python
# Before
class Agent:
    def __init__(self):
        self.tools = [GetIncomeStatements(), GetBalanceSheets()]

# After
class Agent:
    def __init__(self, tools: List[Tool]):
        self.tools = tools

# Usage
financial_tools = ToolLoader.load_tools("financial_tools")
agent = Agent(tools=financial_tools)
```

By implementing these changes, we will create a more flexible and extensible agent that can be easily adapted to a wide range of tasks and domains.