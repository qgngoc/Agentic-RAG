


from core.ports.secondary.services import RetrieveService
from core.ports.secondary.repositories import VectorDBRepository
from core.entities import SearchQueryWithVector, Client, DocumentWithVector, Document

class SemanticRetrieveServiceImpl(RetrieveService):
    def __init__(self, vectordb_repository: VectorDBRepository):
        self.vectordb_repository = vectordb_repository
        
    def retrieve(self, search_query: SearchQueryWithVector, client: Client, limit: int = 10) -> list[DocumentWithVector]:
        """
        Retrieve documents based on a semantic query.

        Args:
            search_query (SearchQueryWithVector): The query object containing the vector and other parameters.
            client (Client): The client object containing client-specific information.
            limit (int): The maximum number of documents to retrieve.

        Returns:
            list[DocumentWithVector]: The list of retrieved documents.
        """
        return self.vectordb_repository.retrieve_documents(client=client, search_query=search_query, limit=limit)

    async def aretrieve(self, search_query: SearchQueryWithVector, client: Client, limit: int = 10) -> list[DocumentWithVector]:
        """
        Asynchronously retrieve documents based on a semantic query.

        Args:
            search_query (SearchQueryWithVector): The query object containing the vector and other parameters.
            client (Client): The client object containing client-specific information.
            limit (int): The maximum number of documents to retrieve.

        Returns:
            list[DocumentWithVector]: The list of retrieved documents.
        """
        return await self.vectordb_repository.aretrieve_documents(client=client, search_query=search_query, limit=limit)