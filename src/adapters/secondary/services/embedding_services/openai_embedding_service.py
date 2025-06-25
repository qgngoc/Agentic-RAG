from typing import List
from openai import OpenAI

from core.ports.secondary.services import EmbeddingService

class OpenAIEmbeddingServiceImpl(EmbeddingService):
    def __init__(self, model_name: str = "text-embedding-3-small", base_url: str = None, api_key: str = None):
        self._model_name = model_name
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )

        # Model dimensions map
        self._dimension_map = {
            "text-embedding-ada-002": 1536,
            "text-embedding-3-small": 1536,
            "text-embedding-3-large": 3072
        }

    def create_embedding(self, text: str) -> list[float]:
        """Create an embedding for the given text using OpenAI API."""
        response = self.client.embeddings.create(
            model=self._model_name,
            input=text
        )
        return response.data[0].embedding
    
    async def acreate_embedding(self, text: str) -> list[float]:
        """Create an embedding for the given text using OpenAI API."""
        response = self.client.embeddings.create(
            model=self._model_name,
            input=text
        )
        return response.data[0].embedding


    def get_model_name(self) -> str:
        """Return the name of the embedding model."""
        return self._model_name
    
    def get_embedding_dimension(self) -> int:   
        """Return the dimension of the embedding vectors."""
        return self._dimension_map.get(self._model_name, 1536)
    
    async def aget_model_name(self) -> str:
        """Asynchronously return the name of the embedding model."""
        return self._model_name
    
    async def aget_embedding_dimension(self) -> int:
        """Asynchronously return the dimension of the embedding vectors."""
        return self._dimension_map.get(self._model_name, 1536)