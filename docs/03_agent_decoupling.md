# 3. Agent Decoupling Guide

This document explains how to decouple the `Agent` class from the hardcoded financial toolset, enabling it to work with any set of tools provided at runtime.

## Current Implementation

The `Agent` class in `agent.py` directly imports and uses a hardcoded list of financial tools. This creates a tight coupling between the agent and the financial domain, preventing it from being used for other purposes.

```python
# agent.py
from dexter.tools import TOOLS

class Agent:
    def __init__(self, ...):
        # ...

    def ask_for_actions(self, ...):
        # ...
        return call_llm(..., tools=TOOLS)

    # ...
```

## Proposed Changes

We will modify the `Agent` class to accept a list of tools as a parameter in its constructor. This will break the hardcoded dependency and allow the agent to be initialized with any set of tools.

### Key Modifications

1.  **Update the Constructor:**
    The `__init__` method of the `Agent` class will be updated to accept a `tools` parameter. This parameter will be a list of `Tool` objects that the agent will use to perform its tasks.

2.  **Remove Hardcoded Tool Imports:**
    The direct import of `TOOLS` from `dexter.tools` will be removed from `agent.py`.

3.  **Pass Tools to `call_llm`:**
    The `ask_for_actions` method will be updated to pass the `self.tools` list to the `call_llm` function, rather than the hardcoded `TOOLS` list.

### Example

```python
# agent.py

# Remove the direct import of TOOLS
# from dexter.tools import TOOLS

class Agent:
    def __init__(self, tools: List[Tool], max_steps: int = 20, ...):
        self.tools = tools
        # ...

    def ask_for_actions(self, task_desc: str, ...):
        # ...
        try:
            # Pass the instance's tools to the LLM call
            return call_llm(prompt, system_prompt=ACTION_SYSTEM_PROMPT, tools=self.tools)
        except Exception as e:
            # ...

# main.py or cli.py

from dexter.agent import Agent
from my_custom_tools import my_tool_list

# Initialize the agent with a custom toolset
agent = Agent(tools=my_tool_list)
agent.run("Some query that uses my custom tools")
```

By making these changes, we will successfully decouple the `Agent` class from the financial toolset, transforming it into a truly generic and reusable component.