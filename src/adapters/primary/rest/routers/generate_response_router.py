
import os
import logging
from fastapi import APIRouter, Depends, HTTPException, Path
from fastapi.responses import JSONResponse

from adapters.primary.rest.schemas import RAGInputSchema, RAGOutputSchema
from core.ports.primary.generate_response import GenerateResponsePort

from infrastructure.di.container import generate_response_port

router = APIRouter(
    prefix="/generate_response",
    tags=["generate_response"]
)


def get_generate_response_port() -> GenerateResponsePort:
    """Dependency to provide the GenerateResponsePort."""
    return generate_response_port


@router.post("/generate_response")
async def generate_response(
    rag_input: RAGInputSchema,
    generate_response_port: GenerateResponsePort = Depends(get_generate_response_port)
):
    """
    Generate a response based on the input messages.

    Args:
        rag_input (RAGInputSchema): The input schema containing messages and client information.

    Returns:
        RAGOutputSchema: The output schema containing the generated response and citations.
    """
    try:
        rag_response = generate_response_port.generate_response(
            messages=rag_input.messages,
            client=rag_input.client,
            rag_config=rag_input.rag_config
        )
        rag_output = RAGOutputSchema(answer=rag_response.answer, citations=rag_response.citations)
        return JSONResponse(content=rag_output.model_dump(), status_code=200)
    except Exception as e:
        logging.exception(f"Error generating response: {e}")
        return JSONResponse(
            content={"error": str(e)},
            status_code=500
        )