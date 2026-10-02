# Discussing the application flow

Problem: a delivery outage should not erase an accepted application or make persistence appear to have failed. Constraints: synthetic input, no customer fields, no external notification integration, and a small reviewable service.

Decision: validate at the boundary, save through a repository contract, then notify separately. Return acceptance and delivery as separate facts. Immutable models and locks protect the process-local fakes across synchronous HTTP workers.

Alternatives: put everything in the endpoint (fewer files, coupled tests); background delivery (less response latency, less immediate outcome visibility); transactional outbox (durable intent, with storage schema, workers, retries and idempotency). These are discussion topics, not delivered features.

Failure modes: invalid input never reaches dependencies; a storage error stops the flow; a known delivery outage preserves the record. Programming defects are not swallowed. A crash after save and before response creates ambiguity; there is no idempotency key. Delivery failures are returned, not durably recorded or retried. In-memory tests do not establish database crash recovery.

Trade-offs: synchronous delivery makes ordering clear but adds latency; immutable snapshots prevent shared mutation but are not transactions; narrow exception contracts keep defects visible but require real adapters to translate expected errors.

Questions: Where is acceptance established? Why must a storage outage skip notification? Why catch DeliveryUnavailable rather than Exception? How can a timeout create duplicate submissions? Where would retry state live? What changes with SQLite? Which tests prove ordering, and which assumptions remain untested?
