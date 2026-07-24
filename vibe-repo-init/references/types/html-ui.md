# HTML UI type playbook

## Basement goal

Openable page (static or Vite) with one clear entry.

## Ask (if unknown)

- Static files vs bundler (Vite)
- Talks to local server / device? (sets hybrid)

## Create

- `index.html` **or** `web/` with Vite scaffold (minimal)
- `package.json` only if bundler chosen
- Placeholder CSS; no card-heavy marketing chrome unless asked
- README — `npm install` / open file / `npm run dev`

## Hybrid notes

- Slice as `web/`
- Point API base URL at `.env.example` / config stub — never hardcode secrets
