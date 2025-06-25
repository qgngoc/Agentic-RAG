
from core.ports.secondary.services import GetRetrieveToolsService, EmbeddingService, RetrieveService

from core.entities import Client, RagConfig, Tool, SearchQueryWithVector, Document

    
class GetRetrieveToolsServiceImpl(GetRetrieveToolsService):
    """Service implementation for retrieving tools for a client."""
    def __init__(self):
        pass

    def get_retrieve_tools(self, embedding_service: EmbeddingService, retrieve_service: RetrieveService, client: Client, rag_config: RagConfig) -> list[Tool]:
        """Retrieve tools for a client based on the provided RAG configuration."""
        def search_local_knowledge_base(query: str) -> list[Document]:
            """Search the local knowledge base to get the most relevant information to the query."""
            try:
                
                vector = embedding_service.create_embedding(query)
                response = retrieve_service.retrieve(
                    search_query=SearchQueryWithVector(
                        vector=vector,
                        text=query
                    ),
                    client=client,
                    limit=rag_config.top_k
                )
                return response
            except Exception as e:
                import logging
                logging.exception("Error retrieving documents from local knowledge base")
                return f"Error retrieving documents: {e}"
                
        tool = Tool(
            name="search_local_knowledge_base",
            description="Search the local knowledge base to get the most relevant information to the query.",
            arguments={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The query to search for in the local knowledge base."
                    }
                },
                "required": ["query"],
                "additionalProperties": False
            },
            function=search_local_knowledge_base
        )
        
        return [tool]
        

    async def aget_retrieve_tools(self, embedding_service: EmbeddingService, retrieve_service: RetrieveService, client: Client, rag_config: RagConfig) -> list[Tool]:
        """Asynchronously retrieve tools for a client based on the provided RAG configuration."""
        # This is a placeholder implementation. Replace with actual asynchronous logic to retrieve tools.
        return self.get_retrieve_tools(embedding_service, retrieve_service, client, rag_config)  # Simulating async behavior