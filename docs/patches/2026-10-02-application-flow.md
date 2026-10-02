# Independent application flow

## Intent and changes

Add reviewable Python/FastAPI evidence to the documentation showcase. Read-only audit confirmed validation, persistence before notification, acceptance surviving delivery failure, and failure-path API tests. The public example uses newly written models, contracts, service, in-memory fakes, HTTP wrapper, and tests. No original source file, business field, database schema, integration, customer data, settings, or history was transferred.

Application modules total 135 lines including comments/spacing. `service.py` establishes save-before-deliver order; expected delivery failures become a separate acceptance outcome. Models are immutable, fake snapshots do not expose mutable records, and locks protect their process-local collections. Unexpected defects propagate. There is no retry, outbox, deduplication, or durable storage claim.

## Verification

Windows Python 3.14.4: compileall, pip dependency consistency, and all 14 pytest cases passed with warnings treated as errors. Coverage includes successful ordering, seven invalid-input variants without side effects, notification/storage failures, client error redaction, normalization, concurrent fake access, snapshot immutability, and unexpected failures after acceptance. Linux Python 3.12/3.14 Actions is configured and awaits publication acceptance.

The complete publication inventory and manual diff were reviewed. No confidential values, private source URLs/paths, addresses, email data, or operational identifiers were found. Reviewed URL matches are public portfolio/GitHub links and SVG metadata. Automated scans do not guarantee confidentiality; source receipts are ignored and never staged. Current Starlette TestClient uses the supported httpx2 dependency; no deprecation warning is suppressed.

## Rollback and limits

Original main: `4a8328af150e42e7d2efd41d8e2cb1b3fb4cc3ea`. A timestamped ignored backup and target manifest cover changed documentation, ignore rules, metadata, and the vault note. Use a normal revert for rollback. The service's acceptance boundary is demonstrative: in-memory records disappear on restart, and a crash after save before response can cause ambiguous retries. No external messages, production services, networking configuration, or private repository were changed.

## Publication acceptance

Implementation `b71bd6c970f632a0d72be0d5faf83233f5dd9ca5` pushed to public main. [Actions 37050417640](https://github.com/lolpul/kochura-deploy-showcase/actions/runs/37050417640) passed both Python 3.12 and 3.14 jobs with 14 tests, warnings-as-errors, compile checks, and dependency consistency.
