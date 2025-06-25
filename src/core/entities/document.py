
from typing import Dict, List, Optional, Union
from pydantic import BaseModel, Field


class Document(BaseModel):
    """Base document model for RAG system."""
    id: Optional[str] = Field(None, description="Document unique identifier")
    content: str = Field(..., description="Document content")
    metadata: Union[Dict, None] = Field(
        None, description="Document metadata"
    )
    file_name: str = Field(None, description="Name of the file associated with the document")
    file_path: str = Field(None, description="Path to the file associated with the document")
    page_number: int = Field(None, description="Page number of the document")
    # source: Optional[str] = Field(None, description="Document source")
    created_at: Optional[int] = Field(None, description="Document creation timestamp")
    updated_at: Optional[int] = Field(None, description="Document last update timestamp")
    
class DocumentWithVector(Document):
    """Document model with vector representation."""
    vector: List[float] = Field(..., description="Vector representation of the document")
    