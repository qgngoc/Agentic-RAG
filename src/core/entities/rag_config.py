from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Union, Callable
from .llm_config import LLMConfig

class RagConfig(BaseModel):
    """RAG configuration model."""

    llm_config: LLMConfig = Field(..., description="LLM configuration for RAG")
    top_k: Optional[int] = Field(5, description="Number of top documents to retrieve")