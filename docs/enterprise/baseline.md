# Upstream baseline

## Provenance

This project extends the decode coding-agent course codebase.
The upstream-baseline Git tag identifies the imported source snapshot.
The original license and author attribution are retained.

## Initial verification

Command:

    uv run --locked pytest tests/unit -q

Observed result:

- Passed: 2998
- Skipped: 1
- Duration: 62.57 seconds

Skip:

    tests/unit/decode/remote/test_app.py:130
    could not import 'fastapi': No module named 'fastapi'

## Interpretation

The existing unit suite passed in the local WSL environment, except for
one test skipped because FastAPI was unavailable.

This result does not establish:
- Real-model coding-task success.
- Docker or Modal integration correctness.
- Security isolation.
- Multi-user capacity.
- Agent latency or throughput.

The reported duration is unit-test suite runtime, not agent task latency.

## Planned milestones

1. Secure sandbox execution and resource limits.
2. Network policy and credential separation.
3. Durable jobs, attempts, and API endpoints.
4. Recovery, approvals, and publishing reconciliation.
5. User, project, and repository authorization.
6. Audit, observability, and budget enforcement.
7. Simulated-client platform load testing.
8. Real-model task evaluation and baseline comparison.

## Environment captured after verification

```text
1667540109a241dae0aa4fa82d5f4fdbbeea74ef
1667540109a241dae0aa4fa82d5f4fdbbeea74ef
uv 0.13.4 (x86_64-unknown-linux-gnu)
Python 3.12.15
Linux 6.18.54.1-microsoft-standard-WSL2 x86_64 GNU/Linux
```
