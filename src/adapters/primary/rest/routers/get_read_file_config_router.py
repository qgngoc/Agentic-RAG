
import logging
import os

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from core.ports.primary.get_read_file_config import GetReadFileConfigPort

from infrastructure.di.container import get_read_file_config_port

router = APIRouter(
    prefix="/get_read_file_config",
    tags=["get_read_file_config"])


def get_get_read_file_config_port() -> GetReadFileConfigPort:
    """
    Dependency to get the GetReadFileConfigPort instance.
    This can be replaced with a more complex dependency injection mechanism if needed.
    """
    return get_read_file_config_port

@router.get("/get_read_file_config")
async def get_read_file_config(
    key: str,
    get_read_file_config_port: GetReadFileConfigPort = Depends(get_get_read_file_config_port)
):
    """
    Retrieve a specific read file configuration by its key.

    Args:
        key (str): The key of the read file configuration to retrieve.

    Returns:
        ReadFileConfig: The read file configuration corresponding to the provided key.
    """
    try:
        read_file_config = get_read_file_config_port.get_read_file_config(key)
        return JSONResponse(content=read_file_config.model_dump(), status_code=200)
    except KeyError as e:
        logging.exception(f"Read file config with key '{key}' not found: {e}")
        raise HTTPException(status_code=404, detail=str(e))