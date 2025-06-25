from typing import Dict, Any, Optional, BinaryIO, Literal

from pydantic import BaseModel, Field
import uuid
import os


class PageContent(BaseModel):
    content: str = Field(..., description="Content of the page")
    page_number: int = Field(..., description="Page number in the document, starts with 1")

class FileContent(BaseModel):
    """File content model representing the content of a file."""
    
    id: Optional[str] = Field(None, description="File unique identifier")
    file_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="File unique identifier")
    file_name: str = Field(..., description="File name")
    file_path: Optional[str] = Field(None, description="Path to the file on disk")
    page_contents: list[PageContent] = Field([], description="List of page contents in the file")
    content_format: str = Field(..., description="Format of the file content (e.g., text, markdown)")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="File metadata")
    created_at: Optional[int] = Field(None, description="File creation timestamp")
    updated_at: Optional[int] = Field(None, description="File last update timestamp")