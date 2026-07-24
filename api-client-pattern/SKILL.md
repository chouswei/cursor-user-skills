---
name: api-client-pattern
description: >-
  Design generic, reusable Python API clients and scripts: shared helpers, parameterized entrypoints, no duplication.
  Triggers: API design, generic client, shared helpers, parameterized API script, avoid copy-paste, reusable functions.
metadata:
  pattern: generator
  domain: code
  applies_to: sysml-v2-models/integrations or similar
  token_focus: high

---

# API Client Pattern Generator

When writing Python that calls external APIs (REST, gRPC, etc.), **design for generality** to reduce duplication and token usage.

## Problem

**Bad (Scattered duplication):**
```python
# script_a.py
token = os.getenv("API_KEY")
url = "https://api.example.com/items"
response = requests.get(f"{url}/123", headers={"Authorization": f"Bearer {token}"})

# script_b.py  (same pattern repeated)
token = os.getenv("API_KEY")
url = "https://api.example.com/items"
response = requests.post(f"{url}/new", headers={"Authorization": f"Bearer {token}"}, json={...})
```

**Result:** Token bloat for AI when reading/generating; manual sync burden when URL changes; scattered hardcoded IDs.

---

## Solution: Shared Client Pattern

### Step 1: Extract Shared Client

Create one module (e.g., `api_client.py`) with:
- Auth logic (token, headers)
- Base URL and request helpers
- Common methods (get, post, update, delete)

```python
# api_client.py
import requests
import os

class ItemsApiClient:
    def __init__(self, token: str = None):
        self.token = token or os.getenv("API_KEY")
        if not self.token:
            raise ValueError("API_KEY not set")
        self.base_url = "https://api.example.com/items"
    
    def _headers(self):
        return {"Authorization": f"Bearer {self.token}"}
    
    def get_item(self, item_id: str) -> dict:
        """Fetch item by ID"""
        url = f"{self.base_url}/{item_id}"
        response = requests.get(url, headers=self._headers())
        response.raise_for_status()
        return response.json()
    
    def create_item(self, data: dict) -> dict:
        """Create new item"""
        response = requests.post(self.base_url, headers=self._headers(), json=data)
        response.raise_for_status()
        return response.json()
    
    def update_item(self, item_id: str, updates: dict) -> dict:
        """Update item"""
        url = f"{self.base_url}/{item_id}"
        response = requests.patch(url, headers=self._headers(), json=updates)
        response.raise_for_status()
        return response.json()
```

### Step 2: Parameterized Scripts

Create thin scripts that take arguments and use the client:

```python
# script_a.py — Fetch item
import argparse
from api_client import ItemsApiClient

parser = argparse.ArgumentParser()
parser.add_argument("--item-id", required=True)
args = parser.parse_args()

client = ItemsApiClient()
item = client.get_item(args.item_id)
print(item)
```

```python
# script_b.py — Create item
import argparse
import json
from api_client import ItemsApiClient

parser = argparse.ArgumentParser()
parser.add_argument("--data-file", required=True)
args = parser.parse_args()

data = json.load(open(args.data_file))
client = ItemsApiClient()
result = client.create_item(data)
print(f"Created: {result['id']}")
```

### Step 3: Config & Environment

Read IDs, endpoints, tokens from env or config (not scattered in code):

```python
# Read from environment
import os
API_KEY = os.getenv("MY_API_KEY")
BASE_URL = os.getenv("MY_API_URL", "https://api.example.com")

# Or from config (gitignored)
import json
config = json.load(open("api_config.json"))  # .gitignore: api_config.json
API_KEY = config["api_key"]
BASE_URL = config["base_url"]
```

### Step 4: Reusable Helper Functions

Extract patterns into callable functions:

```python
# api_common.py — shared helpers for multiple clients
def read_api_config(path: str) -> dict:
    """Read gitignored config file"""
    import json
    return json.load(open(path))

def create_api_session(token: str) -> requests.Session:
    """Create authenticated session"""
    session = requests.Session()
    session.headers.update({"Authorization": f"Bearer {token}"})
    return session

def handle_api_error(response) -> None:
    """Raise human-readable error"""
    try:
        response.raise_for_status()
    except requests.HTTPError as e:
        error_msg = response.json().get("message", str(e))
        raise ValueError(f"API error: {error_msg}") from e
```

Then import and reuse in multiple client modules.

---

## Benefits

| Benefit | Impact |
|---------|--------|
| **One place to edit** | Change URL → update in one place, not 5 scripts |
| **Smaller AI context** | Agent reads 50 lines (client) instead of 200 (scattered code) |
| **Reusable functions** | New script doesn't copy logic; just imports and calls |
| **Easier testing** | Unit test client once; all scripts benefit |
| **Config centralization** | No hardcoded IDs or URLs in source; all in env/config |

---

## Do & Avoid

| ✓ Do | ✗ Avoid |
|-----|---------|
| **Shared client class** with auth, headers, common methods | One-off scripts duplicating auth logic |
| **Parameterized scripts** (args, config, env) | Hardcoded IDs and URLs |
| **One module per API** (e.g., `items_client.py`, `tasks_client.py`) | Copy-paste blocks across files |
| **Config + env for secrets** (gitignored) | Token literals in source code |
| **Extracted helpers** for common patterns | Monolithic scripts doing everything |

---

## Example: Complete Project

```
integrations/
├── api_client.py          # Shared client (ItemsApiClient)
├── api_common.py          # Shared helpers (sessions, auth, error handling)
├── fetch_item.py          # Thin script: args → client.get_item()
├── create_item.py         # Thin script: args → client.create_item()
├── api_config.json.example # Template (actual config is gitignored)
└── README.md              # Documents API_KEY env var, config format
```

**Token efficiency:** Agent reads ~100 lines total (client + one script). No duplication, no redundancy.

---

## Cross-references

- **Secrets & env vars:** See your project's `no-secrets.mdc`
- **General workflow:** [workflow.mdc](~/.cursor/rules/workflow.mdc)
- **Token efficiency:** User pack [AGENTS.md](~/.cursor/skills/AGENTS.md) or project-specific rules
