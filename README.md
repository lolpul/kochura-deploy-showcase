# Kochura Deploy

An independent Python/FastAPI example of validating an application, storing it, and reporting notification delivery separately from acceptance.

## Review in 30 seconds

The engineering question is what a successful response means when storage succeeds but delivery fails. Start with [the service](examples/application-flow/app/service.py), [input/output models](examples/application-flow/app/models.py) and [the HTTP adapter](examples/application-flow/app/main.py); follow [failure-ordering tests](examples/application-flow/tests/test_flow.py). [Latest local verification and demo](docs/verification.md) records what was actually run.

## What this demonstrates

Pydantic validation, a small service layer, repository and notifier protocols, typed boundary errors, and tests of failure ordering. The private product currently has a website and beta-application API; automated deployment, dashboard, and billing remain planned.

## Architecture

![Conceptual application responsibilities](docs/architecture.svg)

The public example follows request -> validation -> repository.save -> notifier.deliver. Storage success defines acceptance. Notification delivery is a separate outcome. Dependencies are injected into the service; a thin FastAPI adapter translates expected storage failure to HTTP 503.

## Code examples

Start with [service.py](examples/application-flow/app/service.py), then inspect [models.py](examples/application-flow/app/models.py), [repository.py](examples/application-flow/app/repository.py), [notifier.py](examples/application-flow/app/notifier.py), and [the HTTP wrapper](examples/application-flow/app/main.py).

The complete application flow is under 200 lines including comments and spacing, with [tests](examples/application-flow/tests/test_flow.py). It uses synthetic work items, a process-local repository, and a notifier that records numbers without sending messages.

## Engineering decisions

Validation rejects unknown fields, out-of-range quantities, implicit numeric coercion, and blank tasks. Frozen input and stored models make repository snapshots safe to share. A lock protects each in-memory fake because synchronous FastAPI handlers can run on different threads. Repository and notifier contracts keep storage and delivery details out of the service.

Delivery runs synchronously here to make ordering and outcomes observable. The private implementation schedules notification after persistence; this demonstration is not a copy of that execution mechanism. A queue or transactional outbox would require durable delivery state and retries, not implied features of this sample. See [interview notes](docs/interview-notes.md).

## Failure handling

- Invalid HTTP input: 422, with no storage or notification calls.
- Expected storage failure: 503 with a stable message, and no notification.
- Expected notification failure: 201 with notification unavailable; the record remains accepted.
- Unexpected programming errors propagate rather than being disguised as delivery failure. If they occur after saving, the record remains saved; the response can be ambiguous to a retrying client.

## Tests

Python 3.12 or 3.14, from the repository root:

```sh
python -m venv .local/venv
# Activate the venv using your shell's command, then:
python -m pip install -r requirements.txt
python -m pip check
python -m compileall -q examples/application-flow/app
python -m pytest
```

Run the toy HTTP wrapper after installing dependencies:

```sh
python -m uvicorn app.main:app --app-dir examples/application-flow
```

[GitHub Actions](https://github.com/lolpul/kochura-deploy-showcase/actions/workflows/python.yml) runs compile checks, dependency consistency, and pytest on both versions. Tests cover storage before notification, invalid input, delivery and repository outages, error redaction, normalization, immutable snapshots, concurrent fake access, and unexpected exceptions. No real services or application data are used.

## Limitations

The in-memory repository loses records on restart; it demonstrates a persistence boundary, not durable storage. There is no real email integration, background queue, delivery retry, deduplication, authentication, admission policy, or deployment system. Repeating a valid request creates another record. Top-level dependencies are pinned; transitive resolution can still change. Tests establish no production-readiness or throughput claim.

## Relation to private project

Read-only implementation and test review confirmed generic validation, persistence-before-notification, explicit failure handling, and separation of delivery from acceptance. This public sample was independently written with different models and interfaces. No private files, business fields, settings, operational data, customer information, integration recipes, or Git history were copied. Prepared with AI assistance and reproducible tests; no license to the private product is granted.

## Portfolio

[Case study](https://elisey.kochura.com/work/kochura-deploy) | [Portfolio](https://elisey.kochura.com) | [GitHub profile](https://github.com/lolpul)
