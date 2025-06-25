
from typing import Dict, List, Optional, Union
from pydantic import BaseModel, Field

from .citation import Citation

class RagResponse(BaseModel):
    """RAG response model."""

    id: Optional[str] = Field(None, description="RAG unique identifier")
    answer: str = Field(..., description="The generated answer from the RAG operation.")
    citations: Optional[List[Citation]] = Field(
        None, 
        description="List of citations used to generate the answer. Each citation includes file name, path, page number, and content."
    )
    flag: Optional[int] = Field(0, description="Flag indicating the status of the RAG operation. 0 for success, 1 for no answer found, 2 for error.")