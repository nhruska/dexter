#!/usr/bin/env python3
"""Test script to verify all imports work correctly after refactoring."""

import sys
import traceback

def test_import(description, import_func):
    """Test an import and print result."""
    try:
        result = import_func()
        print(f"✓ {description}")
        return True
    except Exception as e:
        print(f"✗ {description}")
        print(f"  Error: {e}")
        traceback.print_exc()
        return False

def main():
    print("Testing Dexter Multi-Vertical Architecture Imports\n")
    print("=" * 60)

    all_passed = True

    # Test 1: Core imports
    print("\n1. Testing core module imports:")
    all_passed &= test_import(
        "Import Agent from dexter",
        lambda: __import__('dexter', fromlist=['Agent'])
    )
    all_passed &= test_import(
        "Import from dexter.core.agent",
        lambda: __import__('dexter.core.agent', fromlist=['Agent'])
    )
    all_passed &= test_import(
        "Import from dexter.core.model",
        lambda: __import__('dexter.core.model', fromlist=['call_llm'])
    )
    all_passed &= test_import(
        "Import from dexter.core.schemas",
        lambda: __import__('dexter.core.schemas', fromlist=['Task'])
    )

    # Test 2: Vertical base imports
    print("\n2. Testing vertical base imports:")
    all_passed &= test_import(
        "Import VerticalConfig",
        lambda: __import__('dexter.verticals.base', fromlist=['VerticalConfig'])
    )

    # Test 3: Finance vertical imports
    print("\n3. Testing finance vertical imports:")
    all_passed &= test_import(
        "Import FINANCE_VERTICAL",
        lambda: __import__('dexter.verticals.finance', fromlist=['FINANCE_VERTICAL'])
    )
    all_passed &= test_import(
        "Import FinancialVerticalConfig",
        lambda: __import__('dexter.verticals.finance.config', fromlist=['FinancialVerticalConfig'])
    )

    # Test 4: Finance tools imports
    print("\n4. Testing finance tools imports:")
    all_passed &= test_import(
        "Import from finance.tools",
        lambda: __import__('dexter.verticals.finance.tools', fromlist=['TOOLS'])
    )
    all_passed &= test_import(
        "Import financial tools",
        lambda: __import__('dexter.verticals.finance.tools.financials', fromlist=['get_income_statements'])
    )
    all_passed &= test_import(
        "Import filings tools",
        lambda: __import__('dexter.verticals.finance.tools.filings', fromlist=['get_filings'])
    )

    # Test 5: Verify objects
    print("\n5. Testing object instantiation:")
    try:
        from dexter.verticals.finance import FINANCE_VERTICAL
        print(f"✓ FINANCE_VERTICAL instantiated")
        print(f"  - Name: {FINANCE_VERTICAL.name}")
        print(f"  - Domain: {FINANCE_VERTICAL.domain}")
        print(f"  - Tools count: {len(FINANCE_VERTICAL.tools)}")
        print(f"  - Example queries: {len(FINANCE_VERTICAL.example_queries)}")
    except Exception as e:
        print(f"✗ FINANCE_VERTICAL instantiation failed")
        print(f"  Error: {e}")
        all_passed = False

    # Test 6: Agent instantiation
    print("\n6. Testing Agent instantiation:")
    try:
        from dexter import Agent
        agent = Agent()
        print(f"✓ Agent() with default vertical")
        print(f"  - Vertical name: {agent.vertical.name}")
        print(f"  - Tools available: {len(agent.tools)}")
    except Exception as e:
        print(f"✗ Agent instantiation failed")
        print(f"  Error: {e}")
        traceback.print_exc()
        all_passed = False

    try:
        from dexter import Agent
        from dexter.verticals.finance import FINANCE_VERTICAL
        agent = Agent(vertical=FINANCE_VERTICAL)
        print(f"✓ Agent(vertical=FINANCE_VERTICAL)")
        print(f"  - Vertical name: {agent.vertical.name}")
        print(f"  - Tools available: {len(agent.tools)}")
    except Exception as e:
        print(f"✗ Agent with explicit vertical failed")
        print(f"  Error: {e}")
        traceback.print_exc()
        all_passed = False

    # Summary
    print("\n" + "=" * 60)
    if all_passed:
        print("✓ ALL TESTS PASSED")
        return 0
    else:
        print("✗ SOME TESTS FAILED")
        return 1

if __name__ == "__main__":
    sys.exit(main())
