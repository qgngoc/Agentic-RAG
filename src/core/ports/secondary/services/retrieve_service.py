
from abc import ABC, abstractmethod
from typing import Union

from core.entities import Client, SearchQueryWithVector, DocumentWithVector, Document

class RetrieveService(ABC):
    """Service interface for retrieving documents."""

    @abstractmethod
    def retrieve(
        self, search_query: SearchQueryWithVector, client: Client, limit: int = 10
    ) -> list[Union[DocumentWithVector, Document]]:
        """Find documents by their vector representation."""
        pass
    
    @abstractmethod
    async def aretrieve(
        self, search_query: SearchQueryWithVector, client: Client, limit: int = 10
    ) -> list[Union[DocumentWithVector, Document]]:
        """Find documents by their vector representation."""
        pass