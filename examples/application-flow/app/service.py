from .models import Acceptance, ApplicationInput
from .notifier import DeliveryUnavailable, Notifier
from .repository import Repository


class ApplicationService:
    def __init__(self, repository: Repository, notifier: Notifier) -> None:
        self.repository = repository
        self.notifier = notifier

    def accept(self, request: ApplicationInput) -> Acceptance:
        # Storage defines acceptance. A failed save exits before delivery begins.
        saved = self.repository.save(request)
        delivery = "delivered"
        try:
            self.notifier.deliver(saved)
        except DeliveryUnavailable:
            # Keep the accepted record; expose delivery as a separate outcome.
            delivery = "unavailable"
        return Acceptance(
            application_number=saved.number,
            notification=delivery,
        )
