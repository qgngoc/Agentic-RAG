from datetime import datetime
from typing import Dict, List, Optional, Union

from pydantic import BaseModel, Field

from core.entities import Citation, Client, Message, RagConfig, InputFile, Document, IndexDocumentStatus

class RAGInputSchema(BaseModel):
    messages: list[Message] = Field(..., description="List of messages for the RAG operation.")  
    client: Client = Field(..., description="Client information for the RAG operation.")
    rag_config: RagConfig = Field(..., description="Configuration for the RAG operation, including LLM configurations.")


class RAGOutputSchema(BaseModel):
    """Schema for the output of a RAG operation."""
    answer: str = Field(..., description="The generated answer from the RAG operation.")
    citations: Optional[List[Citation]] = Field(
        None, 
        description="List of citations used to generate the answer. Each citation includes file name, path, page number, and content."
    )
    flag: int = Field(0, description="Flag indicating the status of the RAG operation. 0 for success, 1 for no answer found, 2 for error.")


class IndexDocumentsInputSchema(BaseModel):
    """Schema for indexing documents."""
    client: Client = Field(..., description="Client information for indexing documents.")
    input_files: List[InputFile] = Field(
        ...,
        description="List of input files to be indexed. Each file contains metadata and reading configurations."
    )   
    
class IndexDocumentsOutputSchema(BaseModel):
    statuses: List[IndexDocumentStatus] = Field(
        ...,
        description="List of statuses for each indexed document. Each status includes file path, file name, and indexing status."
    )


class IndexDocumentsBackgroundInputSchema(BaseModel):
    """Schema for indexing documents."""
    client: Client = Field(..., description="Client information for indexing documents.")
    input_files: List[InputFile] = Field(
        ...,
        description="List of input files to be indexed. Each file contains metadata and reading configurations."
    )
    ids: list[str] = Field(
        ...,
        description="List of IDs for the background task. Used to track the indexing process."
    )

class IndexDocumentsBackgroundOutputSchema(BaseModel):
    task_id: str = Field(
        ...,
        description="ID of the background task for indexing documents."
    )
    statuses: List[IndexDocumentStatus] = Field(
        ...,
        description="List of statuses for each indexed document. Each status includes file path, file name, and indexing status."
    )

