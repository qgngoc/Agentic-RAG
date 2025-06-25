from typing import Any, List, Optional

from pydantic import BaseModel, Field


class Message(BaseModel):
    """
    Represents a message in the system.
    """

    role: str = Field(...,
                      description="Role of the message sender (e.g., 'user', 'assistant')")
    content: Any = Field(..., description="Content of the message")
    tool_calls: Optional[List[Any]] = Field(
        None, description="List of tool calls associated with the message"
    )
