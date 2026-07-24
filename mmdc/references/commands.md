# mmdc commands and options

**Source:** [mermaid-cli](https://github.com/mermaid-js/mermaid-cli); run `mmdc -h` for full help.

## Commands

**Validate only (no output):**
```bash
mmdc -i diagram.mmd
```

**Render to SVG (default):**
```bash
mmdc -i diagram.mmd -o diagram.svg
```

**Render to PNG:**
```bash
mmdc -i diagram.mmd -o diagram.png
```

**Render to PDF:**
```bash
mmdc -i diagram.mmd -o diagram.pdf
```

## Options

| Option | Short | Purpose | Default |
|--------|-------|---------|---------|
| `--input` | `-i` | Input .mmd file | (required) |
| `--output` | `-o` | Output path | input + .svg |
| `--theme` | `-t` | Theme | default (also: forest, dark, neutral) |
| `--backgroundColor` | `-b` | Background | white (or transparent, #hex) |
| `--width` | `-w` | Page width (px) | 800 |
| `--height` | `-H` | Page height (px) | 600 |
| `--configFile` | `-c` | Mermaid JSON config | — |
| `--puppeteerConfigFile` | `-p` | Puppeteer JSON | — |

## Examples
```bash
mmdc -i in.mmd -o out.svg -t dark -b transparent
mmdc -i in.mmd -o out.png -w 1200 -H 800
```

## Common errors
- **Parse error on line X** → Check syntax at that line; quotes for labels with spaces; arrow types; node shapes.
- **Cannot find module** → `npm install -g @mermaid-js/mermaid-cli`
- **Puppeteer/Chrome** → mmdc uses Puppeteer; ensure Node.js and npm work.

**Retrieval seeds:** mmdc, mermaid-cli, validate mermaid, render mermaid, mmdc options, mermaid CLI
