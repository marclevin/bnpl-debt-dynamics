---
name: datafirst
description: Interacts with the DataFirst UCT API to search, retrieve, and analyze dataset information.
---

# DataFirst CLI

## Quick start

- Code lives in `data.py`.
- Commands:
	- `python data.py search "keyword" [--limit N] [--page N] [--json] [-o FILE]`
	- `python data.py info "IDNO" [--json] [-o FILE]`
	- `python data.py variables "IDNO" [--json] [-o FILE]`

## AI usage

- Prefer `--json` for parsing stdout.
- Use `-o FILE` to persist raw JSON (parent dirs are auto-created).
- Check exit code; on failure, read stderr and retry with fixed args/path.


