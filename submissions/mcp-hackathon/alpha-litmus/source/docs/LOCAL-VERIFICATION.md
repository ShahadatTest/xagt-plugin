# Local Verification

Recorded with Python 3.12.10. The 2026-09-19 baseline round recorded 333 passed and the pre-live hardening round recorded 560. No live Nexus calls were made by AlphaLitmus during those local-only rounds. After explicit authorization, a separate in-memory-key MCP reconciliation exposed and then verified a production object-content envelope; its evidence is recorded in [Nexus live evidence](NEXUS-LIVE-EVIDENCE.md). A later safe-mode HTTPS deployment is recorded in [VPS deployment](VPS-DEPLOYMENT.md); repository publication and submission remain separate.

## Baseline

Before edits, `python -m pytest -q` returned `14 passed, 1 warning in 3.23s`. API/MCP imports passed. No project lint/type gates were configured.

## Final Gates (Post-Live Compatibility Fix)

```text
python -m pytest -q
562 passed, 1 warning in 50.12s

python -m ruff check .
All checks passed!

python -m mypy app
Success: no issues found in 15 source files

python -m pip check
No broken requirements found.

python tools/secret_scan.py
(exit 0, no findings; rule/path/line output only)
```

No failures or skips. One upstream Starlette/AnyIO deprecation warning remains visible. Ruff has a single scoped E741 annotation for the documented OHLC field `l`, not a global suppression.

## Process Smoke

`python -m tools.local_smoke` exited 0. It checks imports, FastAPI lifespan, health/proof/capabilities, real local MCP stdio discovery and demo dispatch, a Uvicorn loopback TCP health request, and verifier subprocess exit codes. Nexus is disabled. It writes only these generated local artifacts:

- `reports/alphalitmus-synthetic-report.json`
- `reports/alphalitmus-tampered-report.json`

Both transports produced the same synthetic-reference `UNPROVEN` report hash:

```text
a9afa0e169636b68550c62f05ff71429da10fec7e379ed6f6efe81e4c305e381
```

Observed REST service/proof slug: `alpha-litmus`. Commit claims matched. TCP health: HTTP 200. MCP discovery (5 tools):

```text
challenge_nexus_strategy
find_failure_boundary
get_demo_fixture
run_nexus_window_stability
verify_failure_certificate
```

Exact verifier output for the valid export, exit 0:

```json
{"authenticity_verified": false, "errors": [], "report_id": "a9afa0e169636b68550c62f05ff71429da10fec7e379ed6f6efe81e4c305e381", "valid": true}
```

Exact verifier output for the tampered export, exit 1:

```json
{"authenticity_verified": false, "errors": ["CONTENT_HASH_MISMATCH", "TEST_MATRIX_OR_BOUNDARY_MISMATCH"], "report_id": "a9afa0e169636b68550c62f05ff71429da10fec7e379ed6f6efe81e4c305e381", "valid": false}
```

Hashes establish internal integrity, not source authenticity. Creation time is excluded deliberately. Environment commit changes can legitimately change the content hash.

## Other Checks

- Baseline secret-signature scanning passes; this is not a comprehensive external secret audit. The `tools/secret_scan.py` heuristic reports rule/path/line only and exited 0 with no findings.
- Provenance regression suite (`tests/test_provenance_round2.py`) covers strict booleans, valid/invalid commits, generation, constructed-instance revalidation, the rehashed `commit_reviewable=true`/`commit="abc123"` rejection across generation, REST, MCP, and the offline verifier, plus valid transport generation.
- Window-compute tests (`tests/test_nexus_compute.py`, `tests/test_compute_api.py`) use mocked transports with synthetic/documentation-derived fixtures and assert zero network calls on disabled/unconfirmed paths. No live Nexus request was made by the application test suite.
- Mocked upstream tests cover redaction, timeout, malformed envelopes, duplicate keys, streamed size limits, and cancellation propagation. No live Nexus request is required.
- Dashboard JavaScript was checked using actual demo/reconciliation reports in a Node DOM stub, including stale-request races and error/export behavior.
- A real Chrome review on 2026-09-19 loaded the loopback dashboard and mixed fixture over HTTP 200, rendered the desktop judge workspace, exercised the shock-demo transition to `REPORT READY / synthetic shock demo / UNPROVEN`, and found no application-origin console errors. At a 390px viewport, document width remained bounded to the viewport with no horizontal overflow. Semantic inspection confirmed the skip link, headings, status region, section navigation, labelled controls, captions, and table headers. This is bounded browser evidence, not a formal WCAG conformance audit or cross-browser certification.
- Existing negative historical reports remain unchanged. The default synthetic demos already fail at baseline; no positive-to-negative showcase was fabricated or tuned.

## Local Docker Blocker and VPS Execution

On the local Windows host, `docker version` found a client but failed connecting
to the `dockerDesktopLinuxEngine` named pipe because the daemon was unavailable.
The local `docker build -t alpha-litmus:local .` attempt failed with the same
connection error, so no **local** image or container pass is claimed.

That statement applies to the local Windows host. A subsequent authorized build
on the target Linux VPS completed successfully from the same Dockerfile and
hash-locked runtime requirements. The container passed its healthcheck as UID
10001 with a read-only filesystem, all capabilities dropped, no-new-privileges,
resource limits, no host port and Nexus disabled. Exact image/source hashes and
the subsequently verified public DNS/TLS edge are recorded in
[VPS deployment](VPS-DEPLOYMENT.md).

## Dependency Audit

`python -m pip_audit -r requirements.txt` is unavailable in the application environment (`No module named pip_audit`). The isolated release tooling environment reported:

```text
tools/__pycache__/release-venv/Scripts/python.exe -m pip_audit -r requirements.txt
No known vulnerabilities found
```

This covers locked third-party packages only, not application, deployment, or Nexus security.

DNS, Caddy TLS and the hardened safe-mode container are verified. The remaining
release steps are to publish the exact source commit, bind the deployment to that
review commit, run the official offline/online submission validators and open the
submission PR. Live Nexus review remains separate and must not be enabled
publicly without authentication and quotas.
