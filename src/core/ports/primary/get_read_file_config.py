from abc import ABC, abstractmethod 
from typing import List

from core.entities import ReadFileConfig

class GetReadFileConfigPort(ABC):
    """Use case for retrieving read file configurations."""

    @abstractmethod
    def get_read_file_config(self, key: str) -> ReadFileConfig:
        """Retrieve a specific read file configuration by its key."""
        pass
    
    @abstractmethod
    async def aget_read_file_config(self, key: str) -> ReadFileConfig:
        """Asynchronously retrieve a specific read file configuration by its key."""
        pass