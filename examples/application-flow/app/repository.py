from threading import Lock
from typing import Protocol

from .models import ApplicationInput, SavedApplication


class StorageUnavailable(Exception):
    """Adapters translate expected persistence failures to this boundary error."""


class Repository(Protocol):
    def save(self, request: ApplicationInput) -> SavedApplication:
        """Return only after acceptance by storage; raise StorageUnavailable on failure."""
        ...


class MemoryRepository:
    """A thread-safe teaching fake. Restarting the process loses every record."""

    def __init__(self) -> None:
        self._lock = Lock()
        self._records: list[SavedApplication] = []

    def save(self, request: ApplicationInput) -> SavedApplication:
        with self._lock:
            saved = SavedApplication(number=len(self._records) + 1, request=request)
            self._records.append(saved)
            return saved

    def snapshot(self) -> tuple[SavedApplication, ...]:
        with self._lock:
            return tuple(self._records)
