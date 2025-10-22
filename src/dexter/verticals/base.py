"""Base class for vertical-specific configurations."""

from abc import ABC, abstractmethod
from typing import List, Dict, Any


class VerticalConfig(ABC):
    """Base class for domain-specific vertical configurations.

    Each vertical (finance, legal, medical, etc.) implements this interface
    to provide domain-specific tools, prompts, and configuration.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Display name of the agent (e.g., 'Dexter')."""
        pass

    @property
    @abstractmethod
    def domain(self) -> str:
        """Domain description (e.g., 'financial research')."""
        pass

    @property
    @abstractmethod
    def tools(self) -> List[Any]:
        """List of domain-specific tools available to the agent."""
        pass

    @property
    @abstractmethod
    def prompt_variables(self) -> Dict[str, str]:
        """Variables to inject into prompt templates.

        Should include:
        - agent_name: Name of the agent
        - agent_role: Role description
        - domain: Domain name
        - task_type: Type of tasks this agent handles
        - example_tasks: Example tasks for this domain
        """
        pass

    @property
    def example_queries(self) -> List[str]:
        """Example queries users can try with this vertical."""
        return []

    @property
    def required_env_vars(self) -> List[str]:
        """Required environment variables for this vertical."""
        return ["OPENAI_API_KEY"]

    @property
    def description(self) -> str:
        """Short description of what this vertical does."""
        return f"Autonomous {self.domain} agent"
