from marker.converters.pdf import PdfConverter
from marker.models import create_model_dict
from marker.output import text_from_rendered


class MarkerModule:
    def __init__(self):
        self.converter = PdfConverter(
            artifact_dict=create_model_dict(),
        )

    def convert_to_markdown(self, file_path: str, **kwargs):
        """
        Process the image using OCR and return the extracted text.
        """
        # Implement OCR processing logic here
        # For example, using pytesseract or any other OCR library
        print(f"Converting PDF to markdown: {file_path}")
        if not file_path.endswith(".pdf"):
            raise ValueError("File path must end with .pdf")

        rendered = self.converter(file_path)
        text, _, images = text_from_rendered(rendered)
        return text
