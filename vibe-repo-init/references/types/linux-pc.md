# Linux PC type playbook

## Basement goal

Runnable CLI or daemon stub with test hook.

## Ask (if unknown)

- Language preference (Python default if unspecified)
- CLI vs long-running service

## Create

- `src/` entrypoint (`main.py` / `main.go` / `main.rs`)
- `tests/` smoke test or placeholder
- Manifest: `pyproject.toml` / `go.mod` / `Cargo.toml`
- `scripts/run.sh` or documented `python -m` / `go run`
- `README.md` — install + run

## Hybrid notes

- Slice as `host/` when paired with firmware/server/UI
- Prefer talking to other slices via clear IPC (MQTT/HTTP/serial) documented in root README
