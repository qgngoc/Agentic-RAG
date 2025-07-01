import asyncio
import requests
from typing import Union, List

from core.ports.primary.client_manage import ClientManagePort
from core.entities import Message, RagConfig, Client, RagResponse, ToolCall, Tool, ToolCallResponse, Document, DocumentWithVector, Citation

from core.ports.secondary.services import ClientManagingService

class ClientManageUseCaseImpl(ClientManagePort):
    """Use case for managing clients."""

    def __init__(self, client_managing_service: ClientManagingService):
        self.client_managing_service = client_managing_service

    def create_client(self, client: Client) -> Client:
        """Create a new client."""
        return self.client_managing_service.create_client(client)

    def delete_client(self, client_id: str) -> None:
        """Delete a client by its ID."""
        self.client_managing_service.delete_client(client_id)

    async def acreate_client(self, client: Client) -> Client:
        """Asynchronously create a new client."""
        return await self.client_managing_service.acreate_client(client)

    async def adelete_client(self, client_id: str) -> None:
        """Asynchronously delete a client by its ID."""
        await self.client_managing_service.adelete_client(client_id)
