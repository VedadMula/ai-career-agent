from __future__ import annotations

from pathlib import Path
import sys
import yaml
from sources.indeed import IndeedSource
from sources.monster import MonsterSource
from sources.ziprecruiter import ZipRecruiterSource
import json
from datetime import datetime, timezone
from sources.mock import MockSource





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
        "mock": MockSource,
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

def dedupe_by_url(jobs: list) -> list:
    seen = set()
    unique = []
    for job in jobs:
        url = getattr(job, "url", None)
        if not url or url in seen:
            continue
        seen.add(url)
        unique.append(job)
    return unique

def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    config_path = repo_root / "config" / "config.yaml"

    try:
        cfg = load_config(config_path)
        print_run_plan(cfg)
        enabled = cfg.get("sources", {}).get("enabled", [])
        sources = build_sources(enabled)

        print("")
        print("Running sources:")
        all_results = []
        counts = {}

        for src in sources:
            results = list(src.search())
            counts[src.name] = len(results)
            all_results.extend(results)
            print(f"  - {src.name}: {len(results)} results")

        unique_results = dedupe_by_url(all_results)
        total = len(unique_results)
        print(f"Total unique results: {total}")

        results_payload = [
            {
                "source": r.source,
                "title": r.title,
                "company": r.company,
                "location": r.location,
                "url": r.url,
                "date_found": r.date_found.isoformat() if hasattr(r.date_found, "isoformat") else str(r.date_found),
                "distance_miles": r.distance_miles,
                "description_snippet": r.description_snippet,
            }
            for r in unique_results
        ]

        payload = {
            "run_utc": datetime.now(timezone.utc).isoformat(),
            "config": {
                "location": cfg.get("search", {}).get("location", {}),
                "max_results_per_source": cfg.get("search", {}).get("max_results_per_source"),
                "targets": cfg.get("targets", {}),
                "sources_enabled": enabled,
            },
            "results": results_payload,
            "counts_by_source": counts,
            "total_results": total,
        }
        output_cfg = cfg.get("output", {})
        out_path = repo_root / output_cfg.get("path", "data/jobs.json")
        
        write_results(out_path, payload)
        print(f"Wrote output file: {out_path}")

        return 0
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
