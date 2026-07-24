# Online server type playbook

## Basement goal

One health endpoint or worker loop + env template + optional container stub.

## Ask (if unknown)

- HTTP API vs worker vs MQTT client/broker-side
- Deploy target (local Docker, VPS, PaaS)

## Create

- `src/` or `app/` — minimal server (e.g. `/healthz`)
- `.env.example` — names only, no secrets
- `Dockerfile` (optional) + `.dockerignore`
- `deploy/README.md` — one paragraph deploy sketch
- Root/server `README.md` — run locally

## Hybrid notes

- Slice as `server/`
- Document ports and protocols for MCU/UI clients
- Use [api-client-pattern](../../api-client-pattern/SKILL.md) only if adding a typed client package
