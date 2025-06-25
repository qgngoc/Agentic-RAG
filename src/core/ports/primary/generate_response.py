from abc import ABC, abstractmethod
from typing import List


from core.entities import Message, RagConfig, Client, RagResponse

class GenerateResponsePort(ABC):
    """Use case for generating responses using LLMs."""

    @abstractmethod
    def generate_response(self, messages: list[Message], client: Client, rag_config: RagConfig) -> RagResponse:
        """
        Generate a response based on the input messages.
        Args:
            messages (list[Message]): The list of messages to process.
            client (Client): The client object containing client-specific information.
            rag_config (RagConfig): The configuration for the RAG system, including LLM configurations.
        Returns:
            RagResponse: The response object containing the generated output and status.
        """
        pass
    
    @abstractmethod
    async def agenerate_response(self, messages: list[Message], client: Client, rag_config: RagConfig) -> RagResponse:
        """
        Generate a response based on the input messages.

        Args:
            messages (list[Message]): The list of messages to process.
            client (Client): The client object containing client-specific information.
            rag_config (RagConfig): The configuration for the RAG system, including LLM configurations.

        Returns:
            RagResponse: The response object containing the generated output and status.
        """
        pass