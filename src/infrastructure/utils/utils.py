import base64
import io
import json
import os
import re
import subprocess
from typing import List

import fitz  # PyMuPDF
from PIL import Image

def pdf_to_base64_images(pdf_path, max_pages=None, resize_width=1000):
    doc = fitz.open(pdf_path)
    base64_images = []
    for i, page in enumerate(doc):
        if max_pages and i >= max_pages:
            break
        pix = page.get_pixmap(dpi=150)
        img = Image.open(io.BytesIO(pix.tobytes("png")))
        # Resize if too large
        if img.width > resize_width:
            ratio = resize_width / img.width
            img = img.resize((resize_width, int(img.height * ratio)))
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
        base64_images.append(f"data:image/png;base64,{b64}")
    return base64_images


def extract_markdown_text(text: str):
    pattern = r"```markdown(.*?)```"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        markdown_text = match.group(1).strip()
        return markdown_text
    else:
        return text

def read_txt_file(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    return content
    