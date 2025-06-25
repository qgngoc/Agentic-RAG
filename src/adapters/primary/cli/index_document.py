
import os
import logging
from fastapi import APIRouter, Depends, HTTPException, Path
from fastapi.responses import JSONResponse
from celery import chain


from adapters.primary.rest.celery_tasks.index_document_task import index_document_task
from adapters.primary.rest.schemas import IndexDocumentsInputSchema, IndexDocumentsOutputSchema, IndexDocumentsBackgroundInputSchema, IndexDocumentsBackgroundOutputSchema
from core.ports.primary.index_document import IndexDocumentPort

from infrastructure.di.container import index_document_port

router = APIRouter(
    prefix="/index_document",
    tags=["index_document"]
)

def get_index_document_port() -> IndexDocumentPort:
    """Dependency to provide the IndexDocumentPort."""
    return index_document_port

@router.post("/index_document")
async def index_document(input_data: IndexDocumentsInputSchema,
                         index_document_port: IndexDocumentPort = Depends(get_index_document_port)):
    """
    Index a document with its metadata.

    Args:
        input_data (IndexDocumentsInputSchema): The input schema containing client and input file information.

    Returns:
        IndexDocumentsOutputSchema: The output schema containing indexed documents with vectors.
    """
    try:
        # print(input_data.model_dump_json(indent=2))
        statuses = index_document_port.index_documents(
            client=input_data.client,
            input_files=input_data.input_files
        )
        return JSONResponse(content=IndexDocumentsOutputSchema(statuses=statuses).model_dump(), status_code=200)
    except Exception as e:
        logging.exception(f"Error indexing document: {e}")
        return JSONResponse(
            content={"error": str(e)},
            status_code=500
        )
    

@router.post("/index_document_background")
async def index_document_background(input_data: IndexDocumentsBackgroundInputSchema,
                         index_document_port: IndexDocumentPort = Depends(get_index_document_port)):
    """
    Index a document with its metadata.

    Args:
        input_data (IndexDocumentsBackgroundInputSchema): The input schema containing client and input file information.

    Returns:
        IndexDocumentsBackgroundOutputSchema: The output schema containing the task ID for the background indexing operation.
    """
    try:
        client = input_data.client
        input_files = input_data.input_files
        ids = input_data.ids
        assert len(ids) == len(input_files), "Number of IDs must match number of input files"
        
        for id, input_file in zip(ids, input_files):
            index_document_task.delay(id, client, input_file)
        
        return JSONResponse(
            content={"message": "Indexing started in the background", "task_ids": ids},
            status_code=200
        )
        
    except Exception as e:
        logging.exception(f"Error indexing document: {e}")
        return JSONResponse(
            content={"error": str(e)},
            status_code=500
        )