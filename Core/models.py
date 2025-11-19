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
    calender_event_id: Optional[str]
    keep_note_id: Optional[str]
    google_task_id: Optional[str]

    @property
    def is_event(self) -> bool:
        """Determine if this task is an event based on whether it has a due date."""
        return self.due is not None

