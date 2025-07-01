
from abc import ABC, abstractmethod

from core.entities import Client

class ClientManagePort(ABC):
    """Use case for managing clients."""

    @abstractmethod
    def create_client(self, client: Client) -> Client:
        """
        Create a new client.
        
        Args:
            client (Client): The client object to be created.
        
        Returns:
            Client: The created client object.
        """
        pass

    @abstractmethod
    def delete_client(self, client_id: str) -> None:
        """
        Delete a client by its ID.
        
        Args:
            client_id (str): The ID of the client to be deleted.
        """
        pass

    @abstractmethod
    async def acreate_client(self, client: Client) -> Client:
        """Asynchronously create a new client."""
        pass

    @abstractmethod
    async def adelete_client(self, client_id: str) -> None:
        """Asynchronously delete a client by its ID."""
        pass
