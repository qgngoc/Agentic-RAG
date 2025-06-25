from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Union, Callable

class Citation(BaseModel):
    file_name: str
    file_path: str
    page_number: int
    page_content: str