# AlphaLitmus VPS deployment

The checked-in Compose configuration intentionally deploys the public synthetic
demo with Nexus reads and remote compute disabled. It never accepts a Nexus key.

From the project root on the VPS:

```sh
ALPHALITMUS_COMMIT=local-dev ALPHALITMUS_ENV=development \
  docker compose -f deploy/compose.yml up -d --build
```

The service joins the existing external Docker network `apivouch_edge` and is
not published on a host port. Merge `Caddyfile.alphalitmus` into the existing
Caddy configuration, validate it, and reload Caddy. DNS must map
`alphalitmus.sklab.cc` to the VPS before Caddy can obtain its certificate.

This pre-public-commit deployment must report `local-dev` and
`commit_reviewable: false`. After GitHub is restored, rebuild from the reviewed
source using its exact nonzero lowercase 40-character commit and
`ALPHALITMUS_ENV=production`, then confirm health and proof expose the same
commit.

Do not enable Nexus on this public configuration. A later live-review deployment
requires TLS, authentication, external secret injection, explicit quotas and a
separate operator decision. Remote backtest compute remains disabled unless all
of its documented gates are deliberately enabled.
