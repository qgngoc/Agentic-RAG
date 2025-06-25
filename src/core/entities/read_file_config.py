from typing import List, Optional, Union

from pydantic import BaseModel, Field


class ReadFileConfig(BaseModel):
    """
    Represents the configuration for reading files, including file paths and types.
    """

    pass


class PdfReadFileConfig(ReadFileConfig):
    """
    Configuration for reading PDF files.
    """

    force_ocr: bool = Field(
        default=False, description="Whether to use LLM for reading PDF files"
    )
    use_llm_enhance: bool = Field(
        default=False,
        description="Whether to use LLM for enhancing PDF content")
    use_llm_extract: bool = Field(
        default=False,
        description="Whether to use LLM for extracting information from PDF files",
    )


class DocxReadFileConfig(ReadFileConfig):
    # convert_to_pdf: bool = Field(
    #     default=False,
    #     description="Whether to convert DOCX files to PDF before processing",
    # )
    # pdf_config: Union[PdfReadFileConfig, None] = Field(
    #     default=PdfReadFileConfig(),
    #     description="Configuration for reading PDF files from DOCX",
    # )
    pass


class XlsxReadFileConfig(ReadFileConfig):
    """
    Configuration for reading XLSX files.
    """

    # convert_to_pdf: bool = Field(
    #     default=False, description="Whether to convert XLSX files to PDF before processing")
    # pdf_config: Union[PdfReadFileConfig, None] = Field(
    # default=PdfReadFileConfig(), description="Configuration for reading PDF
    # files from XLSX")
    pass


class CsvReadFileConfig(ReadFileConfig):
    """
    Configuration for reading CSV files.
    """

    pass


class TxtReadFileConfig(ReadFileConfig):
    """
    Configuration for reading text files.
    """

    pass


class MdReadFileConfig(ReadFileConfig):
    """
    Configuration for reading Markdown files.
    """

    pass


class PptxReadFileConfig(ReadFileConfig):
    """
    Configuration for reading PPTX files.
    """

    # convert_to_pdf: bool = Field(
    #     default=False,
    #     description="Whether to convert PPTX files to PDF before processing",
    # )
    # pdf_config: Union[PdfReadFileConfig, None] = Field(
    #     default=PdfReadFileConfig(),
    #     description="Configuration for reading PDF files from PPTX",
    # )
    pass
