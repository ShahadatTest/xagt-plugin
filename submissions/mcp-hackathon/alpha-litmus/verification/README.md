# AlphaLitmus verification evidence

## Prerequisites

- Review commit: `b8e87e207608b3540e73788589c24ddc9539198f`
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
{"commit":"b8e87e207608b3540e73788589c24ddc9539198f","commit_reviewable":true,"status":"ok","service":"alpha-litmus","no_execution":true,"provenance_basis":"syntax_only_not_authenticated"}
```

## 2. Deployment proof

```bash
curl --fail --silent --show-error https://alphalitmus.sklab.cc/.well-known/xagent-verification.json
```

Expected response:

```json
{"commit":"b8e87e207608b3540e73788589c24ddc9539198f","commit_reviewable":true,"schemaVersion":1,"slug":"alpha-litmus","provenance_basis":"syntax_only_not_authenticated"}
```

## 3. Real capability call

Run the complete bounded mixed-failure challenge against the deployed service:

```bash
curl --fail --silent --show-error https://alphalitmus.sklab.cc/v1/demo/mixed
```

The response is a complete `Report`. Verify these invariants rather than a creation timestamp:

- `verdict` is `UNPROVEN`;
- `observed_failures` contains six entries for the current fixture;
- `test_matrix` records observed, descriptive, and unavailable checks separately;
- `unavailable_tests` includes `trade_bootstrap`, `trade_permutation`, `selection_adjustment`, `nexus_strategy_replay`, and `reconciliation`;
- `nexus_validated`, `no_execution`, and `authenticity_claimed` are respectively `false`, `true`, and `false`;
- `provenance.commit` equals the review commit and `provenance.commit_reviewable` is `true`.

The dashboard at `https://alphalitmus.sklab.cc/` calls the same endpoint and renders the verdict, folds, cost frontier, parameter sensitivity, certificate, and limitations.

## 4. Safe invalid-input behavior

```bash
curl --silent --show-error --include \
  --request POST https://alphalitmus.sklab.cc/v1/challenge \
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

The recorded reviewed-source results are 562 passing tests with zero failures and zero skips, Ruff clean, strict mypy clean across 15 source files, and a successful local smoke test. Run the commands again in the review environment rather than treating these recorded counts as current execution evidence.
