from abc import ABC, abstractmethod
from typing import List


class EmbeddingService(ABC):
    """Service interface for generating embeddings."""
    
    @abstractmethod
    def create_embedding(self, text: str) -> List[float]:
        """Create an embedding vector from text."""
        pass
    
    @abstractmethod
    async def acreate_embedding(self, text: str) -> List[float]:
        """Asynchronously create an embedding vector from text."""
        pass
    
    @abstractmethod 
    def get_model_name(self) -> str:
        """Return the name of the embedding model."""
        pass
    
    @abstractmethod
    def get_embedding_dimension(self) -> int:
        """Return the dimension of the embedding vectors."""
        pass
    
    @abstractmethod
    async def aget_model_name(self) -> str:
        """Asynchronously return the name of the embedding model."""
        pass
    
    @abstractmethod
    async def aget_embedding_dimension(self) -> int:
        """Asynchronously return the dimension of the embedding vectors."""
        pass