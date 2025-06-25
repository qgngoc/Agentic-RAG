from core.ports.secondary.services import TxtFileReadingService
from core.entities import InputFile, FileContent, PageContent, TxtReadFileConfig

class TxtFileReadingServiceImpl(TxtFileReadingService):
    """Service implementation for reading TXT files."""
    def __init__(self):
        pass

    def read_file(self, input_file: InputFile, read_file_config: dict, **kwargs) -> FileContent:
        """Read the content of a TXT file."""
        with open(input_file.local_file_path, "r", encoding="utf-8") as file:
            content = file.read()
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
        # TODO: Implement asynchronous reading of TXT files
        pass
