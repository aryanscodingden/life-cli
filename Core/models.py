from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Task:
    id: int
    title: str
    note: str
    due: Optional[datetime]
    duration: Optional[str]
    keep: bool
    calender_event_id: Optional[id]
    keep_note_id: Optional[str]

