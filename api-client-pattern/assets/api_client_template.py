# Generic API Client Template

Use this template as a starting point for any external API client:

```python
# api_client.py — Adapt name and methods to your API
import requests
import os
from typing import Optional, Dict, Any

class MyServiceApiClient:
    """
    Generic client for MyService API.
    
    Usage:
        client = MyServiceApiClient(token=os.getenv("MY_API_KEY"))
        item = client.get_resource("123")
        result = client.create_resource({"name": "New Item"})
    """
    
    def __init__(self, token: str = None, base_url: str = None):
        self.token = token or os.getenv("MY_API_KEY")
        self.base_url = base_url or os.getenv("MY_API_URL", "https://api.example.com")
        
        if not self.token:
            raise ValueError("API token required: set MY_API_KEY env var or pass token=")
    
    def _headers(self) -> Dict[str, str]:
        """Standard auth headers"""
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }
    
    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Generic request with error handling"""
        url = f"{self.base_url}/{endpoint}"
        response = requests.request(method, url, headers=self._headers(), **kwargs)
        
        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            error_msg = response.json().get("message", str(e)) if response.text else str(e)
            raise ValueError(f"API error ({response.status_code}): {error_msg}") from e
        
        return response.json() if response.text else {}
    
    # --- Implement your API methods here ---
    
    def get_resource(self, resource_id: str) -> Dict[str, Any]:
        """Fetch resource by ID"""
        return self._request("GET", f"resources/{resource_id}")
    
    def create_resource(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new resource"""
        return self._request("POST", "resources", json=data)
    
    def update_resource(self, resource_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update resource"""
        return self._request("PATCH", f"resources/{resource_id}", json=updates)
    
    def delete_resource(self, resource_id: str) -> bool:
        """Delete resource"""
        self._request("DELETE", f"resources/{resource_id}")
        return True
```

**Adapt for your API:**
1. Rename `MyServiceApiClient`
2. Update `base_url` default
3. Replace `get_resource`, `create_resource`, etc. with your API's actual endpoints
4. Document expected env vars in project README

**Scripts using this client:**

```python
# script_example.py
import argparse
from api_client import MyServiceApiClient

parser = argparse.ArgumentParser()
parser.add_argument("--action", choices=["get", "create"], required=True)
parser.add_argument("--resource-id")
parser.add_argument("--data")
args = parser.parse_args()

client = MyServiceApiClient()

if args.action == "get":
    result = client.get_resource(args.resource_id)
    print(result)
elif args.action == "create":
    import json
    data = json.loads(args.data)
    result = client.create_resource(data)
    print(f"Created: {result['id']}")
```
