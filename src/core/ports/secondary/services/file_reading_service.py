from abc import ABC, abstractmethod
from typing import List

from core.entities import InputFile, FileContent, ReadFileConfig, PdfReadFileConfig, DocxReadFileConfig, PptxReadFileConfig, CsvReadFileConfig, XlsxReadFileConfig, MdReadFileConfig, TxtReadFileConfig

class FileReadingService(ABC):
    """Service interface for reading files."""

    @abstractmethod
    def read_file(self, input_file: InputFile, read_file_config: dict, **kwargs) -> FileContent:
        """Read the content of a file."""
        pass
    
    @abstractmethod
    async def aread_file(self, input_file: InputFile, read_file_config: dict, **kwargs) -> FileContent:
        """Asynchronously read the content of a file."""
        pass
    
class TxtFileReadingService(FileReadingService):
    @abstractmethod
    def read_file(self, input_file: InputFile, read_file_config: dict, **kwargs) -> FileContent:
        pass

    @abstractmethod
    async def aread_file(self, input_file: InputFile, read_file_config: dict, **kwargs) -> FileContent:
        """Asynchronously read the content of a text file."""
        pass

class PdfFileReadingService(FileReadingService):
    @abstractmethod
    def read_file(self, input_file: InputFile, read_file_config: dict, **kwargs) -> FileContent:
        pass
    
    @abstractmethod
    async def aread_file(self, input_file: InputFile, read_file_config: dict, **kwargs) -> FileContent:
        """Asynchronously read the content of a PDF file."""
        pass

class DocxFileReadingService(FileReadingService):
    @abstractmethod
    def read_file(self, input_file: InputFile, read_file_config: dict, **kwargs) -> FileContent:
        pass

    @abstractmethod
    async def aread_file(self, input_file: InputFile, read_file_config: dict, **kwargs) -> FileContent:
        """Asynchronously read the content of a DOCX file."""
        pass

class PptxFileReadingService(FileReadingService):
    @abstractmethod
    def read_file(self, input_file: InputFile, read_file_config: dict, **kwargs) -> FileContent:
        pass
    
    @abstractmethod
    async def aread_file(self, input_file: InputFile, read_file_config: dict, **kwargs) -> FileContent:
        """Asynchronously read the content of a PPTX file."""
        pass

class CsvFileReadingService(FileReadingService):
    @abstractmethod
    def read_file(self, input_file: InputFile, read_file_config: dict, **kwargs) -> FileContent:
        pass
    
    @abstractmethod
    async def aread_file(self, input_file: InputFile, read_file_config: dict, **kwargs) -> FileContent:
        """Asynchronously read the content of a CSV file."""
        pass

class XlsxFileReadingService(FileReadingService):
    @abstractmethod
    def read_file(self, input_file: InputFile, read_file_config: dict, **kwargs) -> FileContent:
        pass
    
    @abstractmethod
    async def aread_file(self, input_file: InputFile, read_file_config: dict, **kwargs) -> FileContent:
        """Asynchronously read the content of an XLSX file."""
        pass

class MdFileReadingService(FileReadingService):
    @abstractmethod
    def read_file(self, input_file: InputFile, read_file_config: dict, **kwargs) -> FileContent:
        pass

    @abstractmethod
    async def aread_file(self, input_file: InputFile, read_file_config: dict, **kwargs) -> FileContent:
        """Asynchronously read the content of a Markdown file."""
        pass
