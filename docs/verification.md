# Verification — 2026-10-10

Python 3.14.4; clean venv and pinned top-level requirements. `pip check`, `compileall` and `pytest -q -W error`: **14 tests passed**. Uvicorn was started on loopback; `/docs` and `/openapi.json` returned 200. The independent notifier sends no messages.

Reproduce the README installation/tests; use `python -m uvicorn app.main:app --app-dir examples/application-flow --host 127.0.0.1 --port 8000`. Open `http://127.0.0.1:8000/docs` and submit `{"task":"Synthetic sample","units":2}` to `POST /applications`; acceptance is 201. Invalid quantity or unknown fields return 422. Each process restart clears records.

[Actions](https://github.com/lolpul/kochura-deploy-showcase/actions/workflows/python.yml) checks Python 3.12 and 3.14. Local rerun here used 3.14; exact hosted runs are recorded by GitHub. No durable database, queue or private product integration was tested.
