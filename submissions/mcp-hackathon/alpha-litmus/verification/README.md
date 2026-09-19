# AlphaLitmus verification evidence

## Prerequisites

- Review commit: `dc12a131aa454a8573a186cc234662bb8e03a437`
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
{"commit":"dc12a131aa454a8573a186cc234662bb8e03a437","commit_reviewable":true,"status":"ok","service":"alpha-litmus","no_execution":true,"provenance_basis":"syntax_only_not_authenticated"}
```

## 2. Deployment proof

```bash
curl --fail --silent --show-error https://alphalitmus.sklab.cc/.well-known/xagent-verification.json
```

Expected response:

```json
{"commit":"dc12a131aa454a8573a186cc234662bb8e03a437","commit_reviewable":true,"schemaVersion":1,"slug":"alpha-litmus","provenance_basis":"syntax_only_not_authenticated"}
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

## 4. Safe invalid-input behavior

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

## 5. Independent local replay

From the submitted `source/` directory, install the review environment and run all gates:

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
python -m ruff check .
python -m mypy app
python -m tools.local_smoke
```

The recorded reviewed-source results are 614 passing tests with zero failures and zero skips, Ruff clean, strict mypy clean across 16 source files, and a successful local smoke test discovering all six MCP tools. Run the commands again in the review environment rather than treating these recorded counts as current execution evidence.
