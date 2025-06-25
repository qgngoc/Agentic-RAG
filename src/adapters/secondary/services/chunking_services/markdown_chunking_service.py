
import re
import uuid
from pydantic import BaseModel
from typing import Union, List


from core.ports.secondary.services import ChunkingService, MarkdownChunkingService
from core.entities import Document, FileContent, Client, PageContent

class MarkdownSection(BaseModel):
    content: str
    header: Union[str, None] = None
    subheader: Union[str, None] = None
    page_number: int = 0


class MarkdownChunkingServiceImpl(MarkdownChunkingService):
    """Chunking service for Markdown files."""
    def __init__(self):
        pass
    
    def chunk(self, file_content: FileContent) -> list[Document]:
        """Chunk the file content into smaller documents."""
        # Implement the logic to chunk the Markdown content
        # For example, split by headings or paragraphs
        # This is a placeholder implementation
        documents = []
        all_markdown_sections = []
        for page_content in file_content.page_contents:
            # md_text = page_content.content
            markdown_sections = self._structural_chunking(page_content)
            all_markdown_sections.extend(markdown_sections)
        
        last_header = None
        last_subheader = None
        for section in all_markdown_sections:
            if not section.content.strip():
                continue
            if not section.header:
                section.header = last_header
            if not section.subheader:
                section.subheader = last_subheader
            if last_subheader:
                section.content = last_subheader + '\n' + section.content.strip()
            last_header = section.header
            last_subheader = section.subheader
            document = self._markdown_to_document(section, file_content)
            documents.append(document)
        return documents

    async def achunk(self, file_content: FileContent) -> list[Document]:
        """Asynchronously chunk the file content into smaller documents."""
        # For now, we will just call the synchronous method
        # TODO: Implement asynchronous chunking logic if needed
        return self.chunk(file_content)
    
    def _extract_heading_pattern(self, md_text: str):
        """Extract headings from Markdown text."""
        heading_pattern = r'^# (.*)$'
        subheading_pattern = r'^## (.*)$'
        return heading_pattern, subheading_pattern
    
    def _structural_chunking(self, page_content: PageContent, max_chars_in_chunk: int = 512) -> list[MarkdownSection]:
        """Chunk Markdown text into sections based on headings."""
        md_text = page_content.content
        heading_pattern, subheading_pattern = self._extract_heading_pattern(md_text)
        sections = []
        current_section = MarkdownSection(content="")
        
        for line in md_text.split('\n'):
            line = line.strip()
            if re.match(heading_pattern, line):
                if current_section.content:
                    sections.append(current_section)
                current_section = MarkdownSection(content="", header=line.strip(), page_number=page_content.page_number)
            elif re.match(subheading_pattern, line):
                current_section.subheader = line.strip()
                current_section.content += (line + '\n')
            else:
                if len(current_section.content) + len(line) + 1 <= max_chars_in_chunk:
                    current_section.content += (line + '\n')
                else:
                    sections.append(current_section)
                    current_section = MarkdownSection(content=line + '\n', page_number=page_content.page_number)
        if current_section.content:
            sections.append(current_section)
        return sections
    
    def _markdown_to_document(self, section: MarkdownSection, file_content: FileContent) -> Document:
        """Convert a Markdown section to a Document."""
        document_id = str(uuid.uuid4())
        return Document(
            id=document_id,
            content=section.content.strip(),
            file_name=file_content.file_name,
            file_path=file_content.file_path,
            page_number=section.page_number
        )