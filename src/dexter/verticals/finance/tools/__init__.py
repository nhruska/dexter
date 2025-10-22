from typing_extensions import Callable
from dexter.verticals.finance.tools.financials import get_income_statements
from dexter.verticals.finance.tools.financials import get_balance_sheets
from dexter.verticals.finance.tools.financials import get_cash_flow_statements
from dexter.verticals.finance.tools.filings import get_filings
from dexter.verticals.finance.tools.filings import get_10K_filing_items
from dexter.verticals.finance.tools.filings import get_10Q_filing_items
from dexter.verticals.finance.tools.filings import get_8K_filing_items

TOOLS: list[Callable[..., any]] = [
    get_income_statements,
    get_balance_sheets,
    get_cash_flow_statements,
    get_10K_filing_items,
    get_10Q_filing_items,
    get_8K_filing_items,
    get_filings,
]
