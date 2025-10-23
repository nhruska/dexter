# Dexter 🤖

An autonomous agent framework for domain-specific research and analysis. Built on intelligent task planning, self-validation, and pluggable domain expertise.

**Current Status:** Multi-vertical architecture with financial research as the flagship implementation.

<img width="979" height="651" alt="Dexter Financial Research Demo" src="https://github.com/user-attachments/assets/5a2859d4-53cf-4638-998a-15cef3c98038" />

## What is Dexter?

Dexter is not just another chatbot. It's an autonomous agent that:
- 📋 **Plans ahead** - Breaks complex queries into structured, actionable tasks
- 🔄 **Self-validates** - Checks its own work and iterates until complete
- 🎯 **Domain-focused** - Uses specialized tools and knowledge for specific fields
- 🔌 **Extensible** - Plugin architecture for multiple domain verticals

Think of it as **Claude Code for domain-specific research** - whether that's financial analysis, legal research, medical literature review, or any other specialized field.

## Quick Start (Financial Research)

Get up and running with financial research in under 2 minutes.

### Prerequisites

- **Python 3.10+**
- **[uv](https://github.com/astral-sh/uv)** package manager (recommended) or pip
- **OpenAI API key** ([get one here](https://platform.openai.com/api-keys))
- **Financial Datasets API key** ([get one here](https://financialdatasets.ai))

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/nhruska/dexter.git
cd dexter

# 2. Install dependencies
uv sync
# OR with pip: pip install -e .

# 3. Set up environment variables
cp env.example .env

# 4. Edit .env and add your API keys
# OPENAI_API_KEY=sk-...
# FINANCIAL_DATASETS_API_KEY=...
```

### Run Dexter

```bash
# Start interactive mode (defaults to financial research vertical)
uv run dexter-agent

# Or with Python directly
python -m dexter.cli
```

### Try These Queries

```
>> What was Apple's revenue growth over the last 4 quarters?
>> Compare Microsoft and Google's operating margins for 2023
>> Analyze Tesla's cash flow trends over the past year
>> What is Amazon's debt-to-equity ratio based on recent financials?
```

Dexter will automatically:
1. 📋 Break down your question into research tasks
2. 🔍 Fetch necessary financial data (SEC filings, statements)
3. 🧮 Perform calculations and analysis
4. 📊 Provide a comprehensive, data-backed answer

---

## Architecture Overview

### Multi-Vertical Design

Dexter uses a **core + verticals** architecture that separates domain-agnostic agent logic from domain-specific implementations.

```
┌─────────────────────────────────────────┐
│          DEXTER CORE                    │
│  ┌─────────────────────────────────┐   │
│  │  Planning → Action → Validation  │   │
│  │  → Answer Generation             │   │
│  └─────────────────────────────────┘   │
└───────────────┬─────────────────────────┘
                │
     ┌──────────┴──────────┬──────────────┬─────────────┐
     │                     │              │             │
┌────▼─────┐      ┌───────▼──────┐  ┌───▼────┐   ┌───▼────┐
│ FINANCE  │      │    LEGAL     │  │ MEDICAL│   │ CUSTOM │
│ VERTICAL │      │   VERTICAL   │  │VERTICAL│   │VERTICAL│
│          │      │  (Phase 3)   │  │(Future)│   │  (You!) │
│ ✅ Active│      │              │  │        │   │         │
└──────────┘      └──────────────┘  └────────┘   └─────────┘
```

### Agent Components

**Core Engine:**
- **Planning Agent** - Decomposes queries into structured task lists
- **Action Agent** - Selects and executes appropriate tools
- **Validation Agent** - Verifies task completion and data sufficiency
- **Answer Agent** - Synthesizes findings into comprehensive responses

**Vertical System:**
- **VerticalConfig** - Abstract interface for all verticals
- **Pluggable Tools** - Domain-specific data sources and APIs
- **Custom Prompts** - Domain-aware instructions for better LLM performance
- **Example Queries** - Domain-specific query templates

---

## Project Structure

```
dexter/
├── src/dexter/
│   ├── core/                      # Domain-agnostic agent logic
│   │   ├── agent.py              # Main orchestration
│   │   ├── model.py              # LLM interface
│   │   ├── prompts.py            # System prompts
│   │   └── schemas.py            # Data models
│   │
│   ├── verticals/                 # Domain-specific implementations
│   │   ├── base.py               # VerticalConfig interface
│   │   │
│   │   ├── finance/              # Financial research vertical ✅
│   │   │   ├── config.py         # Finance vertical config
│   │   │   └── tools/            # Financial tools (440+ lines)
│   │   │       ├── filings.py    # SEC filings (10-K, 10-Q, 8-K)
│   │   │       ├── financials.py # Income, balance, cash flow
│   │   │       ├── constants.py  # Financial data schemas
│   │   │       └── api.py        # Financial Datasets API
│   │   │
│   │   └── template/             # Template for new verticals
│   │
│   ├── utils/                     # Utilities (logging, UI)
│   └── cli.py                     # CLI entry point
│
├── docs/                          # Documentation
│   ├── 01_tool_refactoring.md
│   ├── 02_prompt_generalization.md
│   ├── 03_agent_decoupling.md
│   └── 04_readme_update.md
│
├── PROPER_GENERALIZATION_PLAN.md  # Architecture guide
├── TEST_RESULTS.md                # Test documentation
├── test_imports.py                # Test suite
├── pyproject.toml                 # Project config
└── uv.lock                        # Dependency lock file
```

---

## Usage Guide

### Basic Usage (Financial Research)

```python
from dexter import Agent

# Create agent with default financial vertical
agent = Agent()

# Run a query
result = agent.run("What was Apple's revenue in 2023?")
print(result)
```

### Advanced Configuration

```python
from dexter import Agent
from dexter.verticals.finance import FINANCE_VERTICAL

# Explicit vertical selection
agent = Agent(
    vertical=FINANCE_VERTICAL,
    max_steps=20,              # Global safety limit
    max_steps_per_task=5       # Per-task iteration limit
)

# Run query
result = agent.run("Compare tech giants' profit margins")
```

### Programmatic Use

```python
from dexter import Agent

agent = Agent()

# Single query
answer = agent.run("Analyze NVIDIA's quarterly revenue trends")

# Multiple queries
queries = [
    "What is Tesla's current ratio?",
    "How does it compare to Ford?",
    "What does this tell us about liquidity?"
]

for query in queries:
    print(f"\nQ: {query}")
    print(f"A: {agent.run(query)}")
```

---

## Creating Custom Verticals

Want to use Dexter for legal research, medical analysis, or another domain? Create your own vertical!

### 1. Create Vertical Structure

```bash
mkdir -p src/dexter/verticals/legal/tools
```

### 2. Define Your Vertical Config

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
    def tools(self) -> List:
        return LEGAL_TOOLS  # Your legal research tools

    @property
    def prompt_variables(self) -> Dict[str, str]:
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
            "Find cases about intellectual property in the 9th circuit",
            "Analyze non-compete clause enforceability in California",
        ]

    @property
    def required_env_vars(self) -> List[str]:
        return ["OPENAI_API_KEY", "LEGAL_DATABASE_API_KEY"]
```

### 3. Create Your Tools

```python
# src/dexter/verticals/legal/tools.py

from langchain.tools import tool

@tool
def search_case_law(query: str, jurisdiction: str = None) -> str:
    """Search for legal cases matching the query."""
    # Your implementation here
    pass

@tool
def analyze_contract(contract_text: str) -> str:
    """Analyze contract for potential issues."""
    # Your implementation here
    pass

LEGAL_TOOLS = [search_case_law, analyze_contract]
```

### 4. Use Your Vertical

```python
from dexter import Agent
from dexter.verticals.legal.config import LegalVerticalConfig

agent = Agent(vertical=LegalVerticalConfig())
result = agent.run("Find cases about software licensing in California")
```

### See More

📖 **Full guide:** See `PROPER_GENERALIZATION_PLAN.md` for detailed instructions on creating verticals.

📋 **Template:** Check `src/dexter/verticals/template/` for a starting template.

---

## Available Verticals

### ✅ Financial Research (Active)

**Domain:** SEC filings, financial statements, company analysis
**API Required:** [Financial Datasets](https://financialdatasets.ai)

**Tools:**
- `get_income_statements` - Retrieve income statements
- `get_balance_sheets` - Retrieve balance sheets
- `get_cash_flow_statements` - Retrieve cash flow statements
- `get_filings` - Search SEC filings
- `get_10K_filing_items` - Extract 10-K sections
- `get_10Q_filing_items` - Extract 10-Q sections
- `get_8K_filing_items` - Extract 8-K sections

**Example Queries:**
```
What was Apple's revenue growth over the last 4 quarters?
Compare Microsoft and Google's operating margins for 2023
Analyze Tesla's cash flow trends over the past year
What is Amazon's debt-to-equity ratio?
```

### 🚧 Legal Research (Coming Soon - Phase 3)

Case law search, contract analysis, legal precedent discovery.

### 🚧 Medical Research (Future)

Research paper analysis, clinical trial data, medical literature review.

### 🎨 Your Custom Vertical

Whatever domain you need! Follow the guide above to create your own.

---

## Configuration Options

### Agent Parameters

```python
Agent(
    vertical: VerticalConfig = None,  # Vertical to use (defaults to finance)
    max_steps: int = 20,               # Global step limit (prevents runaway)
    max_steps_per_task: int = 5        # Per-task step limit
)
```

### Environment Variables

**Required:**
```bash
OPENAI_API_KEY=sk-...  # Your OpenAI API key
```

**For Financial Vertical:**
```bash
FINANCIAL_DATASETS_API_KEY=...  # From financialdatasets.ai
```

**For Future Verticals:**
```bash
LEGAL_DATABASE_API_KEY=...      # When legal vertical is ready
MEDICAL_DATABASE_API_KEY=...    # When medical vertical is ready
```

---

## Development

### Running Tests

```bash
# Run structure tests
PYTHONPATH=src python3 test_imports.py

# Check syntax
find src -name "*.py" -exec python3 -m py_compile {} \;
```

### Project Standards

- **Python 3.10+** required
- **Type hints** encouraged
- **Docstrings** for all public functions
- **Keep PRs focused** - one feature per PR

### Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests
5. Commit (`git commit -m 'Add amazing feature'`)
6. Push to branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

**Creating a New Vertical?** See `PROPER_GENERALIZATION_PLAN.md` for guidance.

---

## Troubleshooting

### Import Errors

**Problem:** `ModuleNotFoundError: No module named 'langchain_core'`

**Solution:**
```bash
# Make sure dependencies are installed
uv sync
# OR
pip install -r requirements.txt
```

### API Errors

**Problem:** `401 Unauthorized` or API errors

**Solution:**
```bash
# Check your .env file has valid API keys
cat .env

# Make sure OPENAI_API_KEY and FINANCIAL_DATASETS_API_KEY are set
# Get keys from:
# - OpenAI: https://platform.openai.com/api-keys
# - Financial Datasets: https://financialdatasets.ai
```

### Agent Not Stopping

**Problem:** Agent keeps running indefinitely

**Solution:**
```python
# Reduce step limits
agent = Agent(
    max_steps=10,           # Lower global limit
    max_steps_per_task=3    # Lower per-task limit
)
```

---

## Roadmap

### ✅ Phase 1 - Multi-Vertical Architecture (Current)
- [x] Refactor into core + verticals
- [x] Preserve financial vertical (440+ lines)
- [x] Create VerticalConfig interface
- [x] Backwards compatibility
- [x] Comprehensive documentation

### 🚧 Phase 2 - Enhanced Vertical System (Next)
- [ ] Prompt templates with variable substitution
- [ ] CLI `--vertical` flag for vertical selection
- [ ] Vertical development guide
- [ ] Example custom vertical tutorial

### 🔮 Phase 3 - Vertical Expansion (Future)
- [ ] Legal research vertical
- [ ] Medical research vertical
- [ ] Scientific research vertical
- [ ] Vertical marketplace/registry

---

## Documentation

- **[PROPER_GENERALIZATION_PLAN.md](PROPER_GENERALIZATION_PLAN.md)** - Complete architecture guide
- **[CLAUDE_GIT_HISTORY_ANALYSIS.md](CLAUDE_GIT_HISTORY_ANALYSIS.md)** - Project history and decisions
- **[TEST_RESULTS.md](TEST_RESULTS.md)** - Test documentation
- **[docs/](docs/)** - Additional documentation files

---

## Key Features

### 🎯 Domain-Specific Intelligence
Unlike generic chatbots, Dexter uses domain-specific tools and knowledge bases for accurate, specialized research.

### 🔄 Autonomous Task Execution
Dexter doesn't just answer questions - it plans a research strategy, executes it, validates results, and synthesizes findings.

### 🛡️ Safety Features
Built-in loop detection and step limits prevent runaway execution and ensure predictable behavior.

### 🔌 Extensible Architecture
Clean vertical system makes it easy to add new domains without touching core agent logic.

### ⚡ Backwards Compatible
Existing code works unchanged - the refactor maintains full backwards compatibility.

---

## Why Multi-Vertical?

**Before (Specialized):** Great financial agent, but locked to one domain.

**After (Multi-Vertical):**
- ✅ Keep financial expertise (nothing lost!)
- ✅ Add legal, medical, scientific domains
- ✅ Let developers create custom verticals
- ✅ Maintain domain-specific performance

**Best of both worlds:** Specialized performance + flexible architecture.

---

## Credits

**Original Author:** [@virattt](https://twitter.com/virattt)
**Fork Maintainer:** [@nhruska](https://github.com/nhruska)
**Multi-Vertical Architecture:** Phase 1 refactor (2025-10-22)

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

## Community

- **Issues:** [GitHub Issues](https://github.com/nhruska/dexter/issues)
- **Discussions:** [GitHub Discussions](https://github.com/nhruska/dexter/discussions)
- **Original Project:** [virattt/dexter](https://github.com/virattt/dexter)

---

## Quick Links

- 📖 [Architecture Guide](PROPER_GENERALIZATION_PLAN.md)
- 🧪 [Test Results](TEST_RESULTS.md)
- 📊 [Git History Analysis](CLAUDE_GIT_HISTORY_ANALYSIS.md)
- 🔧 [Creating Custom Verticals](#creating-custom-verticals)
- 🚀 [Quick Start](#quick-start-financial-research)

---

**Built with ❤️ for researchers, analysts, and domain experts who need more than a chatbot.**
