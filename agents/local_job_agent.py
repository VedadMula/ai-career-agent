from __future__ import annotations

from pathlib import Path
import sys
import yaml


def load_config(config_path: Path) -> dict:
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with config_path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    if not isinstance(data, dict):
        raise ValueError("Config file did not parse into a dictionary.")
    return data


def print_run_plan(cfg: dict) -> None:
    project = cfg.get("project", {})
    search = cfg.get("search", {})
    location = search.get("location", {})
    targets = cfg.get("targets", {})
    sources = cfg.get("sources", {})
    output = cfg.get("output", {})

    print("=== AI Career Agent: Local Job Search (dry run) ===")
    print(f"Project: {project.get('name')} | Agent: {project.get('agent')} | Version: {project.get('version')}")
    print("")
    print("Search:")
    print(f"  Location: {location.get('city')}, {location.get('state')} {location.get('country')}")
    print(f"  Radius (miles): {location.get('radius_miles')}")
    print(f"  Max results per source: {search.get('max_results_per_source')}")
    print("")
    print("Targets:")
    print(f"  Keywords: {', '.join(targets.get('keywords', []))}")
    print(f"  Titles: {', '.join(targets.get('titles', []))}")
    print("")
    print("Sources enabled:")
    for s in sources.get("enabled", []):
        print(f"  - {s}")
    print("")
    print("Output:")
    print(f"  Format: {output.get('format')}")
    print(f"  Path: {output.get('path')}")
    print("===============================================")


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    config_path = repo_root / "config" / "config.yaml"

    try:
        cfg = load_config(config_path)
        print_run_plan(cfg)
        return 0
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
