"""Financial research vertical for Dexter."""

from dexter.verticals.finance.config import FinancialVerticalConfig

# Singleton instance for convenience
FINANCE_VERTICAL = FinancialVerticalConfig()

__all__ = ["FinancialVerticalConfig", "FINANCE_VERTICAL"]
