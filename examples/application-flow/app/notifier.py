from threading import Lock
from typing import Protocol

from .models import SavedApplication


class DeliveryUnavailable(Exception):
    """An expected notification failure, distinct from application rejection."""


class Notifier(Protocol):
    def deliver(self, application: SavedApplication) -> None:
        """Use DeliveryUnavailable for expected delivery failures; no storage mutation."""
        ...


class RecordingNotifier:
    """Records synthetic numbers in memory. Does not send any external message."""

    def __init__(self) -> None:
        self._lock = Lock()
        self._numbers: list[int] = []

    def deliver(self, application: SavedApplication) -> None:
        with self._lock:
            self._numbers.append(application.number)

    def snapshot(self) -> tuple[int, ...]:
        with self._lock:
            return tuple(self._numbers)
