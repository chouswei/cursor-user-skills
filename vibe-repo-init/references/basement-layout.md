# Shared basement layout

Create only what the matched type(s) need. Prefer ASCII paths.

## Always (any type)

```text
README.md           # purpose, how to build/run, type code(s)
.gitignore
LICENSE             # only if user wants
```

**Cursor (required):** see [cursor-basement.md](cursor-basement.md) — `AGENTS.md`, `.cursor/rules/`, **`.cursor/skills/`**, optional `.cursorignore`.

Optional when MemNet/serve used: `.memnet/` (empty ok).

## Single-type roots

| Type | Typical tree |
|------|----------------|
| `mcu` | `src/` `include/` `CMakeLists.txt` or `platformio.ini` `boards/` or `config/` |
| `linux-pc` | `src/` `tests/` `pyproject.toml` or `go.mod` / `Cargo.toml` `scripts/` |
| `online-server` | `src/` or `app/` `Dockerfile` `.env.example` `deploy/` |
| `html-ui` | `index.html` or `web/` `package.json` (if tooling) `public/` |
| `pc-ui` | `src/` toolkit project file `assets/` |

## Hybrid slices

```text
README.md                 # contract between slices
.gitignore
firmware/                 # mcu slice (if present)
server/                   # online-server slice
web/                      # html-ui slice
desktop/                  # pc-ui slice
host/                     # linux-pc CLI/daemon slice
docs/                     # short notes only
```

Name slices to match types present; omit unused dirs.

## README minimum

1. One-line purpose  
2. Type code(s)  
3. Build / flash / run commands  
4. Hybrid only: how slices talk (protocol + who owns config)

## Do not create in basement

- Full app features, sample business logic beyond hello/blink/ping
- Secrets, real endpoints, copied credentials
- Large vendored SDKs unless user asks (document clone steps instead)
