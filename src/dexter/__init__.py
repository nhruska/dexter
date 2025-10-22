# This file makes the directory a Python package

# For backwards compatibility, re-export Agent from core
from dexter.core.agent import Agent

__all__ = ["Agent"] 