from typing import Dict, Any, Optional, BinaryIO, Literal

from pydantic import BaseModel, Field
import uuid
import os

class IndexDocumentStatus(BaseModel):
    """Status of the document indexing process."""
    file_path: str = Field(..., description="Path to the file being indexed")
    file_name: Optional[str] = Field(None, description="Name of the file being indexed")
    status: Literal["pending", "in_progress", "completed", "failed"] = Field(
        "in_progress", description="Current status of the indexing process"
    )