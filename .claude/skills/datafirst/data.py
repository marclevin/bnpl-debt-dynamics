"""
DataFirst UCT catalog tool.

Usage:
    python data.py search "keyword" [--limit N] [--page N] [-o FILE]
    python data.py info "IDNO" [-o FILE]
    python data.py variables "IDNO" [-o FILE]
"""

import os
import sys
import json
import argparse

from dotenv import load_dotenv
import requests

load_dotenv()

BASE_URL = "https://www.datafirst.uct.ac.za/dataportal/index.php/api"
HEADERS = {"X-API-KEY": os.getenv("DATAFIRST_KEY")}


def search(keyword: str, limit: int = 10, page: int = 1) -> dict:
    """Search the DataFirst catalog by keyword."""
    params = {
        "sk": keyword,
        "ps": limit,
        "from": (page - 1) * limit,
    }
    resp = requests.get(f"{BASE_URL}/catalog/search", headers=HEADERS, params=params)
    resp.raise_for_status()
    return resp.json()


def get_study(idno: str) -> dict:
    """Fetch full metadata for a study by its ID number."""
    resp = requests.get(f"{BASE_URL}/catalog/{idno}", headers=HEADERS)
    resp.raise_for_status()
    return resp.json()


def get_variables(idno: str) -> dict:
    """Fetch variable-level metadata for a study."""
    resp = requests.get(f"{BASE_URL}/catalog/{idno}/variables", headers=HEADERS)
    resp.raise_for_status()
    return resp.json()


def _print_search_results(data: dict) -> None:
    result = data.get("result", {})
    found = result.get("found", data.get("found", 0))
    studies = result.get("rows", data.get("studies", []))
    print(f"Found {found} result(s). Showing {len(studies)}:\n")
    for s in studies:
        idno = s.get("idno", "?")
        title = s.get("title", "Untitled")
        year = s.get("year_start", "")
        nation = s.get("nation", "")
        print(f"  [{idno}] {title} ({nation}, {year})")


def _write_json_output(data: dict, output_path: str) -> None:
    """Write JSON data to a file path, creating parent directories if needed."""
    parent = os.path.dirname(output_path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def main():
    parser = argparse.ArgumentParser(description="Query the DataFirst UCT data catalog.")
    sub = parser.add_subparsers(dest="cmd", required=True)

    # search subcommand
    p_search = sub.add_parser("search", help="Search for datasets by keyword")
    p_search.add_argument("keyword", help="Search term")
    p_search.add_argument("--limit", type=int, default=10, help="Results per page (default 10)")
    p_search.add_argument("--page", type=int, default=1, help="Page number (default 1)")
    p_search.add_argument("--json", action="store_true", help="Output raw JSON")
    p_search.add_argument("-o", "--output", help="Write raw JSON output to a file")

    # info subcommand
    p_info = sub.add_parser("info", help="Get full metadata for a study")
    p_info.add_argument("idno", help="Study ID number (e.g. ZA-STATSSA-CEN-2011)")
    p_info.add_argument("--json", action="store_true", help="Output raw JSON")
    p_info.add_argument("-o", "--output", help="Write raw JSON output to a file")

    # variables subcommand
    p_vars = sub.add_parser("variables", help="List variables for a study")
    p_vars.add_argument("idno", help="Study ID number")
    p_vars.add_argument("--json", action="store_true", help="Output raw JSON")
    p_vars.add_argument("-o", "--output", help="Write raw JSON output to a file")

    args = parser.parse_args()

    try:
        if args.cmd == "search":
            data = search(args.keyword, limit=args.limit, page=args.page)
            if args.output:
                _write_json_output(data, args.output)
                print(f"Wrote JSON to {args.output}")
            if args.json:
                print(json.dumps(data, indent=2))
            else:
                _print_search_results(data)

        elif args.cmd == "info":
            data = get_study(args.idno)
            if args.output:
                _write_json_output(data, args.output)
                print(f"Wrote JSON to {args.output}")
            if args.json:
                print(json.dumps(data, indent=2))
            else:
                study = data.get("dataset", data)
                print(json.dumps(study, indent=2))

        elif args.cmd == "variables":
            data = get_variables(args.idno)
            if args.output:
                _write_json_output(data, args.output)
                print(f"Wrote JSON to {args.output}")
            if args.json:
                print(json.dumps(data, indent=2))
            else:
                variables = data.get("variables", data.get("variable", []))
                for v in variables[:50]:
                    name = v.get("name", "?")
                    label = v.get("labl", v.get("label", ""))
                    print(f"  {name:20s} {label}")
                if len(variables) > 50:
                    print(f"  ... and {len(variables) - 50} more (use --json for full list)")

    except requests.HTTPError as e:
        print(f"API error: {e.response.status_code} - {e.response.text}", file=sys.stderr)
        sys.exit(1)
    except OSError as e:
        print(f"File write error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
