
from abc import ABC, abstractmethod

from core.entities import Client

from core.ports.secondary.services import ClientManagingService
from core.ports.secondary.repositories import VectorDBRepository

class ClientManagingServiceImpl(ClientManagingService):
    """Implementation of the ClientManagingService interface."""

    def __init__(self, vector_db_repository: VectorDBRepository):
        self.vector_db_repository = vector_db_repository

    def create_client(self, client: Client) -> Client:
        """Create a new client."""
        if self.vector_db_repository.create_collection(client):
            return client
        else:
            raise Exception(f"Failed to create client collection for {client.id}")

    def delete_client(self, client_id: str) -> None:
        """Delete a client by its ID."""
        self.vector_db_repository.delete_collection(client_id)

    async def acreate_client(self, client: Client) -> Client:
        """Asynchronously create a new client."""
        return await self.vector_db_repository.acreate_collection(client)

    async def adelete_client(self, client_id: str) -> None:
        """Asynchronously delete a client by its ID."""
        await self.vector_db_repository.adelete_collection(client_id)