from typing import Dict, List, Optional, Union

from pydantic import BaseModel, Field

from core.entities.tool import ToolCall


class LLMCompletion(BaseModel):
    text: Union[str, None] = Field(...,
                                   description="Text of the LLM completion")
    tool_calls: Union[List[ToolCall], None] = Field(
        None, description="List of tool calls made during the completion"
    )
