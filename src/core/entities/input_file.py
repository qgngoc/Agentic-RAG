from typing import List, Optional, Union

from pydantic import BaseModel, Field

from .read_file_config import (
    CsvReadFileConfig,
    DocxReadFileConfig,
    MdReadFileConfig,
    PdfReadFileConfig,
    PptxReadFileConfig,
    ReadFileConfig,
    TxtReadFileConfig,
    XlsxReadFileConfig,
)


class InputFile(BaseModel):
    """
    Represents a reference document with an ID, title, and optional content.
    """

    remote_file_path: Optional[str] = Field(
        None, description="Path to the remote reference file"
    )
    local_file_path: Optional[str] = Field(
        None, description="Path to the reference file"
    )
    file_name: Optional[str] = Field(
        None, description="Name of the reference file"
    )
    file_type: str = Field(
        ..., description="Type of the reference file (e.g., 'pdf', 'docx')"
    )
    # read_file_config: Union[dict, ReadFileConfig] = Field(
    #     ..., description="Configuration for reading the reference file"
    # )
    read_file_config: dict = Field(
        ..., description="Configuration for reading the reference file"
    )


class PdfInputFile(InputFile):
    """
    Represents a PDF reference file with specific reading configurations.
    """

    read_file_config: PdfReadFileConfig = Field(
        ..., description="Configuration for reading PDF reference files"
    )


class DocxInputFile(InputFile):
    """
    Represents a DOCX reference file with specific reading configurations.
    """

    read_file_config: DocxReadFileConfig = Field(
        ..., description="Configuration for reading DOCX reference files"
    )


class XlsxInputFile(InputFile):
    """
    Represents an XLSX reference file with specific reading configurations.
    """

    read_file_config: XlsxReadFileConfig = Field(
        ..., description="Configuration for reading XLSX reference files"
    )


class CsvInputFile(InputFile):
    """
    Represents a CSV reference file with specific reading configurations.
    """

    read_file_config: CsvReadFileConfig = Field(
        ..., description="Configuration for reading CSV reference files"
    )


class TxtInputFile(InputFile):
    """
    Represents a TXT reference file with specific reading configurations.
    """

    read_file_config: TxtReadFileConfig = Field(
        ..., description="Configuration for reading TXT reference files"
    )


class MdInputFile(InputFile):
    """
    Represents a Markdown reference file with specific reading configurations.
    """

    read_file_config: MdReadFileConfig = Field(
        ..., description="Configuration for reading Markdown reference files"
    )
    
class PptxInputFile(InputFile):
    """
    Represents a PPTX reference file with specific reading configurations.
    """

    read_file_config: PptxReadFileConfig = Field(
        ..., description="Configuration for reading PPTX reference files"
    )
