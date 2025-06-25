from typing import Dict, List, Optional, Union
from pydantic import BaseModel, Field


class SearchQuery(BaseModel):
    """User query model."""
    id: Optional[str] = Field(None, description="Query unique identifier")
    text: str = Field(..., description="Query text")
    metadata: Optional[dict] = Field(
        None, description="Query metadata"
    )

class SearchQueryWithVector(SearchQuery):
    """User query model with vector representation."""
    vector: List[float] = Field(..., description="Vector representation of the query")