from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from uuid import uuid4


@dataclass
class StoredResume:
    text: str
    filename: str
    created_at: datetime


class ResumeStore:
    def __init__(self, ttl_minutes: int = 60) -> None:
        self._items: dict[str, StoredResume] = {}
        self._ttl = timedelta(minutes=ttl_minutes)

    def put(self, text: str, filename: str) -> str:
        self.cleanup()
        resume_id = str(uuid4())
        self._items[resume_id] = StoredResume(
            text=text,
            filename=filename,
            created_at=datetime.now(timezone.utc),
        )
        return resume_id

    def get(self, resume_id: str) -> StoredResume | None:
        self.cleanup()
        return self._items.get(resume_id)

    def cleanup(self) -> None:
        now = datetime.now(timezone.utc)
        expired = [
            resume_id
            for resume_id, item in self._items.items()
            if now - item.created_at > self._ttl
        ]
        for resume_id in expired:
            self._items.pop(resume_id, None)


resume_store = ResumeStore()

