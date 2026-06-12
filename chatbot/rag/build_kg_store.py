from __future__ import annotations

import argparse
import json
from pathlib import Path

from kg_store import KgStore


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a persistent Oxigraph SPARQL store from the GLOF TTL file.")
    parser.add_argument("--ttl", type=Path, default=Path("graphrag/glof_kg_populated_codex.ttl"))
    parser.add_argument("--store-dir", type=Path, default=Path("rag/kg_store"))
    parser.add_argument("--force", action="store_true", help="Delete and rebuild the existing store directory.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    manifest = KgStore.build(args.ttl, args.store_dir, force=args.force)
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
