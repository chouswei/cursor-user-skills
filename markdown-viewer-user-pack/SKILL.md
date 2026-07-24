---
name: markdown-viewer-user-pack
description: >-
  Run Markdown Viewer as a local user-pack tool for markdown and Mermaid
  inspection with zoom, pan, and export. Use when preview readability is poor or
  when the user asks to inspect or export Mermaid diagrams.
metadata:
  pattern: tool-wrapper
  version: "1.0"
---

# Markdown Viewer User Pack Tool

## Start

```powershell
docker run -d --name markdown-viewer -p 8080:80 --restart unless-stopped ghcr.io/thisis-developer/markdown-viewer:latest
```

Open: `http://localhost:8080`

## Operate

```powershell
docker ps --filter "name=markdown-viewer"
docker stop markdown-viewer
docker start markdown-viewer
docker rm -f markdown-viewer
```

## Apply

- Load `.md` files and inspect Mermaid with zoom/pan.
- Export SVG/PNG from the viewer when needed.
- If `8080` is occupied, use another host port (`-p 18080:80`).
