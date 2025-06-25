
from typing import List

from core.ports.secondary.services import ToolCallHandlingService
from core.entities import ToolCall, ToolCallResponse, Tool

class ToolCallHandlingServiceImpl(ToolCallHandlingService):
    """Service implementation for handling tool calls."""
    
    def __init__(self):
        pass

    def handle_tool_calls(self, tool_calls: List[ToolCall], tools: List[Tool], parallel: bool = False) -> List[ToolCallResponse]:
        """Handle multiple tool calls and return their responses."""
        tool_call_responses = []
        tool_mapping = {tool.name: tool.function for tool in tools}
        for tool_call in tool_calls:
            tool_name = tool_call.name
            if tool_name in tool_mapping:
                try:
                    tool_response = tool_mapping[tool_name](**tool_call.arguments)

                    tool_call_responses.append(
                        ToolCallResponse(
                            id=tool_call.id,
                            name=tool_name,
                            arguments=tool_call.arguments,
                            tool_response=tool_response
                        )
                    )
                except Exception as e:
                    tool_call_responses.append(
                        ToolCallResponse(
                            id=tool_call.id,
                            name=tool_name,
                            arguments=tool_call.arguments,
                            tool_response=f"Error: {str(e)}"
                        )
                    )
        return tool_call_responses

    async def ahandle_tool_calls(self, tool_calls: List[ToolCall], tools: List[Tool], parallel: bool = False) -> List[ToolCallResponse]:
        """Asynchronously handle multiple tool calls and return their responses."""
        # TODO: Implement actual asynchronous handling of tool calls.
        return self.handle_tool_calls(tool_calls, tools, parallel)