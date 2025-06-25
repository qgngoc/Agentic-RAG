
from core.entities import ReadFileConfig
from core.ports.primary.get_read_file_config import GetReadFileConfigPort


class GetReadFileConfigUseCaseImpl(GetReadFileConfigPort):
    def __init__(self, read_file_config_mapping: dict[str, ReadFileConfig] = {}):
        self.read_file_config_mapping = read_file_config_mapping
        
    def get_read_file_config(self, key: str) -> ReadFileConfig:
        """Retrieve a specific read file configuration by its key."""
        if key not in self.read_file_config_mapping:
            raise KeyError(f"Read file config with key '{key}' not found.")
        return self.read_file_config_mapping[key]
    
    async def aget_read_file_config(self, key: str) -> ReadFileConfig:
        """Asynchronously retrieve a specific read file configuration by its key."""
        # For simplicity, we can just call the synchronous method here.
        # In a real implementation, this might involve an async database call or similar.
        return self.get_read_file_config(key)
    
    def add_read_file_config(self, key: str, read_file_config: ReadFileConfig) -> None:
        """Add a new read file configuration."""
        if key in self.read_file_config_mapping:
            raise KeyError(f"Read file config with key '{key}' already exists.")
        self.read_file_config_mapping[key] = read_file_config
        