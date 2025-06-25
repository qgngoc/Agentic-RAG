import pymupdf4llm
from typing import Union
from core.ports.secondary.services import PdfFileReadingService, LLMService
from core.entities import InputFile, FileContent, PageContent, PdfReadFileConfig, Message, LLMConfig, LLMCompletion

from infrastructure.frameworks.marker_module import MarkerModule
# from core.ports.secondary.services.common.llm_service import LLMService
from infrastructure.utils.utils import pdf_to_base64_images, extract_markdown_text

class PdfFileReadingServiceImpl(PdfFileReadingService):
    """Service implementation for reading PDF files."""
    def __init__(self, llm_service: LLMService, marker: MarkerModule = MarkerModule()):
        self.marker = marker
        self.llm_service = llm_service

    def _convert_to_markdown_pymupdf(self, path: str) -> Union[list[PageContent], None]:
        """Convert PDF to markdown using Pymupdf."""
        try:
            pages = pymupdf4llm.to_markdown(path, page_chunks=True)
            page_contents = []
            for i, page in enumerate(pages):
                md_text = page.get("text", "")
                if not md_text:
                    continue
                page_content = PageContent(
                    content=md_text,
                    page_number=i,
                )
                page_contents.append(page_content)
            return page_contents
        except Exception as e:
            print(f"Error converting PDF to markdown by Pymupdf: {e}")
            return None
        
    def _convert_to_markdown_marker(self, path: str) -> Union[list[PageContent], None]:
        """Convert PDF to markdown using MarkerModule."""
        try:
            md_text = self.marker.convert_to_markdown(path)
            page_content = PageContent(
                content=md_text,
                page_number=1,  # Assuming single page for simplicity
            )
            return [page_content] if md_text else None
        except Exception as e:
            print(f"Error converting PDF to markdown by MarkerModule: {e}")
            return None

    def _convert_to_markdown_llm(self, path: str, pages_per_chunk=5) -> Union[list[PageContent], None]:
        """Convert PDF to markdown using LLM."""
        llm_config = LLMConfig(model="gpt-4.1-mini", temperature=0.01)
        b64_images = pdf_to_base64_images(path)

        image_messages = [{"type": "image_url", "image_url": {"url": url}} for url in b64_images]

        i = 0
        extracted_text = ''
        while i < len(image_messages):
            chunk = image_messages[i:i + pages_per_chunk]
            if not chunk:
                break
            i += pages_per_chunk
        
            system_message = Message(
                role="system",
                content="You are a helpful assistant"
            )
            user_message = Message(
                role="user",
                content=[
                    {"type": "text", "text": "Given the following images which is converted from a PDF file, please convert content to markdown format. With tables, please use markdown table format and generate a description below of each table. With images and charts, generate the text representation or description of the image or chart. Please return the markdown text in markdown code block (```markdown```)"},
                    *chunk
                ]
            )

            response = self.llm_service.chat(
                llm_config=llm_config,  # Example LLM config
                messages=[system_message, user_message]
            )
            if response and isinstance(response, LLMCompletion):
                extracted_text += extract_markdown_text(response.text)
                
        return [PageContent(content=extracted_text, page_number=1)]
    
    def _enhance_page_contents(self, page_contents: list[PageContent]) -> list[PageContent]:
        llm_config = LLMConfig(model="gpt-4.1-mini", temperature=0.01)
        
        for i in range(len(page_contents)):
            page_content = page_contents[i]
            if not page_content.content.strip():
                continue
            
            system_message = Message(
                role="system",
                content="You are a helpful assistant."
            )
            user_message = Message(
                role="user",
                content=f"Given the text extracted from a PDF file, which might have some errors, please enhance the text by checking spelling and grammar.\n\nText: {page_content.content}.\n\nPlease return the enhanced text in markdown format in markdown code block (```markdown```)"
            )
            
            response = self.llm_service.chat(
                llm_config=llm_config,
                messages=[system_message, user_message]
            )
            
            if response and isinstance(response, LLMCompletion):
                page_content.content = extract_markdown_text(response.text)

        return page_contents

    def _convert_to_markdown(self, path: str, force_ocr: bool = False, use_llm_extract: bool = False, use_llm_enhance: bool = False) -> Union[list[PageContent], None]:
        if force_ocr:
            page_contents = self._convert_to_markdown_marker(path)
        elif use_llm_extract:
            page_contents = self._convert_to_markdown_llm(path)
        else:
            page_contents = self._convert_to_markdown_pymupdf(path)
            if not page_contents:
                page_contents = self._convert_to_markdown_marker(path)
        if not page_contents:
            raise ValueError("Failed to convert PDF to markdown using available methods.")
        if use_llm_enhance:
            page_contents = self._enhance_page_contents(page_contents)
        return page_contents

    def read_file(self, input_file: InputFile, read_file_config: dict, **kwargs) -> FileContent:
        read_file_config = PdfReadFileConfig(**read_file_config) if read_file_config else PdfReadFileConfig()
        force_ocr = getattr(read_file_config, "force_ocr", False)
        use_llm_extract = getattr(read_file_config, "use_llm_extract", False)
        use_llm_enhance = getattr(read_file_config, "use_llm_enhance", False)
        print(f"force_ocr={force_ocr}, use_llm_extract={use_llm_extract}, use_llm_enhance={use_llm_enhance}")
        page_contents = self._convert_to_markdown(input_file.local_file_path, force_ocr=force_ocr, use_llm_extract=use_llm_extract, use_llm_enhance=use_llm_enhance)
        file_content = FileContent(
            file_name=input_file.file_name,
            file_path=input_file.local_file_path,
            page_contents=page_contents,
            content_format="markdown",
        )
        return file_content

    async def aread_file(self, input_file, read_file_config, **kwargs):
        # TODO: Implement asynchronous reading of PDF files
        pass

