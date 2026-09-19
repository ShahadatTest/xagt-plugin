# AlphaLitmus Release Readiness

**Public safe-mode deployment verified; final submission publication remains pending.**
The HTTPS service, container hardening and public review routes are recorded in
[VPS deployment](VPS-DEPLOYMENT.md). Separately authorized Studio backtests and
one read-only AlphaLitmus-to-Nexus MCP reconciliation are recorded in
[Nexus live evidence](NEXUS-LIVE-EVIDENCE.md). The public deployment keeps Nexus
and remote compute disabled; repository publication, official validation and the
submission PR are separate gates.

## Local Quality Gate

Run with Python 3.12 from the project root:

```powershell
python -m pip install -r requirements-dev.txt
python -m pytest -q
python -m ruff check .
python -m mypy app
python -c "import app.main, app.mcp_server, app.lab, app.certificates"
python -m tools.local_smoke
```

Pytest checks its configuration/markers strictly. Ruff enables E4/E7/E9/F with no ignore list. Mypy checks all `app` modules in strict mode, without missing-import suppression or module overrides. Configuration alone is not evidence that a gate passes.

The inspected tooling is Ruff 0.16.6 and mypy 1.20.2. Runtime and development dependencies ship as pip-tools transitive SHA-256 hash locks (`requirements.in`/`requirements-dev.in` inputs, `requirements.txt`/`requirements-dev.txt` locked outputs); Docker installs with `--require-hashes`. A wheel-verified third-party license inventory is generated from downloaded artifacts without inventing project licensing or ownership. These locks were resolved on Windows; Linux/Docker installation still needs verification on the target platform, and the `python:3.12-slim` tag is mutable. See [dependencies](DEPENDENCIES.md).

## Required Acceptance Checks

Final local gates, Python 3.12.10:

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
(exit 0, no findings)

python -m tools.local_smoke
(exit 0; 5 MCP tools; REST/MCP hash-equivalent UNPROVEN synthetic report)
```

There were zero failures and zero skips. The warning is Starlette's use of AnyIO's deprecated BlockingPortal alias; it is not suppressed. Quantitative unchanged-fixture results are recorded in [DEMO](DEMO.md). Full smoke evidence and its reproduction command are in [LOCAL-VERIFICATION](LOCAL-VERIFICATION.md).

`python -m pip_audit -r requirements.txt` is unavailable in the application environment (`No module named pip_audit`). The isolated release tooling environment (`tools/__pycache__/release-venv`, pip-audit 2.10.1) reported **no known vulnerabilities** for `requirements.txt`. That audit queries vulnerability services for locked third-party packages only; it is not a Nexus, deployment, or application-security certification.

Local health service and proof slug both returned `alpha-litmus`. The source reads only `ALPHALITMUS_COMMIT`, without a legacy fallback. Development reported `local-dev`, not an actual public review commit. Body handling is capped at 4,000,000 bytes, eight intake slots, a 10-second body deadline and two compute slots per process; `GET /health` bypasses upload intake and compute admission and never waits for body input.

A real local MCP stdio subprocess client discovered all five tools and obtained the full mixed demo report. Its hash matched REST exactly. A separate Uvicorn subprocess served health over loopback TCP with HTTP 200. The offline verifier exited 0 for the valid exported report and 1 for its tampered counterpart. Provenance rejects `commit_reviewable=true` with `commit="abc123"` at generation, REST, MCP, and offline-verifier layers. These are local process/transport checks, not an external MCP host or public deployment.

A real Chrome pass on 2026-09-19 rendered the dashboard, exercised the mixed-to-shock demo transition, checked the semantic control/table structure, and verified a 390px viewport without document-level horizontal overflow. No application-origin console errors were observed. This is a bounded visual/responsive review, not formal accessibility conformance or broad cross-browser coverage.

The Windows Docker daemon remained unavailable, but the authorized target Linux
VPS subsequently built the image from the same Dockerfile and hash-locked runtime
requirements. The resulting container passed health as UID 10001 with a read-only
root filesystem, dropped capabilities, no-new-privileges, explicit resource
limits and no host port. Nexus remained disabled and no key was deployed. See
[VPS deployment](VPS-DEPLOYMENT.md). Public DNS/TLS are verified there; only
final reviewed-commit binding remains pending.

- [x] Final source imports, tests, lint and strict types pass with recorded exact commands/environment.
- [x] REST OpenAPI and MCP `tools/list` match README request nesting, field domains and five tool names.
- [x] Synthetic examples cannot receive an eligible survival verdict; missing Nexus evidence remains unproven.
- [x] A certificate verifies offline; both an ordinary tamper and a rehashed inconsistent analysis fail verification.
- [x] Provenance contract enforced: reviewable requires nonzero lowercase 40-hex, unreviewable permits only `local-dev`; the rehashed `abc123` claim is rejected by generation, REST, MCP, and the offline verifier.
- [ ] Production provenance rejects missing/invalid commit configuration; health and proof match an actual public reviewed commit.
- [x] A real named Nexus strategy completed one Studio backtest and was left stopped; its negative metrics and limitations are recorded without a profitability claim.
- [x] With explicit authorization and an in-memory strategy-bound key, AlphaLitmus consumed all four read-only Nexus MCP evidence surfaces and correctly returned `INCONSISTENT` for a cross-instrument trade mismatch. The default remains disabled and secret-free.
- [ ] The live window-compute path has not run. It retains its separate switch and per-request confirmation and is not required for the read-only reconciliation above.
- [x] Container builds on the target Linux VPS from Python 3.12, runs non-root, serves health, and includes MCP runtime dependencies.
- [x] Public DNS, automatic TLS, HTTP-to-HTTPS redirect, edge body limit, security headers and reviewer access are exercised in safe-mode deployment without regressing APIVouch health.
- [ ] Caller authentication, per-principal quotas and retention controls are exercised before enabling live Nexus access or remote compute.
- [ ] Actual source/data/branding/dependency rights and official submission artifacts are completed by authorized owners.

The healthy container is publicly reachable through verified HTTPS in safe mode.
Final commit binding, official validator result, registration proof and rights
clearance remain pending. No Git initialization, commit, push or submission is
inferred. Legacy negative reports stay unchanged and labeled as described in
[BASELINE](BASELINE.md).

## Remaining Limits

- Nexus strategy and run identifiers plus one AlphaLitmus MCP snapshot have been captured, but metrics/signal lack run identifiers, trades are a 50-row recent subset versus the metric's 70, and Candidate v1 contains instruments outside the requested BTC pair. The EMA reference is separate and cannot validate the Nexus strategy. The opt-in window-stability path has never run against live Nexus; its fixtures are synthetic/documentation-derived and its reports cannot exceed `UNPROVEN`/`INCONSISTENT`.
- No complete metric/signal/run/window binding, attested closed-trade history or no-cash-flow proof. Numeric cross-surface comparisons remain insufficient even with equal values; explicit symbol/run contradictions still mismatch.
- No PSR, deflated Sharpe or selection-adjusted significance. Caller-declared variant counts do not repair selection bias; IID bootstrap and the 30-trade floor do not establish independence or future profit.
- No global multidimensional failure minimum. Cost/delay/EMA results are bounded grids and per-dimension discoveries, not a search over all joint perturbations.
- No selective sample exclusion to improve a result. Any out-of-domain bootstrap draw makes all bootstrap quantiles unavailable while other analyses remain; any replay cumulative or individual trade log return outside [-100,100] makes the entire reference analysis unavailable. Missing profit factors are never treated as passes, and later observed failures remain visible without a false bracket.
- No public source repository, official validator result, registration proof or final rights clearance yet. The public safe-mode deployment is intentionally unauthenticated because Nexus and remote compute are disabled; those capabilities must not be enabled without authentication and quotas.
