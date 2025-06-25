
import os
import logging
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from adapters.primary.rest.schemas import RAGInputSchema, RAGOutputSchema
from core.ports.primary.get_llm_configs import GetLLMConfigsPort

from infrastructure.di.container import openai_llm_service

router = APIRouter(
    prefix="/get_llm_configs",
    tags=["get_llm_configs"]
)

def get_get_llm_configs_port() -> GetLLMConfigsPort:
    """Dependency to provide the GetLLMConfigsPort."""
    return openai_llm_service

@router.get("/get_llm_config_keys")
async def get_llm_config_keys(
    get_llm_configs_port: GetLLMConfigsPort = Depends(get_get_llm_configs_port)
):
    """
    Retrieve a list of LLM configuration keys.

    Returns:
        List[str]: A list of LLM configuration keys.
    """
    try:
        llm_config_keys = get_llm_configs_port.get_llm_config_keys()
        return JSONResponse(content=llm_config_keys, status_code=200)
    except Exception as e:
        logging.exception(f"Error retrieving LLM config keys: {e}")
        return JSONResponse(
            content={"error": str(e)},
            status_code=500
        )

@router.get("/get_llm_config")
async def get_llm_config(
    key: str,
    get_llm_configs_port: GetLLMConfigsPort = Depends(get_get_llm_configs_port)
):
    """
    Retrieve a specific LLM configuration by its key.

    Args:
        key (str): The key of the LLM configuration to retrieve.

    Returns:
        LLMConfig: The LLM configuration corresponding to the provided key.
    """
    try:
        llm_config = get_llm_configs_port.get_llm_config(key)
        return JSONResponse(content=llm_config.model_dump(), status_code=200)
    except Exception as e:
        logging.exception(f"Error retrieving LLM config for key {key}: {e}")
        return JSONResponse(
            content={"error": str(e)},
            status_code=500
        )