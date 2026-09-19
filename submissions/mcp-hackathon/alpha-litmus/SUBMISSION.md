# AlphaLitmus

## Capability

- **One-line description:** Falsify a trading-strategy claim with bounded stress tests, find its first observed failure boundaries, and return an independently replayable evidence certificate.
- **Who it helps:** Trading agents, strategy researchers, and reviewers who need to challenge a strategy before capital is exposed.
- **Capability boundary:** AlphaLitmus replays a fixed reference strategy against costs, execution delay, chronological folds, parameter perturbations, bootstrap diagnostics, and market regimes. It can also reconcile separately authorized OlaXBT Nexus evidence and can optionally request bounded Nexus backtest windows, but the public review deployment keeps all Nexus access disabled. It never places orders, signs wallets, predicts profit, promotes a strategy to live trading, or treats a synthetic fixture as market evidence.

## Live API

- **API base URL:** https://alphalitmus.sklab.cc
- **Health-check URL:** https://alphalitmus.sklab.cc/health
- **Authentication:** None for the public safe-mode review deployment. Nexus reads and remote backtest compute are disabled.
- **Rate limits / known limits:** JSON bodies are limited to 4,000,000 bytes and depth 32. Each process admits at most eight intake requests and two expensive operations; body receipt has a 10-second deadline. Reviewers should avoid load testing.
- **API contract:** Interactive OpenAPI is at https://alphalitmus.sklab.cc/docs, the machine-readable contract is at https://alphalitmus.sklab.cc/openapi.json, and the implementation is in `source/app/`. A local stdio MCP server exposes the five tools documented in `source/README.md`.

## Source and reproducibility

- **Source repository:** https://github.com/ShahadatTest/alpha-litmus
- **Review commit:** `b8e87e207608b3540e73788589c24ddc9539198f`
- **Source submitted in this PR:** `source/`
- **Run tests:** `python -m pip install -r requirements-dev.txt && python -m pytest -q && python -m ruff check . && python -m mypy app`
- **Run locally:** `python -m pip install -r requirements.txt && python -m uvicorn app.main:app --host 127.0.0.1 --port 8040`
- **Deploy:** `docker build --build-arg ALPHALITMUS_COMMIT=b8e87e207608b3540e73788589c24ddc9539198f -t alpha-litmus .` followed by a hardened container run with `ALPHALITMUS_ENV=production`; the exact production controls are in `source/docs/VPS-DEPLOYMENT.md`.
- **Version binding:** The image is built from `git archive` of the review commit with the same commit passed as `ALPHALITMUS_COMMIT`. Both public health and same-origin proof expose it. The response also states that syntax is not independent build attestation.

The deployed API exposes:

```json
{"commit":"b8e87e207608b3540e73788589c24ddc9539198f","commit_reviewable":true,"status":"ok","service":"alpha-litmus","no_execution":true,"provenance_basis":"syntax_only_not_authenticated"}
```

```json
{"commit":"b8e87e207608b3540e73788589c24ddc9539198f","commit_reviewable":true,"schemaVersion":1,"slug":"alpha-litmus","provenance_basis":"syntax_only_not_authenticated"}
```

## Verification

The exact public calls, expected invariants, and safe failure behavior are in `verification/README.md`.

- **Health-check result:** Public HTTPS returns HTTP 200, `status: ok`, and the exact review commit.
- **Capability call:** `GET /v1/demo/mixed` performs the complete bounded synthetic challenge. The verified public run returned `UNPROVEN`, reported six observed failures, and identified unavailable evidence instead of claiming a profitable edge.
- **Expected error behavior:** A schema-invalid challenge such as `{}` returns HTTP 422 with the bounded body `{"detail":"INVALID_REQUEST"}`. Missing Nexus access returns an evidence-labelled unavailable result; it is not converted into validation.

## Security and data handling

- **Data collected:** Challenge requests and generated reports are processed in memory. The service has no report-list or persisted report-retrieval API. A returned/exported report contains the caller's submitted research data, so callers must review it before sharing.
- **Purpose and retention:** Inputs are used only to compute the requested analysis and response. The submitted implementation does not provide application-level persistence or a retention guarantee; reverse-proxy/container logs may retain ordinary request metadata under operator policy.
- **Third parties / outbound network calls:** The public deployment makes no Nexus calls because both Nexus switches are disabled. Optional Nexus operations contact only the fixed OlaXBT Nexus MCP endpoint when an operator separately enables them and injects an authorized strategy-bound key. The optional historical-data tool contacts Binance and is not part of the public demo path.
- **Secrets:** No secrets are committed. The public demo needs none. A Nexus key, if ever enabled, must be injected outside source and capability routes must first be protected by authentication and quotas.
- **Known risks / restrictions:** The public safe-mode routes are unauthenticated and are not intended for confidential data. Synthetic results are test fixtures, hashes prove integrity rather than authenticity, and bounded survival is not evidence of future profitability. The optional remote-compute tool has side effects (backtest submission, never trading) and must not be retried automatically.

## Support

- **Team / builder:** Shahadat Islam / SKLab Studio; GitHub submission account `@ShahadatTest`
- **Contact:** https://github.com/ShahadatTest
- **License / rights:** First-party source is submitted under the program review and archive authorization in `RIGHTS.md`; no broader open-source license is asserted. Third-party dependencies and services remain under their own terms.
