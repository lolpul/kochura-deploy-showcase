# Independent application-flow example

## Problem and boundary

Demonstrate validation, a repository boundary, and persistence before notification. Read-only source audit confirms a FastAPI/Pydantic request boundary, persistence preceding notification scheduling, repository error responses, and tests proving that notification failure preserves the record. These generic decisions inform a new sample; original models, business fields, integrations, data, naming, settings, infrastructure, and Git history are excluded.

## Implementation stages

1. Write an immutable, bounded Pydantic request for synthetic work items, repository/notifier protocols, and typed boundary failures. Acceptance: invalid input cannot reach persistence.
2. Write an application service with save-before-notify order. Use in-memory fakes without email or network access. Acceptance: notification failure returns an accepted result with a distinct delivery outcome; repository failure never invokes notification.
3. Add a small FastAPI wrapper and unit/API tests. Acceptance: valid 201, invalid 422, storage failure 503; clean client errors and no partial notification on rejected input. No duplicate/idempotency guarantee is introduced without source evidence.
4. Document failure modes and limits, add Python CI, run pytest and compile checks, review the complete publication set for confidentiality, then commit/push and verify Actions.

Storage here is process-local and intentionally not durable. Synchronous fake notification keeps failure ordering observable; production delivery queues, retries, credentials, migrations, or deployment are outside scope. Original main and affected-file backups are recorded locally; rollback uses a public revert.
