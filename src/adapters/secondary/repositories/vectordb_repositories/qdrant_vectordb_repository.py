import logging
from typing import Any, Dict, List, Optional, Union

from qdrant_client import QdrantClient
from qdrant_client.http.models import (
    FieldCondition,
    Filter,
    PointStruct,
    Range,
    SearchRequest,
)
from qdrant_client.models import Distance

from core.ports.secondary.repositories import VectorDBRepository
from core.ports.secondary.services.embedding_service import EmbeddingService
from core.entities import DocumentWithVector, Client, SearchQueryWithVector

logger = logging.getLogger(__name__)


class QdrantVectorDBRepositoryImpl(VectorDBRepository):
    """Qdrant implementation of the VectorRepository interface."""

    def __init__(
        self,
        embedding_service: EmbeddingService,
        qdrant_client: QdrantClient,
        collection_name: str,
    ):
        self.embedding_service = embedding_service
        self.qdrant_client = qdrant_client
        self.collection_name = collection_name

    def _check_collection_exists(self, collection_id: str) -> bool:
        """Check if the collection exists in Qdrant."""
        try:
            exists = self.qdrant_client.collection_exists(collection_id)
            return exists
        except Exception as e:
            logger.error(f"Error checking collection existence: {e}")
            return False

    def _create_collection(self, collection_id: str) -> bool:
        """Create a collection in Qdrant if it doesn't exist."""
        try:
            if self._check_collection_exists(collection_id):
                logger.info(
                    f"Collection {collection_id} already exists.")
                return True
            vector_dimensions = self.embedding_service.get_embedding_dimension()
            self.qdrant_client.recreate_collection(
                collection_name=collection_id,
                vectors_config={
                    "size": vector_dimensions,
                    "distance": Distance.COSINE,  # Distance metric
                },
            )
            return True
        except Exception as e:
            raise Exception(f"Error creating collection: {e}")

    def create_collection(self, client: Client) -> bool:
        return self._create_collection(f"{self.collection_name}_{client.id}")
    
    def delete_collection(self, client_id: str) -> bool:
        """Delete a collection from the vector database."""
        try:
            collection_id = f"{self.collection_name}_{client_id}"
            if not self._check_collection_exists(collection_id):
                logger.info(f"Collection {collection_id} does not exist.")
                return False
            self.qdrant_client.delete_collection(collection_name=collection_id)
            return True
        except Exception as e:
            raise Exception(f"Error deleting collection: {e}")
    
    def insert_document(
        self, client: Client, document: DocumentWithVector
    ) -> DocumentWithVector:
        """Save a document with its vector representation."""
        try:
            collection_id = f"{self.collection_name}_{client.id}"
            # Ensure the collection exists
            self._create_collection(collection_id)

            # Upsert the document into Qdrant
            point = PointStruct(
                id=document.id,
                vector=document.vector,
                payload=self._build_payload(document, client),
            )
            self.qdrant_client.upsert(
                collection_name=collection_id, points=[point]
            )
            return document
        except Exception as e:
            # logger.error(f"Error inserting document: {e}")
            raise e
    
    
    def insert_documents(
        self, client: Client, documents: List[DocumentWithVector]
    ) -> List[DocumentWithVector]:
        """Insert multiple documents into the vector database."""
        try:
            collection_id = f"{self.collection_name}_{client.id}"
            # Ensure the collection exists
            self._create_collection(collection_id)

            points = [
                PointStruct(
                    id=document.id,
                    vector=document.vector,
                    payload=self._build_payload(document, client),
                )
                for document in documents
            ]
            self.qdrant_client.upsert(
                collection_name=collection_id, points=points
            )
            return documents
        except Exception as e:
            raise e
    
    def retrieve_documents(
        self, client: Client, search_query: SearchQueryWithVector, limit: int = 20
    ) -> List[DocumentWithVector]:
        """Find documents by their vector representation."""
        try:
            collection_id = f"{self.collection_name}_{client.id}"
            response = self.qdrant_client.query_points(
                collection_name=collection_id,
                query=search_query.vector,
                limit=limit,
                query_filter=Filter(
                    must=[
                        FieldCondition(
                            key="client_id",
                            match={
                                "value": client.id})]),
                with_payload=True,
                with_vectors=True,
            )
            # results = [p for p in response.points]
            results = [p for p in response.points]
            documents = [
                DocumentWithVector(
                    content=p.payload["content"],
                    vector=p.vector,
                    file_name=p.payload["file_name"],
                    file_path=p.payload["file_path"],
                    page_number=p.payload["page_number"],
                )
                for p in results
            ]
            return documents
        except Exception as e:
            raise e

    async def ainsert_document(
        self, client: Client, document: DocumentWithVector
    ) -> DocumentWithVector:
        """Asynchronously save a document with its vector representation."""
        # TODO: Implement asynchronous insertion
        raise NotImplementedError(
            "Asynchronous insert is not implemented for QdrantVectorDBRepository."
        )
        
    async def ainsert_documents(
        self, client: Client, documents: List[DocumentWithVector]
    ) -> List[DocumentWithVector]:
        """Asynchronously insert multiple documents into the vector database."""
        # TODO: Implement asynchronous insertion
        raise NotImplementedError(
            "Asynchronous insert is not implemented for QdrantVectorDBRepository."
        )
        
    async def aretrieve_documents(
        self, client: Client, search_query: SearchQueryWithVector, limit: int = 20
    ) -> List[DocumentWithVector]:
        """Asynchronously find documents by their vector representation."""
        # TODO: Implement asynchronous retrieval
        raise NotImplementedError(
            "Asynchronous retrieval is not implemented for QdrantVectorDBRepository."
        )
        
    async def acreate_collection(self, client: Client) -> bool:
        """Asynchronously create a collection in the vector database."""
        # TODO: Implement asynchronous collection creation
        raise NotImplementedError(
            "Asynchronous collection creation is not implemented for QdrantVectorDBRepository."
        )
        
    async def adelete_collection(self, client_id: str) -> bool:
        """Asynchronously delete a collection from the vector database."""
        # TODO: Implement asynchronous collection deletion
        raise NotImplementedError(
            "Asynchronous collection deletion is not implemented for QdrantVectorDBRepository."
        )
    
    def _build_payload(self, document: DocumentWithVector,
                       client: Client) -> Dict[str, Any]:
        """Build the payload for Qdrant."""
        return {
            "id": document.id,
            "content": document.content,
            "file_name": document.file_name,
            "file_path": document.file_path,
            "page_number": document.page_number,
            # "metadata": document.metadata,
            "client_id": client.id,
        }
