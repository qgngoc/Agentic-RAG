import json
from typing import List
from openai import OpenAI

from core.entities import LLMConfig, Message, Tool, ToolCall, LLMCompletion
from core.ports.secondary.services.llm_service import LLMService

class OpenAILLMServiceImpl(LLMService):
    """Implementation of the LLMService interface for OpenAI."""

    def __init__(self, client: OpenAI = OpenAI(), llm_config_mapping: dict[str, LLMConfig] = {}):
        self.client = client
        self.llm_config_mapping = llm_config_mapping


    def chat(self, llm_config: LLMConfig, messages: List[Message], tools: List[Tool] = None) -> LLMCompletion:
        """
        Perform a chat operation using OpenAI's API.

        Args:
            messages (List[Message]): List of messages to send to the LLM.
            tools (List[Tool], optional): List of tools to use during the chat. Defaults to None.

        Returns:
            LLMCompletion: The response from the LLM.
        """
        # Implementation for OpenAI's chat API call
        if llm_config.api_key or llm_config.base_url:
            self.client.api_key = llm_config.api_key
            self.client.base_url = llm_config.base_url
            
        openai_tools = self._build_tools(tools) if tools else []
        openai_messages = self.build_messages(messages)
        try:
            completion = self.client.chat.completions.create(
                model=llm_config.model_path,
                messages=openai_messages,
                tools=openai_tools,
                temperature=llm_config.temperature
            )
            text = completion.choices[0].message.content
            openai_tool_calls = completion.choices[0].message.tool_calls
            openai_tool_calls = openai_tool_calls if openai_tool_calls else []
            tool_calls = []
            for openai_tool_call in openai_tool_calls:
                arguments = json.loads(openai_tool_call.function.arguments)
                tool_call = ToolCall(
                    id=openai_tool_call.id,
                    name=openai_tool_call.function.name,
                    arguments=arguments
                )
                tool_calls.append(tool_call)
            
            return LLMCompletion(
                text=text,
                tool_calls=tool_calls
            )
        except Exception as e:
            raise Exception(f"Error during OpenAI chat completion: {str(e)}")
   
   
    def get_llm_config_keys(self) -> List[str]:
        """Get the keys of all LLM configurations."""
        return list(self.llm_config_mapping.keys())
    
    def get_llm_config(self, key: str) -> LLMConfig:
        """Retrieve a specific LLM configuration by its key."""
        try:
            return self.llm_config_mapping[key]
        except KeyError:
            raise ValueError(f"LLM configuration with key '{key}' not found.")
        
    def add_llm_config(self, key: str, llm_config: LLMConfig) -> None:
        """Add a new LLM configuration."""
        if key in self.llm_config_mapping:
            raise ValueError(f"LLM configuration with key '{key}' already exists.")
        self.llm_config_mapping[key] = llm_config
        
    
    async def achat(self, llm_config: LLMConfig, messages: List[Message], tools: List[Tool] = None) -> LLMCompletion:
        """
        Asynchronously perform a chat operation using OpenAI's API.

        Args:
            messages (List[Message]): List of messages to send to the LLM.
            tools (List[Tool], optional): List of tools to use during the chat. Defaults to None.

        Returns:
            LLMCompletion: The response from the LLM.
        """
        # TODO: Implement asynchronous chat operation
        raise NotImplementedError("Asynchronous chat operation is not implemented yet.")
    
    async def aget_llm_config_keys(self) -> List[str]:
        """Asynchronously retrieve a list of LLM configuration keys."""
        # For simplicity, we can just call the synchronous method here.
        # In a real implementation, this might involve an async database call or similar.
        return self.get_llm_config_keys()
    
    
    async def aget_llm_config(self, key: str) -> LLMConfig:
        """Asynchronously retrieve a specific LLM configuration by its key."""
        # For simplicity, we can just call the synchronous method here.
        # In a real implementation, this might involve an async database call or similar.
        return self.get_llm_config(key)
    
    async def aadd_llm_config(self, key: str, llm_config: LLMConfig) -> None:
        """Asynchronously add a new LLM configuration."""
        # For simplicity, we can just call the synchronous method here.
        # In a real implementation, this might involve an async database call or similar.
        self.add_llm_config(key, llm_config)
        
    def build_messages(self, messages: List[Message]) -> List[dict]:
        """
        Build the messages for the OpenAI API.

        Args:
            messages (List[Message]): List of messages to build.

        Returns:
            List[dict]: List of dictionaries representing the messages.
        """
        openai_messages = []
        for message in messages:
            if message.role == "tool":
                tool_response = message.content.tool_response
                tool_call_id = message.content.id
                openai_message = {
                    "role": "tool",
                    "content": tool_response,
                    "tool_call_id": tool_call_id
                }
            else:
                openai_message = {
                    "role": message.role,
                    "content": message.content
                }
            if message.tool_calls:
                openai_message["tool_calls"] = []
                for tool_call in message.tool_calls:
                    tool_call_dict = {
                        "id": tool_call.id,
                        "function": {
                            "arguments": json.dumps(tool_call.arguments, ensure_ascii=False),
                            "name": tool_call.name,
                        },
                        "type": "function"
                    }
                    openai_message["tool_calls"].append(tool_call_dict)
            
            openai_messages.append(openai_message)
        return openai_messages
    
    def _build_tools(self, tools: List[Tool]) -> List[dict]:
        """
        Build the tools for the OpenAI API.

        Args:
            tools (List[Tool]): List of tools to build.

        Returns:
            List[dict]: List of dictionaries representing the tools.
        """
        openai_tools = []
        for tool in tools:
            openai_tool = {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.arguments,
                    "strict": True
                }
            }
            openai_tools.append(openai_tool)
        return openai_tools
    