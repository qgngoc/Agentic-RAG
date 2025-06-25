import os

from markitdown import MarkItDown


class MarkitdownModule:
    def __init__(self):
        self.md = MarkItDown()

    def convert_to_markdown(self, file_path: str, **kwargs):
        results = self.md.convert(file_path)
        return results.text_content
