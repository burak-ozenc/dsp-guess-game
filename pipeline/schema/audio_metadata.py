import uuid
from dataclasses import dataclass


@dataclass
class AudioFileMetadata:
    file_path: str
    file_name: str
    file_size: int
    file_hash: str
    audio_source_id: uuid.UUID
    duration_ms: int = None
