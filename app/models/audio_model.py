from dataclasses import dataclass
from typing import Optional


@dataclass
class AudioModel:
    id: Optional[int] = None
    original_name: Optional[str] = None
    file_name: Optional[str] = None
    file_path: Optional[str] = None
    notes: Optional[str] = None
    created_at: Optional[str] = None