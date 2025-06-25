import os

import mysql.connector
import qdrant_client
from dependency_injector import containers, providers


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    # Configure database clients
    mysql_connection_params = providers.Dict(
        host=config.mysql.host,
        port=config.mysql.port,
        user=config.mysql.user,
        password=config.mysql.password,
        database=config.mysql.database,
    )

    qdrant_client = providers.Singleton(
        qdrant_client.QdrantClient,
        url=config.qdrant.url,
        api_key=config.qdrant.api_key)

    # Configure repositories
    document_repository = providers.Singleton(
        MySQLDocumentRepository, connection_params=mysql_connection_params
    )

    vector_repository = providers.Singleton(
        QdrantVectorRepository,
        collection_name=config.qdrant.collection_name,
        qdrant_client=qdrant_client,
    )

    # Configure services
    embedding_service = providers.Singleton(
        OpenAIEmbedder,
        api_key=config.openai.api_key,
        model_name=config.openai.embedding_model,
    )

    # Configure use cases
    document_service = providers.Singleton(
        DocumentService,
        document_repository=document_repository,
        vector_repository=vector_repository,
        embedding_service=embedding_service,
    )

    search_service = providers.Singleton(
        SearchService,
        document_repository=document_repository,
        vector_repository=vector_repository,
        embedding_service=embedding_service,
    )


# Singleton for the container
_container = None


def get_container():
    global _container

    if _container is None:
        _container = Container()

        # Load configuration from environment or files
        _container.config.from_dict(
            {
                "mysql": {
                    "host": os.environ.get("MYSQL_HOST", "localhost"),
                    "port": int(os.environ.get("MYSQL_PORT", "3306")),
                    "user": os.environ.get("MYSQL_USER", "root"),
                    "password": os.environ.get("MYSQL_PASSWORD", ""),
                    "database": os.environ.get("MYSQL_DATABASE", "rag"),
                },
                "qdrant": {
                    "url": os.environ.get("QDRANT_URL", "http://localhost:6333"),
                    "api_key": os.environ.get("QDRANT_API_KEY", ""),
                    "collection_name": os.environ.get("QDRANT_COLLECTION", "documents"),
                },
                "openai": {
                    "api_key": os.environ.get("OPENAI_API_KEY", ""),
                    "embedding_model": os.environ.get(
                        "OPENAI_EMBEDDING_MODEL", "text-embedding-ada-002"
                    ),
                },
            }
        )

    return _container
