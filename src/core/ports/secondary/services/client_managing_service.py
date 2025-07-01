
from abc import ABC, abstractmethod

from core.entities import Client

class ClientManagingService(ABC):

    @abstractmethod
    def create_client(self, client: Client) -> Client:
        """Create a new client."""
        pass
    
    @abstractmethod
    def delete_client(self, client_id: str) -> None:
        """Delete a client by its ID."""
        pass
    
    @abstractmethod
    async def acreate_client(self, client: Client) -> Client:
        """Asynchronously create a new client."""
        pass
    
    @abstractmethod
    async def adelete_client(self, client_id: str) -> None:
        """Asynchronously delete a client by its ID."""
        pass