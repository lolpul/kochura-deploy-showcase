from fastapi import FastAPI, HTTPException

from .models import Acceptance, ApplicationInput
from .notifier import RecordingNotifier
from .repository import MemoryRepository, StorageUnavailable
from .service import ApplicationService


def create_app(service: ApplicationService) -> FastAPI:
    api = FastAPI(title="Independent application-flow example")

    @api.post("/applications", status_code=201, response_model=Acceptance)
    def submit(request: ApplicationInput) -> Acceptance:
        try:
            return service.accept(request)
        except StorageUnavailable:
            # Adapter diagnostic details are never returned to the caller.
            raise HTTPException(503, "Storage unavailable") from None

    return api


app = create_app(ApplicationService(MemoryRepository(), RecordingNotifier()))
