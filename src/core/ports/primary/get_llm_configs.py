
from abc import ABC, abstractmethod
from typing import List

from core.entities import LLMConfig

class GetLLMConfigsPort(ABC):
    """Use case for retrieving LLM configurations."""

    @abstractmethod
    def get_llm_config_keys(self) -> List[str]:
        """Retrieve a list of LLM configuration keys."""
        pass

    @abstractmethod
    def get_llm_config(self, key: str) -> LLMConfig:
        """Retrieve a specific LLM configuration by its key."""
        pass
    
    @abstractmethod
    async def aget_llm_config_keys(self) -> List[str]:
        """Asynchronously retrieve a list of LLM configuration keys."""
        pass
    
    @abstractmethod
    async def aget_llm_config(self, key: str) -> LLMConfig:
        """Asynchronously retrieve a specific LLM configuration by its key."""
        pass