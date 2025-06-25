import pathlib
from infrastructure.frameworks.markitdown_module import MarkitdownModule
from core.ports.secondary.services import DocxFileReadingService
from core.entities import InputFile, FileContent, PageContent, DocxReadFileConfig

class DocxFileReadingServiceImpl(DocxFileReadingService):
    """Service implementation for reading DOCX files."""
    def __init__(self, markitdown_module: MarkitdownModule = MarkitdownModule()):
        self.md = markitdown_module

    def read_file(self, input_file: InputFile, read_file_config: dict, **kwargs) -> FileContent:
        """Read the content of a DOCX file."""
        content = self.md.convert_to_markdown(input_file.local_file_path)
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
        # TODO: Implement asynchronous reading of DOCX files
        pass
