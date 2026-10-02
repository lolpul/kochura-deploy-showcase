from concurrent.futures import ThreadPoolExecutor

import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from app.main import create_app
from app.models import ApplicationInput
from app.notifier import DeliveryUnavailable, RecordingNotifier
from app.repository import MemoryRepository, StorageUnavailable
from app.service import ApplicationService


VALID = {"task": "Synthetic work item", "units": 2}


def setup_flow(notifier=None, repository=None):
    repository = repository if repository is not None else MemoryRepository()
    notifier = notifier if notifier is not None else RecordingNotifier()
    return repository, notifier, ApplicationService(repository, notifier)


def test_valid_request_is_stored_before_notification():
    repository = MemoryRepository()
    observed = []

    class ObservingNotifier:
        def deliver(self, application):
            assert repository.snapshot() == (application,)
            observed.append(application.number)

    _, _, service = setup_flow(ObservingNotifier(), repository)
    result = service.accept(ApplicationInput(**VALID))
    assert result.application_number == 1
    assert result.notification == "delivered"
    assert observed == [1]


@pytest.mark.parametrize("invalid", [
    {"task": "  ", "units": 1},
    {"task": "x" * 121, "units": 1},
    VALID | {"units": 0},
    VALID | {"units": 21},
    VALID | {"units": "2"},
    VALID | {"units": True},
    VALID | {"unexpected": "value"},
])
def test_invalid_api_request_has_no_side_effects(invalid):
    repository, notifier, service = setup_flow()
    with TestClient(create_app(service)) as client:
        assert client.post("/applications", json=invalid).status_code == 422
    assert repository.snapshot() == ()
    assert notifier.snapshot() == ()


class FailingNotifier:
    def deliver(self, application):
        raise DeliveryUnavailable("synthetic delivery outage")


def test_notification_failure_preserves_accepted_application():
    repository, _, service = setup_flow(FailingNotifier())
    with TestClient(create_app(service)) as client:
        response = client.post("/applications", json=VALID)
    assert response.status_code == 201
    assert response.json() == {"application_number": 1, "notification": "unavailable"}
    assert repository.snapshot()[0].request == ApplicationInput(**VALID)


class FailingRepository:
    def save(self, request):
        raise StorageUnavailable("synthetic adapter diagnostics")


def test_repository_failure_never_notifies_and_hides_details():
    _, notifier, service = setup_flow(repository=FailingRepository())
    with TestClient(create_app(service)) as client:
        response = client.post("/applications", json=VALID)
    assert response.status_code == 503
    assert response.json() == {"detail": "Storage unavailable"}
    assert notifier.snapshot() == ()


def test_valid_api_response_and_normalization():
    repository, notifier, service = setup_flow()
    with TestClient(create_app(service)) as client:
        response = client.post("/applications", json=VALID | {"task": "  Work item  "})
    assert response.status_code == 201
    assert response.json() == {"application_number": 1, "notification": "delivered"}
    assert repository.snapshot()[0].request.task == "Work item"
    assert notifier.snapshot() == (1,)


def test_concurrent_fake_storage_allocates_distinct_numbers():
    repository, notifier, service = setup_flow()
    with ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(lambda _: service.accept(ApplicationInput(**VALID)), range(32)))
    assert sorted(result.application_number for result in results) == list(range(1, 33))
    assert len(repository.snapshot()) == len(notifier.snapshot()) == 32


def test_saved_input_cannot_be_mutated_through_snapshot():
    repository, _, service = setup_flow()
    service.accept(ApplicationInput(**VALID))
    with pytest.raises(ValidationError):
        repository.snapshot()[0].request.task = "Changed"
    assert repository.snapshot()[0].request.task == VALID["task"]


def test_unexpected_programming_error_is_not_misclassified_as_delivery_failure():
    class BrokenNotifier:
        def deliver(self, application):
            raise RuntimeError("programming defect")

    repository, _, service = setup_flow(BrokenNotifier())
    with pytest.raises(RuntimeError):
        service.accept(ApplicationInput(**VALID))
    assert len(repository.snapshot()) == 1
