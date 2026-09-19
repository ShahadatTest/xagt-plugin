# AlphaLitmus verification evidence

**Track:** OlaXBT × X-Agent Trading Challenge

## Prerequisites

- Review commit: `dd4f2e85f1c77435793012d6f52738952566e341`
- API base URL: `https://alphalitmus.sklab.cc`
- Authentication: None for the public safe-mode deployment. Nexus access is disabled and no key is needed.
- Tool: `curl`

The built-in demo uses synthetic data and must remain `UNPROVEN`; it is a repeatable capability exercise, not a profitable-strategy claim.

## 1. Health check

```bash
curl --fail --silent --show-error https://alphalitmus.sklab.cc/health
```

Expected response:

```json
{"commit":"dd4f2e85f1c77435793012d6f52738952566e341","commit_reviewable":true,"status":"ok","service":"alpha-litmus","no_execution":true,"provenance_basis":"syntax_only_not_authenticated"}
```

## 2. Deployment proof

```bash
curl --fail --silent --show-error https://alphalitmus.sklab.cc/.well-known/xagent-verification.json
```

Expected response:

```json
{"commit":"dd4f2e85f1c77435793012d6f52738952566e341","commit_reviewable":true,"schemaVersion":1,"slug":"alpha-litmus","provenance_basis":"syntax_only_not_authenticated"}
```

## 3. Real capability call

Run the agent-facing release gate against the deployed service. It executes the
complete bounded mixed-failure challenge, verifies the source certificate, and
returns the decision contract plus the authoritative report:

```bash
curl --fail --silent --show-error https://alphalitmus.sklab.cc/v1/release-gate/demo/mixed
```

Verify these invariants rather than a creation timestamp:

- `schema_version` is `alphalitmus-release-gate-1`;
- `decision` is `INSUFFICIENT_EVIDENCE` and `recommended_action` is `COLLECT_MORE_EVIDENCE`;
- `source_verdict` is `UNPROVEN` and `evidence_classification` is `synthetic_reference`;
- `source_report_verified` and `no_execution` are exactly `true`, while `profitability_claimed` is `false`;
- `report_id` equals `canonical_report_hash`;
- the embedded `report.observed_failures` contains six entries for the current fixture;
- the embedded `report.provenance.commit` equals the review commit and `commit_reviewable` is `true`.

The dashboard at `https://alphalitmus.sklab.cc/` calls the same endpoint and renders the verdict, folds, cost frontier, parameter sensitivity, certificate, and limitations.

## 4. Recorded Nexus evidence replay

```bash
curl --fail --silent --show-error https://alphalitmus.sklab.cc/v1/nexus/replay/candidate-v1
```

Verify these invariants:

- `snapshot_id` is `candidate-v1`, and the aggregate snapshot SHA-256 is `3a086a1cbf392d15ae961227c091afa343fde5f21b3aebc2aa81ff9d33b389f8`;
- the four evidence surfaces are `signal`, `metrics`, `equity`, and `trades`;
- `historical` and `no_execution` are exactly `true`; `live` and `profitability_claimed` are exactly `false`;
- the release gate is `INCONSISTENT`, `BLOCK_DEPLOYMENT`, and `DO_NOT_DEPLOY` with exact-true `source_report_verified`;
- `TRADE_SYMBOLS` is a `MISMATCH` because recent trades include a symbol outside the requested strategy symbol;
- the disclosure says this is recorded historical evidence, not a live call, independent source authentication, or future-profit evidence.

This route uses no Nexus key and performs no live Nexus request. Hashes establish source-commit-bound content consistency, not authorship or source authenticity.

## 5. Safe invalid-input behavior

```bash
curl --silent --show-error --include \
  --request POST https://alphalitmus.sklab.cc/v1/release-gate \
  --header 'content-type: application/json' \
  --data '{}'
```

Expected status is HTTP 422 and the bounded response is:

```json
{"detail":"INVALID_REQUEST"}
```

The error does not echo the invalid body or expose an exception trace. A valid Nexus-mode request while public Nexus access is disabled returns an evidence-labelled unavailable result rather than making an outbound call or treating missing evidence as success.

## 6. Independent local replay

From the submitted `source/` directory, install the review environment and run all gates:

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
python -m ruff check .
python -m mypy app
python -m tools.local_smoke
```

The recorded reviewed-source results are 664 passing tests with zero failures and zero skips, Ruff clean, strict mypy clean across 17 source files, and a successful local smoke test discovering all seven MCP tools. Run the commands again in the review environment rather than treating these recorded counts as current execution evidence.
