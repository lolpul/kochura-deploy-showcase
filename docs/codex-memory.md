# Application showcase memory - v4

- Purpose: independent Python/FastAPI application flow alongside the beta-onboarding overview.
- Repository: https://github.com/lolpul/kochura-deploy-showcase. Private product remains private; deployment platform features remain planned.
- Entry: examples/application-flow/app/service.py; models/repository/notifier/main adjacent; tests/test_flow.py exercises boundaries and HTTP behavior.
- Contracts: validate -> save -> notify; expected delivery failure preserves acceptance; storage failure skips notification; unexpected errors propagate.
- Fakes: immutable Pydantic values, locked process-local storage and notification numbers. Restart loses data; no external delivery, retries, deduplication, or customer fields.
- Commands: python -m pip install -r requirements.txt; python -m pip check; python -m compileall -q examples/application-flow/app; python -m pytest.
- CI: .github/workflows/python.yml tests Python 3.12/3.14. Top-level dependencies pinned independently.
- Audit: confirmed generic concepts; no source, business data, configuration, integration, naming, or history transfer. Receipts/backups ignored.
- Verified: 14 tests pass on Windows Python 3.14.4 and Linux Python 3.12/3.14, warnings-as-errors; compileall and pip check pass. [Actions 37050417640](https://github.com/lolpul/kochura-deploy-showcase/actions/runs/37050417640) accepted implementation b71bd6c970f632a0d72be0d5faf83233f5dd9ca5.
- Next: Kotlin showcase, then profile and portfolio integration. Publication inventory and manual confidentiality review passed.
- Docs: [scope](spec.md), [interview notes](interview-notes.md), [patch](patches/2026-10-02-application-flow.md).
- Portfolio: https://elisey.kochura.com/work/kochura-deploy; site integration follows three published showcases.
