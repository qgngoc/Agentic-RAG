from abc import ABC, abstractmethod
from typing import List, Optional

from core.entities import DocumentWithVector, Client, SearchQueryWithVector


class VectorDBRepository(ABC):
    """Repository interface for vector operations."""
        
    @abstractmethod
    def insert_document(
        self, client: Client, document: DocumentWithVector
    ) -> DocumentWithVector:
        """Insert a document into the vector database."""
        pass
    
    @abstractmethod
    def insert_documents(
        self, client: Client, documents: List[DocumentWithVector]
    ) -> List[DocumentWithVector]:
        """Insert multiple documents into the vector database."""
        pass
    
    @abstractmethod
    def retrieve_documents(
        self, client: Client, search_query: SearchQueryWithVector, limit: int = 20
    ) -> List[DocumentWithVector]:
        """Retrieve documents based on a search query."""
        pass
    
    @abstractmethod
    async def ainsert_document(
        self, client: Client, document: DocumentWithVector
    ) -> DocumentWithVector:
        """Asynchronously insert a document into the vector database."""
        pass

    @abstractmethod
    async def ainsert_documents(
        self, client: Client, documents: List[DocumentWithVector]
    ) -> List[DocumentWithVector]:
        """Asynchronously insert multiple documents into the vector database."""
        pass

    @abstractmethod
    async def aretrieve_documents(
        self, client: Client, search_query: SearchQueryWithVector, limit: int = 20
    ) -> List[DocumentWithVector]:
        """Asynchronously retrieve documents based on a search query."""
        pass
    