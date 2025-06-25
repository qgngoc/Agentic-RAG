from typing import Any, Callable, Dict, List, Optional, Union

from pydantic import BaseModel, Field


class Tool(BaseModel):
    """Tool model representing a callable tool in the system."""

    name: str = Field(..., description="Name of the tool")
    description: str = Field(..., description="Description of the tool")
    arguments: Dict = Field(
        default_factory=dict,
        description="Parameters for the tool")
    function: Callable = Field(
        ..., description="Function to be called when the tool is invoked"
    )


class ToolCall(BaseModel):
    id: Optional[str] = Field(
        None, description="Unique identifier for the tool call")
    name: str = Field(..., description="Name of the tool called")
    arguments: Union[Dict, None] = Field(
        ..., description="Arguments passed to the tool"
    )


class ToolCallResponse(ToolCall):
    tool_response: Any = Field(
        None, description="Response from the tool called")
