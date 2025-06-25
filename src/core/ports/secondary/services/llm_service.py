from abc import ABC, abstractmethod
from typing import List, Dict, Any, Union

from core.entities import LLMConfig, Message, Tool, LLMCompletion

class LLMService(ABC):
    """Service interface for LLM operations."""

    @abstractmethod
    def chat(self, llm_config: LLMConfig, messages: List[Message], tools: List[Tool] = None) -> LLMCompletion:
        """Perform a chat operation."""
        pass
    
    @abstractmethod
    def get_llm_config_keys(self) -> List[str]:
        """Get the keys of all LLM configurations."""
        pass
    
    @abstractmethod
    def get_llm_config(self, key: str) -> LLMConfig:
        """Retrieve a specific LLM configuration by its key."""
        pass
    
    
    @abstractmethod
    def add_llm_config(self, key: str, llm_config: LLMConfig) -> None:
        """Add a new LLM configuration."""
        pass
    
    @abstractmethod
    async def achat(self, llm_config: LLMConfig, messages: List[Message], tools: List[Tool] = None) -> LLMCompletion:
        """Asynchronously perform a chat operation."""
        pass
    
    @abstractmethod
    async def aget_llm_config_keys(self) -> List[str]:
        """Asynchronously retrieve a list of LLM configuration keys."""
        pass
    
    @abstractmethod
    async def aget_llm_config(self, key: str) -> LLMConfig:
        """Asynchronously retrieve a specific LLM configuration by its key."""
        pass
    
    @abstractmethod
    async def aadd_llm_config(self, key: str, llm_config: LLMConfig) -> None:
        """Asynchronously add a new LLM configuration."""
        pass
    