import pandas as pd
from core.ports.secondary.services import XlsxFileReadingService
from core.entities import InputFile, FileContent, PageContent, XlsxReadFileConfig

class XlsxFileReadingServiceImpl(XlsxFileReadingService):
    """Service implementation for reading XLSX files."""
    def __init__(self):
        pass

    def read_file(self, input_file: InputFile, read_file_config: dict, **kwargs) -> FileContent:
        df = pd.read_excel(input_file.local_file_path)
        content = df.to_string()
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
        # TODO: Implement asynchronous reading of XLSX files
        pass
