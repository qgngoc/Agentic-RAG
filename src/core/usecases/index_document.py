
from typing import List

from core.entities import Document, DocumentWithVector, InputFile, Client, FileContent, IndexDocumentStatus
from core.ports.primary.index_document import IndexDocumentPort

from core.ports.secondary.repositories import VectorDBRepository
from core.ports.secondary.services import EmbeddingService, FileReadingService, ChunkingService

class IndexDocumentUseCaseImpl(IndexDocumentPort):
    def __init__(self, vectordb: VectorDBRepository, embedding_service: EmbeddingService, file_reading_services_mapping: dict[str, FileReadingService] = {}, chunking_services_mapping: dict[str, ChunkingService] = {}):
        self.vectordb = vectordb
        self.embedding_service = embedding_service
        self.file_reading_services_mapping = file_reading_services_mapping
        self.chunking_services_mapping = chunking_services_mapping

    
    def index_document(self, client: Client, input_file: InputFile) -> IndexDocumentStatus:
        """Index a document with its metadata."""
        try:
            file_reading_service = self.get_file_reading_service(input_file)
            # read_file_config = input_file.read_file_config
            file_content = file_reading_service.read_file(input_file, input_file.read_file_config)
            # print(input_file.read_file_config)
            chunking_service = self.get_chunking_service(file_content)
            documents = chunking_service.chunk(file_content)
            
            indexed_documents = []
            for document in documents:
                vector = self.embedding_service.create_embedding(text=document.content)
                document_dict = document.model_dump()
                document_dict['vector'] = vector
                document_with_vector = DocumentWithVector(**document_dict)
                indexed_documents.append(document_with_vector)

            self.vectordb.insert_documents(client, indexed_documents)
            status = IndexDocumentStatus(
                file_path=input_file.local_file_path,
                status="completed",
                documents=indexed_documents
            )
        except Exception as e:
            status = IndexDocumentStatus(
                file_path=input_file.local_file_path,
                status="failed"
            )
                
            
        return status

    def index_documents(self, client: Client, input_files: List[InputFile]) -> List[IndexDocumentStatus]:
        """Index multiple documents with their metadata."""
        statuses = []
        for input_file in input_files:
            statuses.append(self.index_document(client, input_file))
        return statuses
    
    async def aindex_document(self, client: Client, input_file: InputFile) -> IndexDocumentStatus:
        # TODO: Implement asynchronous indexing of a single document
        pass
    
    async def aindex_documents(self, client: Client, input_files: List[InputFile]) -> List[IndexDocumentStatus]:
        # TODO: Implement asynchronous indexing of multiple documents
        pass
    
    def add_file_reading_service(self, key: str, service: FileReadingService):
        """Add a file reading service for a specific file type."""
        self.file_reading_services_mapping[key] = service
        
    def add_chunking_service(self, key: str, service: ChunkingService):
        """Add a chunking service for a specific file type."""
        self.chunking_services_mapping[key] = service
        
    def get_file_reading_service(self, file: InputFile) -> FileReadingService:
        """Get the appropriate file reading service based on the file type."""
        file_extension = file.local_file_path.split('.')[-1].lower()
        try:
            return self.file_reading_services_mapping[file_extension]
        except KeyError:
            raise ValueError(f"Unsupported file type: {file_extension}")
    
    def get_chunking_service(self, file_content: FileContent) -> ChunkingService:
        """Get the appropriate chunking service based on the file content format."""
        content_format = file_content.content_format.lower()
        try:
            return self.chunking_services_mapping[content_format]
        except KeyError:
            raise ValueError(f"Unsupported content format: {content_format}")
        
        
        