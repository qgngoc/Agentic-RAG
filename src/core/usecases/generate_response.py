import asyncio
import requests
from typing import Union, List

from core.ports.primary.generate_response import GenerateResponsePort
from core.entities import Message, RagConfig, Client, RagResponse, ToolCall, Tool, ToolCallResponse, Document, DocumentWithVector, Citation

from core.ports.secondary.services import LLMService, EmbeddingService, GetRetrieveToolsService, GetCitationsService, ToolCallHandlingService, RetrieveService

class GenerateResponseUseCaseImpl(GenerateResponsePort):
    """Implementation of the use case for generating responses using LLMs."""

    def __init__(self, llm_service: LLMService, embedding_service: EmbeddingService, retrieval_service: RetrieveService, get_retrieve_tools_service: GetRetrieveToolsService, get_citations_service: GetCitationsService, tool_call_handling_service: ToolCallHandlingService):
        """ Initialize the GenerateResponseUseCaseImpl with necessary services."""
        self.llm_service = llm_service
        self.embedding_service = embedding_service
        self.retrieval_service = retrieval_service
        self.get_retrieve_tools_service = get_retrieve_tools_service
        self.get_citations_service = get_citations_service
        self.tool_call_handling_service = tool_call_handling_service
        self.max_iterations = 3  # Maximum number of iterations for the RAG process
        
        
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
        retrieve_tools = self.get_retrieve_tools_service.get_retrieve_tools(self.embedding_service, self.retrieval_service, client, rag_config)
        retrieved_documents = []
        for i in range(self.max_iterations):
            llm_completion = self.llm_service.chat(llm_config=rag_config.llm_config, messages=messages, tools=retrieve_tools)
            tool_calls = llm_completion.tool_calls
            text = llm_completion.text
            if not tool_calls:
                break  # Exit if no tool calls are made
            tool_call_responses, documents = self._handle_retrieve_tool_calls(tool_calls, retrieve_tools)
            retrieved_documents.extend(documents)
            messages.append(Message(role='assistant', content=text, tool_calls=tool_calls))
            for tool_call_response in tool_call_responses:
                messages.append(Message(role='tool', content=tool_call_response))
        citations = self.get_citations_service.get_citations(retrieved_documents)

        rag_response = RagResponse(
            answer=text,
            citations=citations,
        )
        return rag_response

    async def agenerate_response(self, messages: list[Message], client: Client, rag_config: RagConfig) -> RagResponse:
        """
        Asynchronously generate a response based on the input messages.

        Args:
            messages (list[Message]): The list of messages to process.
            client (Client): The client object containing client-specific information.
            rag_config (RagConfig): The configuration for the RAG system, including LLM configurations.

        Returns:
            RagResponse: The response object containing the generated output and status.
        """
        # Simulate an asynchronous call to an external service
        pass

    def _handle_retrieve_tool_calls(self, tool_calls: list[ToolCall], tools: list[Tool]) -> tuple[list[ToolCallResponse], list[Document]]:
        """
        Handle tool calls and return their responses.

        Args:
            tool_calls (list[ToolCall]): List of tool calls to be handled.

        Returns:
            list[ToolCallResponse]: List of responses from the tool calls.
        """
        tool_call_responses = self.tool_call_handling_service.handle_tool_calls(tool_calls, tools)
        documents = []
        for i in range(len(tool_call_responses)):
            tool_response = tool_call_responses[i].tool_response
            if isinstance(tool_response, list):
                
                documents.extend(tool_response)
                relevant_docs = '\n\n'.join([doc.content for doc in tool_response if isinstance(doc, Document)])
                tool_call_responses[i].tool_response = relevant_docs
        return tool_call_responses, documents