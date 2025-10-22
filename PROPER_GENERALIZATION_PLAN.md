# Proper Generalization Plan for Dexter

**Goal:** Transform Dexter into a generic autonomous agent framework that can be customized for multiple verticals (finance, legal, medical, etc.) while preserving the valuable financial implementation as a reference.

**Date:** 2025-10-22
**Analyzed By:** Claude
**Context:** PR #1 has the right goal (generalization) but the wrong approach (would lose 500+ lines of valuable financial code)

---

## The Vision: Multi-Vertical Agent Platform

### What We Want to Build

```
dexter-core/                    # Generic agent framework
├── Planning agent
├── Action agent
├── Validation agent
├── Answer agent
└── Tool plugin system

dexter-finance/                 # Financial vertical (KEEP THIS!)
├── SEC filings tools
├── Financial statements API
├── Company research tools
└── Financial domain prompts

dexter-legal/                   # Future: Legal vertical
├── Case law search
├── Document analysis
└── Legal domain prompts

dexter-medical/                 # Future: Medical vertical
├── Research paper search
├── Clinical trial data
└── Medical domain prompts
```

**Key Insight:** The financial tools are not garbage to throw away - they're **THE REFERENCE IMPLEMENTATION** for how to build a vertical.

---

## Why PR #1's Approach is Wrong

### Problem #1: Proposes REMOVING Instead of ABSTRACTING

**Bad Approach (PR #1):**
```python
# Remove financial tools entirely
# Make user provide tools manually every time
agent = Agent(tools=user_must_provide_these)
```

**Good Approach:**
```python
# Keep financial tools as default vertical
from dexter.verticals.finance import FINANCIAL_TOOLS, FINANCIAL_PROMPTS

agent = Agent(
    vertical="finance",  # Uses built-in financial vertical
    # OR
    tools=custom_tools,
    prompts=custom_prompts
)
```

### Problem #2: Documentation-Only Change

PR #1 adds 271 lines of documentation but **doesn't actually refactor anything**. This creates:
- Technical debt (docs don't match code)
- No working implementation
- Confusion about what to do next

### Problem #3: Would Lose Domain Expertise

**Current financial code has value:**
- 203 lines of SEC filings logic (`filings.py`)
- 150 lines of financial statements (`financials.py`)
- 103 lines of financial constants (`constants.py`)
- Retry logic, API integration, error handling
- **Total: ~500 lines of working, tested code**

**PR #1 proposes:** Strip it all out, make generic

**Better approach:** Preserve it as `dexter.verticals.finance`

### Problem #4: Wrong Abstraction Level

PR #1 wants to make prompts "domain-agnostic":

```python
# PR #1 proposes:
"You are an autonomous agent"  # Too vague!

# Better:
"You are {vertical_name}, an autonomous {vertical_domain} agent"
# Filled in by vertical config
```

**Why this matters:** LLMs perform better with specific context. Generic prompts = worse results.

---

## Proper Generalization Architecture

### Phase 1: Preserve Financial Implementation

**Goal:** Don't lose any code, just reorganize it.

```
src/dexter/
├── core/
│   ├── agent.py           # Generic agent logic
│   ├── model.py           # LLM interface
│   ├── schemas.py         # Base schemas
│   └── prompts.py         # Prompt templates (with {variables})
│
├── verticals/
│   ├── __init__.py
│   ├── base.py           # VerticalConfig base class
│   │
│   └── finance/          # Move existing code HERE
│       ├── __init__.py
│       ├── tools/
│       │   ├── filings.py      # KEEP (203 lines)
│       │   ├── financials.py   # KEEP (150 lines)
│       │   ├── constants.py    # KEEP (103 lines)
│       │   └── api.py          # KEEP
│       ├── prompts.py          # Financial prompt config
│       └── config.py           # FinanceVerticalConfig
│
└── cli.py                # Entry point
```

**Key Point:** All 500+ lines of financial code are **preserved and enhanced**, not deleted.

### Phase 2: Define Vertical Interface

Create a standard interface that all verticals implement:

```python
# src/dexter/verticals/base.py

from abc import ABC, abstractmethod
from typing import List
from langchain.tools import BaseTool

class VerticalConfig(ABC):
    """Base class for domain-specific configurations"""

    @property
    @abstractmethod
    def name(self) -> str:
        """Display name: 'Dexter Financial Research Agent'"""
        pass

    @property
    @abstractmethod
    def domain(self) -> str:
        """Domain: 'financial research', 'legal research', etc."""
        pass

    @property
    @abstractmethod
    def tools(self) -> List[BaseTool]:
        """Domain-specific tools"""
        pass

    @property
    @abstractmethod
    def prompt_variables(self) -> dict:
        """Variables to inject into prompt templates"""
        pass

    @property
    def example_queries(self) -> List[str]:
        """Example queries for this vertical"""
        return []

    @property
    def required_env_vars(self) -> List[str]:
        """Required environment variables"""
        return ["OPENAI_API_KEY"]
```

### Phase 3: Implement Financial Vertical

**This is where all the current code goes:**

```python
# src/dexter/verticals/finance/config.py

from dexter.verticals.base import VerticalConfig
from dexter.verticals.finance.tools import FINANCIAL_TOOLS

class FinancialVerticalConfig(VerticalConfig):
    @property
    def name(self) -> str:
        return "Dexter"

    @property
    def domain(self) -> str:
        return "financial research"

    @property
    def tools(self) -> List[BaseTool]:
        # All the existing financial tools!
        return FINANCIAL_TOOLS

    @property
    def prompt_variables(self) -> dict:
        return {
            "agent_name": "Dexter",
            "agent_role": "autonomous financial research agent",
            "domain": "financial research",
            "task_type": "financial research query",
            "example_tasks": """
            - Analyze revenue trends
            - Compare financial metrics
            - Review SEC filings
            """,
        }

    @property
    def example_queries(self) -> List[str]:
        return [
            "What was Apple's revenue growth over the last 4 quarters?",
            "Compare Microsoft and Google's operating margins for 2023",
            "Analyze Tesla's cash flow trends over the past year",
        ]

    @property
    def required_env_vars(self) -> List[str]:
        return ["OPENAI_API_KEY", "FINANCIAL_DATASETS_API_KEY"]
```

**Result:** All existing financial logic is preserved, just better organized.

### Phase 4: Generic Agent Core

```python
# src/dexter/core/agent.py

from dexter.verticals.base import VerticalConfig
from dexter.core.prompts import PLANNING_PROMPT_TEMPLATE

class Agent:
    def __init__(
        self,
        vertical: VerticalConfig,
        max_steps: int = 20,
        max_steps_per_task: int = 5
    ):
        self.vertical = vertical
        self.tools = vertical.tools
        self.max_steps = max_steps
        self.max_steps_per_task = max_steps_per_task

    def plan_tasks(self, query: str) -> List[Task]:
        tool_descriptions = "\n".join([
            f"- {t.name}: {t.description}" for t in self.tools
        ])

        # Use template with vertical-specific variables
        system_prompt = PLANNING_PROMPT_TEMPLATE.format(
            agent_name=self.vertical.name,
            agent_role=self.vertical.prompt_variables["agent_role"],
            domain=self.vertical.domain,
            tools=tool_descriptions
        )

        # Rest of planning logic...
```

### Phase 5: Prompt Templates (Not Generic Prompts!)

**PR #1 is wrong about this:** Don't make prompts generic, make them **templated**.

```python
# src/dexter/core/prompts.py

PLANNING_PROMPT_TEMPLATE = """
You are the planning component for {agent_name}, {agent_role}.

Your responsibility is to analyze a user's {domain} query and break it down
into a clear, logical sequence of actionable tasks.

You have access to these tools:
{tools}

Examples of {domain} tasks:
{example_tasks}

Focus on creating tasks that can be completed using the available tools.
"""

# NOT this (PR #1's approach):
# "You are the planning component for an autonomous agent."  # Too vague!
```

**Why templates are better:**
- ✅ LLM gets specific domain context (better performance)
- ✅ Easy to customize per vertical
- ✅ Maintains expertise while being reusable

---

## Migration Path: Step by Step

### Step 1: Create Vertical Structure (No Breaking Changes)

```bash
# Create new structure alongside existing code
mkdir -p src/dexter/verticals/finance/tools
mkdir -p src/dexter/core
```

**Move (don't delete) files:**
```bash
# Move existing tools to finance vertical
mv src/dexter/tools/* src/dexter/verticals/finance/tools/

# Create vertical config (new file)
# Create base vertical class (new file)
```

**Result:** Code is reorganized, nothing is lost.

### Step 2: Create VerticalConfig Classes

```python
# src/dexter/verticals/finance/__init__.py

from dexter.verticals.finance.config import FinancialVerticalConfig

# Convenience export
FINANCE_VERTICAL = FinancialVerticalConfig()
```

### Step 3: Update Agent to Use Verticals

```python
# Backwards compatible approach
class Agent:
    def __init__(
        self,
        vertical: VerticalConfig = None,  # New parameter
        max_steps: int = 20,
        max_steps_per_task: int = 5
    ):
        # Default to finance vertical for backwards compatibility
        if vertical is None:
            from dexter.verticals.finance import FINANCE_VERTICAL
            vertical = FINANCE_VERTICAL

        self.vertical = vertical
        self.tools = vertical.tools
        # ...
```

**Result:** Existing code still works, new vertical system is available.

### Step 4: Update CLI for Multi-Vertical Support

```python
# src/dexter/cli.py

import click
from dexter.core.agent import Agent
from dexter.verticals.finance import FINANCE_VERTICAL

@click.command()
@click.option('--vertical', default='finance', help='Vertical to use')
def main(vertical: str):
    # Load vertical config
    if vertical == 'finance':
        config = FINANCE_VERTICAL
    # elif vertical == 'legal':
    #     config = LEGAL_VERTICAL
    else:
        click.echo(f"Unknown vertical: {vertical}")
        return

    agent = Agent(vertical=config)

    # Show vertical-specific intro
    click.echo(f"🤖 {config.name} - {config.domain}")
    click.echo(f"Example queries:")
    for example in config.example_queries:
        click.echo(f"  - {example}")

    # Rest of CLI logic...
```

### Step 5: Create Template for New Verticals

```python
# src/dexter/verticals/template/config.py
# (Developers copy this to create new verticals)

from dexter.verticals.base import VerticalConfig
from typing import List
from langchain.tools import BaseTool

class TemplateVerticalConfig(VerticalConfig):
    """
    Template for creating a new vertical.

    Steps:
    1. Copy this file to src/dexter/verticals/YOUR_DOMAIN/config.py
    2. Implement the required properties
    3. Create your domain-specific tools
    4. Update CLI to register your vertical
    """

    @property
    def name(self) -> str:
        return "Your Agent Name"

    @property
    def domain(self) -> str:
        return "your domain (e.g., 'legal research')"

    @property
    def tools(self) -> List[BaseTool]:
        # Import and return your tools
        return []

    @property
    def prompt_variables(self) -> dict:
        return {
            "agent_name": self.name,
            "agent_role": f"autonomous {self.domain} agent",
            "domain": self.domain,
            "task_type": f"{self.domain} query",
            "example_tasks": "TODO: Add example tasks",
        }
```

---

## What Gets Better vs PR #1's Approach

| Aspect | PR #1 Approach | Proper Approach |
|--------|---------------|-----------------|
| Financial Code | ❌ Delete/Remove | ✅ Preserve & Enhance |
| Reusability | ⚠️ Manual tool config | ✅ Vertical plugin system |
| Prompts | ❌ Too generic | ✅ Templated with context |
| Backwards Compat | ❌ Breaking changes | ✅ Defaults to finance |
| New Verticals | ❓ Unclear how | ✅ Clear template & docs |
| Code Organization | ❌ Docs only | ✅ Actual refactor |
| Domain Expertise | ❌ Lost | ✅ Preserved per vertical |
| Ease of Use | ❌ More config needed | ✅ Batteries included |

---

## Example: Creating a Legal Research Vertical

Once the framework is in place, adding a new vertical is straightforward:

```python
# src/dexter/verticals/legal/config.py

from dexter.verticals.base import VerticalConfig
from dexter.verticals.legal.tools import LEGAL_TOOLS

class LegalVerticalConfig(VerticalConfig):
    @property
    def name(self) -> str:
        return "Dexter Legal"

    @property
    def domain(self) -> str:
        return "legal research"

    @property
    def tools(self) -> List[BaseTool]:
        return LEGAL_TOOLS  # Case law search, document analysis, etc.

    @property
    def prompt_variables(self) -> dict:
        return {
            "agent_name": "Dexter Legal",
            "agent_role": "autonomous legal research agent",
            "domain": "legal research",
            "task_type": "legal research query",
            "example_tasks": """
            - Find relevant case law
            - Analyze contract clauses
            - Research legal precedents
            """,
        }

    @property
    def example_queries(self) -> List[str]:
        return [
            "Find cases related to intellectual property in the 9th circuit",
            "Analyze non-compete clause enforceability in California",
        ]

    @property
    def required_env_vars(self) -> List[str]:
        return ["OPENAI_API_KEY", "LEGAL_DATABASE_API_KEY"]
```

```python
# src/dexter/verticals/legal/tools/case_law.py

from langchain.tools import tool

@tool
def search_case_law(query: str, jurisdiction: str = None) -> str:
    """Search for legal cases matching the query."""
    # Implementation here
    pass

@tool
def analyze_contract(contract_text: str) -> str:
    """Analyze contract for potential issues."""
    # Implementation here
    pass

LEGAL_TOOLS = [search_case_law, analyze_contract]
```

**Usage:**
```bash
uv run dexter-agent --vertical legal
```

---

## Implementation Checklist

### Phase 1: Refactor (Week 1)
- [ ] Create `src/dexter/core/` directory
- [ ] Create `src/dexter/verticals/` directory
- [ ] Define `VerticalConfig` base class
- [ ] Move financial tools to `verticals/finance/`
- [ ] Create `FinancialVerticalConfig`
- [ ] Update `Agent` class to accept `VerticalConfig`
- [ ] Ensure backwards compatibility (defaults to finance)
- [ ] Run existing tests to verify nothing broke

### Phase 2: Enhance (Week 2)
- [ ] Create prompt templates with variables
- [ ] Update all prompts to use vertical config
- [ ] Add vertical selection to CLI
- [ ] Create comprehensive documentation
- [ ] Create vertical template for developers
- [ ] Add vertical showcase to README

### Phase 3: Expand (Week 3+)
- [ ] Build second vertical (legal or medical) as proof of concept
- [ ] Create vertical development guide
- [ ] Set up vertical registry/marketplace concept
- [ ] Consider vertical as separate packages (`dexter-finance`, etc.)

---

## Addressing PR #1's Documentation

### What to Keep from PR #1:
- ✅ **The goal** of making Dexter more flexible
- ✅ **The insight** that tools should be modular

### What to Reject from PR #1:
- ❌ **Deleting financial specialization** - preserve it as a vertical
- ❌ **Generic prompts** - use templates instead
- ❌ **Documentation-only changes** - need actual refactor
- ❌ **Making tools optional** - verticals provide tools
- ❌ **"Domain-agnostic" approach** - domains are the feature!

---

## Updated README Structure

```markdown
# Dexter - Multi-Vertical Autonomous Agent

An autonomous agent framework that can be customized for different research domains.
Built on intelligent task planning, self-validation, and domain-specific tools.

## Available Verticals

### 🏦 Finance (Built-in)
Autonomous financial research with SEC filings, financial statements, and company analysis.

**Example queries:**
- "What was Apple's revenue growth over the last 4 quarters?"
- "Compare Microsoft and Google's operating margins for 2023"

```bash
uv run dexter-agent --vertical finance
```

### ⚖️ Legal (Coming Soon)
Case law research, contract analysis, and legal precedent discovery.

### 🏥 Medical (Coming Soon)
Research paper analysis, clinical trial data, and medical literature review.

## Quick Start

### For Users
```bash
# Install
uv sync

# Run with financial vertical (default)
uv run dexter-agent

# Run with specific vertical
uv run dexter-agent --vertical legal
```

### For Developers: Creating a New Vertical

1. Copy the vertical template:
```bash
cp -r src/dexter/verticals/template src/dexter/verticals/YOUR_DOMAIN
```

2. Implement your tools and config
3. Register your vertical in the CLI

See [VERTICAL_DEVELOPMENT_GUIDE.md](docs/VERTICAL_DEVELOPMENT_GUIDE.md) for details.

## Architecture

**Core:** Generic agent logic (planning, action, validation, answer)
**Verticals:** Domain-specific tools and prompts (finance, legal, medical, etc.)

Each vertical provides:
- Domain-specific tools
- Customized prompts
- Example queries
- Required API keys

The core agent orchestrates task planning and execution using the vertical's tools.
```

---

## Why This Approach is Better

### 1. Preserves Value
- All 500+ lines of financial code are kept and enhanced
- Financial vertical becomes the reference implementation
- New developers can learn from working example

### 2. Enables Growth
- Clear path to add legal, medical, scientific verticals
- Template makes creating new verticals straightforward
- Each vertical can have its own tools and prompts

### 3. Better UX
- Default vertical (finance) means existing usage still works
- `--vertical` flag makes switching easy
- Each vertical shows relevant examples on startup

### 4. Better Performance
- Verticals provide specific context to LLM
- Domain-aware prompts perform better than generic ones
- Tools are curated for each domain

### 5. Maintainable
- Clear separation of concerns
- Core agent logic is domain-agnostic
- Vertical logic is domain-specific and isolated
- Easy to test each vertical independently

---

## Next Steps

### Option A: Implement This Plan
1. Review this document
2. Start with Phase 1 (refactor without breaking changes)
3. Move financial code to vertical structure
4. Test that everything still works
5. Then expand to new verticals

### Option B: Hybrid Approach
1. Keep current structure for finance (it works!)
2. Build new verticals using the framework described here
3. Refactor finance vertical later once pattern is proven

### Option C: Remove PR #1, Start Fresh
1. Delete the 4 documentation files from PR #1
2. Implement proper refactor with code changes
3. Follow the plan in this document

---

## Conclusion

**PR #1's goal is right, but the approach is wrong.**

- ✅ **Right:** Make Dexter adaptable to multiple verticals
- ❌ **Wrong:** Delete financial specialization and make prompts generic

**The proper approach:**
- ✅ Preserve financial tools as first vertical (reference implementation)
- ✅ Create vertical plugin system for extensibility
- ✅ Use prompt templates (not generic prompts) for better LLM performance
- ✅ Provide clear path for developers to add new verticals

**Bottom Line:** Don't throw away 500 lines of working financial code. Reorganize it into a vertical, then build the framework around it. The financial implementation is not technical debt - it's your MVP and reference implementation.

---

**Generated by:** Claude (Anthropic)
**Session:** claude/review-git-history-011CUMHVxmGA8dWTVz2qyohb
**Date:** 2025-10-22
