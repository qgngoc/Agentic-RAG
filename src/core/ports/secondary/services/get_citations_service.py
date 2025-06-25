
from abc import ABC, abstractmethod
from typing import Union

from core.entities import Document, DocumentWithVector, Citation

class GetCitationsService(ABC):
    """Service interface for retrieving citations."""

    @abstractmethod
    def get_citations(
        self, documents: list[Union[DocumentWithVector, Document]]
    ) -> list[Citation]:
        """Retrieve citations for a given document."""
        pass

    @abstractmethod
    async def aget_citations(
        self, documents: list[Union[DocumentWithVector, Document]]
    ) -> list[Citation]:
        """Asynchronously retrieve citations for a given document."""
        pass