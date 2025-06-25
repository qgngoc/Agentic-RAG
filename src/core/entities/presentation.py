from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class SavedFile(BaseModel):
    """
    Represents a saved file with a path and an optional name.
    """

    remote_file_path: str = Field(..., description="Path to the saved file")
    local_file_path: Optional[str] = Field(
        None, description="Local path to the saved file"
    )
    file_name: Optional[str] = Field(
        None, description="Name of the saved file")
    file_type: str = Field(
        ..., description="Type of the saved file (e.g., 'pptx', 'txt')"
    )


class Presentation(BaseModel):
    """
    Represents a presentation with an ID, title, and optional content.
    """

    saved_files: List[SavedFile] = Field(
        default_factory=list,
        description="List of saved files associated with the presentation",
    )
    json_content: List[Dict] = Field(
        default_factory=list, description="JSON content of the presentation"
    )
