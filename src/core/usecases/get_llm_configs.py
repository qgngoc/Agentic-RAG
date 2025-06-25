

from typing import List

from core.entities import LLMConfig
from core.ports.primary.get_llm_configs import GetLLMConfigsPort
from core.ports.secondary.services import LLMService

class GetLLMConfigsUseCaseImpl(GetLLMConfigsPort):
    def __init__(self, llm_service: LLMService):
        """Initialize the GetLLMConfigsUseCaseImpl with the LLM service."""
        self.llm_service = llm_service
        
    def get_llm_config_keys(self) -> List[str]:
        """Retrieve a list of LLM configuration keys."""
        return self.llm_service.get_llm_config_keys()
    
    def get_llm_config(self, key: str) -> LLMConfig:
        """Retrieve a specific LLM configuration by its key."""
        return self.llm_service.get_llm_config(key)
    
    async def aget_llm_config_keys(self) -> List[str]:
        """Asynchronously retrieve a list of LLM configuration keys."""
        return await self.llm_service.aget_llm_config_keys()
    
    async def aget_llm_config(self, key: str) -> LLMConfig:
        """Asynchronously retrieve a specific LLM configuration by its key."""
        return await self.llm_service.aget_llm_config(key)