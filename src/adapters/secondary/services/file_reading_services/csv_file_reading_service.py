import pathlib
from langchain_community.document_loaders.csv_loader import CSVLoader

from core.ports.secondary.services import CsvFileReadingService
from core.entities import InputFile, FileContent, PageContent, CsvReadFileConfig

class CSVFileReadingServiceImpl(CsvFileReadingService):
    """Service implementation for reading CSV files."""
    def __init__(self):
        pass

    def read_file(self, input_file: InputFile, read_file_config: dict, **kwargs) -> FileContent:
        """Read the content of a CSV file."""
        path = pathlib.Path(input_file.local_file_path)
        loader = CSVLoader(file_path=path, autodetect_encoding=True)
        data = loader.load()
        content = "\n\n".join([doc.page_content for doc in data])
        page_content = PageContent(
            content=content,
            page_number=0
        )
        page_contents = [page_content]
        file_content = FileContent(
            file_name=input_file.file_name,
            file_path=input_file.local_file_path,
            page_contents=page_contents,
            content_format="markdown",
        )
        return file_content
    
    async def aread_file(self, input_file, read_file_config, **kwargs):
        """Asynchronously read the content of a CSV file."""
        # TODO: Implement asynchronous reading of CSV files
        pass
