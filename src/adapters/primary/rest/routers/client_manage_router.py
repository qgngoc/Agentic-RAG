
import os
import logging
from fastapi import APIRouter, Depends, HTTPException, Path
from fastapi.responses import JSONResponse

from adapters.primary.rest.schemas import CreateClientInputSchema, CreateClientOutputSchema, ClientDeleteOutputSchema
from core.ports.primary.client_manage import ClientManagePort

from infrastructure.di.container import client_manage_port

router = APIRouter(
    prefix="/client_manage",
    tags=["client_manage"]
)

def get_client_manage_port() -> ClientManagePort:
    """Dependency to provide the ClientManagePort."""
    return client_manage_port

@router.post("/create_client")
async def create_client(
    request: CreateClientInputSchema,
    client_manage_port: ClientManagePort = Depends(get_client_manage_port)
):
    """
    Create a new client.

    Args:
        client (RAGInputSchema): The input schema containing client information.

    Returns:
        RAGOutputSchema: The output schema containing the created client's information.
    """
    try:
        created_client = client_manage_port.create_client(request.client)
        output = CreateClientOutputSchema(client=created_client, status='success')
        return JSONResponse(content=output.model_dump(), status_code=200)
    except Exception as e:
        logging.exception(f"Error creating client: {e}")
        return JSONResponse(
            content={"error": str(e)},
            status_code=500
        )
        
@router.delete("/delete_client/{client_id}")
async def delete_client(
    client_id: str = Path(..., description="The ID of the client to be deleted"),
    client_manage_port: ClientManagePort = Depends(get_client_manage_port)
):
    """
    Delete a client by its ID.

    Args:
        client_id (str): The ID of the client to be deleted.

    Returns:
        ClientDeleteOutputSchema: The output schema containing the deletion status.
    """
    try:
        client_manage_port.delete_client(client_id)
        output = ClientDeleteOutputSchema(status='success')
        return JSONResponse(content=output.model_dump(), status_code=200)
    except Exception as e:
        logging.exception(f"Error deleting client: {e}")
        return JSONResponse(
            content={"error": str(e)},
            status_code=500
        )