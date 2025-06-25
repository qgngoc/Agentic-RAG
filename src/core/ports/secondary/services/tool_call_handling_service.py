
from abc import ABC, abstractmethod
from typing import List

from core.entities import ToolCall, ToolCallResponse, Tool

class ToolCallHandlingService(ABC):
    """Use case for handling tool calls."""

    @abstractmethod
    def handle_tool_calls(self, tool_calls: List[ToolCall], tools: List[Tool], parallel: bool = False) -> List[ToolCallResponse]:   
        """Handle multiple tool calls and return their responses."""
        pass