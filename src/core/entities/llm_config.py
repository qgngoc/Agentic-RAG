from typing import List, Optional

from pydantic import BaseModel, Field


class LLMConfig(BaseModel):
    """LLM configuration model."""

    # key: Optional[str] = Field(None, description="LLM configuration key")
    model_path: Optional[str] = Field(
        "gpt-4.1-mini", description="Path to the LLM model"
    )
    base_url: Optional[str] = Field(
        None, description="Base URL for the LLM service")
    api_key: Optional[str] = Field(
        None, description="API key for the LLM service")
    temperature: Optional[float] = Field(
        0.01, description="Temperature for LLM responses"
    )
    # max_tokens: Optional[int] = Field(4096, description="Maximum number of tokens for LLM responses")
