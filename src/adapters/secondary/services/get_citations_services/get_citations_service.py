
from core.ports.secondary.services import GetCitationsService

from core.entities import Document, DocumentWithVector, Citation

class GetCitationsServiceImpl(GetCitationsService):
    def __init__(self):
        pass
    
    def get_citations(self, documents: list[Document]) -> list[Citation]:
        """Retrieve citations for a given document."""
        citations = [Citation(
            file_name=doc.file_name,
            file_path=doc.file_path,
            page_number=doc.page_number,
            page_content=doc.content
        ) for doc in documents]
        return citations
    
    async def aget_citations(self, documents: list[Document]) -> list[Citation]:
        """Asynchronously retrieve citations for a given document."""
        # For now, we will use the synchronous method in the async context.
        # TODO: Implement asynchronous retrieval of citations.
        return self.get_citations(documents)