from abc import ABC, abstractmethod
from typing import List

from core.entities import FileContent, Document

class ChunkingService(ABC):
    """Service interface for chunking documents into smaller parts."""
    
    @abstractmethod
    async def chunk(self, file_content: FileContent) -> List[Document]:
        """Chunk the content of a file into smaller parts."""
        pass
    
    @abstractmethod
    async def achunk(self, file_content: FileContent) -> List[Document]:
        """Asynchronously chunk the content of a file into smaller parts."""
        pass
    
class TextChunkingService(ChunkingService):
    """Chunking service for text files."""
    pass


class MarkdownChunkingService(ChunkingService):
    """Chunking service for markdown files."""
    pass