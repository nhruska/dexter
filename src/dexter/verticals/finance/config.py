"""Configuration for the financial research vertical."""

from typing import List, Dict
from dexter.verticals.base import VerticalConfig
from dexter.verticals.finance.tools import TOOLS


class FinancialVerticalConfig(VerticalConfig):
    """Configuration for financial research vertical.

    Provides access to SEC filings, financial statements, and company analysis tools.
    """

    @property
    def name(self) -> str:
        return "Dexter"

    @property
    def domain(self) -> str:
        return "financial research"

    @property
    def tools(self) -> List:
        return TOOLS

    @property
    def prompt_variables(self) -> Dict[str, str]:
        return {
            "agent_name": "Dexter",
            "agent_role": "autonomous financial research agent",
            "domain": "financial research",
            "task_type": "financial research query",
            "example_tasks": """
            - Analyze revenue trends and growth rates
            - Compare financial metrics across companies
            - Review SEC filings for specific information
            - Extract data from financial statements
            """,
        }

    @property
    def example_queries(self) -> List[str]:
        return [
            "What was Apple's revenue growth over the last 4 quarters?",
            "Compare Microsoft and Google's operating margins for 2023",
            "Analyze Tesla's cash flow trends over the past year",
            "What is Amazon's debt-to-equity ratio based on recent financials?",
        ]

    @property
    def required_env_vars(self) -> List[str]:
        return ["OPENAI_API_KEY", "FINANCIAL_DATASETS_API_KEY"]

    @property
    def description(self) -> str:
        return "Autonomous financial research agent with access to SEC filings and financial statements"
