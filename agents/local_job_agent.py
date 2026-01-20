from __future__ import annotations

from pathlib import Path
import sys
import yaml
from sources.indeed import IndeedSource
from sources.monster import MonsterSource
from sources.ziprecruiter import ZipRecruiterSource
import json
from datetime import datetime, timezone




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

def build_sources(enabled: list[str]):
    registry = {
        "indeed": IndeedSource,
        "monster": MonsterSource,
        "ziprecruiter": ZipRecruiterSource,
    }

    sources = []
    for name in enabled:
        cls = registry.get(name)
        if cls is None:
            print(f"WARNING: Unknown source '{name}' - skipping")
            continue
        sources.append(cls())
    return sources

def write_results(output_path: Path, payload: dict) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    config_path = repo_root / "config" / "config.yaml"

    try:
        cfg = load_config(config_path)
        print_run_plan(cfg)
        enabled = cfg.get("sources", {}).get("enabled", [])
        sources = build_sources(enabled)

        print("")
        print("Running sources (stubbed):")
        total = 0
        for src in sources:
            results = list(src.search())
            total += len(results)
            print(f"  - {src.name}: {len(results)} results")
        print(f"Total results: {total}")
        output_cfg = cfg.get("output", {})
        out_path = repo_root / output_cfg.get("path", "data/jobs.json")

        payload = {
            "run_utc": datetime.now(timezone.utc).isoformat(),
            "config": {
                "location": cfg.get("search", {}).get("location", {}),
                "max_results_per_source": cfg.get("search", {}).get("max_results_per_source"),
                "targets": cfg.get("targets", {}),
                "sources_enabled": enabled,
            },
            "results": [],
            "counts_by_source": {src.name: 0 for src in sources},
            "total_results": total,
        }

        write_results(out_path, payload)
        print(f"Wrote output file: {out_path}")

        return 0
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
