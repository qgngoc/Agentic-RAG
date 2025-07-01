
from dotenv import load_dotenv
load_dotenv()

from celery import Celery
import os
import json
import logging
from fastapi import APIRouter, Depends, HTTPException, Path
from fastapi.responses import JSONResponse

from adapters.primary.rest.schemas import IndexDocumentsInputSchema, IndexDocumentsOutputSchema, IndexDocumentsBackgroundInputSchema, IndexDocumentsBackgroundOutputSchema
from core.ports.primary.index_document import IndexDocumentPort
from core.entities import InputFile, Client, IndexDocumentStatus

from infrastructure.di.container import index_document_port

# def get_index_document_port() -> IndexDocumentPort:
#     """Dependency to provide the IndexDocumentPort."""
#     return index_document_port

app = Celery(
    "aime-agenticrag",
    broker=os.getenv("CELERY_BROKER_URL"),
    backend=os.getenv("CELERY_RESULT_BACKEND")
)

@app.task(name="index_document_task")
def index_document_task(id: str, client: dict, input_file: dict) -> None:
    client = Client(**client)
    input_file = InputFile(**input_file)
    status = index_document_port.index_document(client, input_file)
    handle_callback(id, status)
    return
    
def handle_callback(id: str, status: IndexDocumentStatus):
    # TODO: handle callback
    logging.info(f"Document indexing task {id} completed with status: {status.status}")
    pass