from abc import ABC, abstractmethod
from typing import List

from core.entities import Document, DocumentWithVector, InputFile, Client, IndexDocumentStatus

class IndexDocumentPort(ABC):
    """Use case for indexing documents."""

    @abstractmethod
    def index_document(self, client: Client, input_file: InputFile) -> IndexDocumentStatus:
        """Index a document with its metadata."""
        pass

    @abstractmethod
    def index_documents(self, client: Client, input_files: List[InputFile]) -> List[IndexDocumentStatus]:
        """Index multiple documents with their metadata."""
        pass
    
    @abstractmethod
    async def aindex_document(self, client: Client, input_file: InputFile) -> IndexDocumentStatus:
        """Asynchronously index a document with its metadata."""
        pass
    
    @abstractmethod 
    async def aindex_documents(self, client: Client, input_files: List[InputFile]) -> List[IndexDocumentStatus]:
        """Asynchronously index multiple documents with their metadata."""
        pass
    