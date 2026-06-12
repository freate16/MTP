from __future__ import annotations

import argparse
import json
import pickle
import re
import shutil
from pathlib import Path


TOKEN_RE = re.compile(r"[A-Za-z0-9_./+-]+")


def require_dependencies() -> None:
    missing: list[str] = []
    try:
        import faiss  # noqa: F401
    except Exception:
        missing.append("faiss-cpu")
    try:
        import sentence_transformers  # noqa: F401
    except Exception:
        missing.append("sentence-transformers")
    try:
        import rank_bm25  # noqa: F401
    except Exception:
        missing.append("rank-bm25")
    if missing:
        raise SystemExit(
            "Missing dependencies: "
            + ", ".join(missing)
            + "\nInstall them with: pip install -r rag/requirements-rag.txt"
        )


def load_chunks(path: Path) -> list[dict]:
    chunks: list[dict] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                chunks.append(json.loads(line))
    if not chunks:
        raise ValueError(f"No chunks found in {path}")
    return chunks


def tokenize_for_bm25(text: str) -> list[str]:
    return [token.lower() for token in TOKEN_RE.findall(text)]


def save_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def build_dense_index(chunks: list[dict], model_name: str, batch_size: int, index_dir: Path) -> tuple[int, int]:
    import faiss
    import numpy as np
    from sentence_transformers import SentenceTransformer

    try:
        model = SentenceTransformer(model_name, trust_remote_code=True)
    except TypeError:
        model = SentenceTransformer(model_name)

    texts = [chunk["text"] for chunk in chunks]
    embeddings = model.encode(
        texts,
        batch_size=batch_size,
        normalize_embeddings=True,
        show_progress_bar=True,
        convert_to_numpy=True,
    ).astype("float32")

    if embeddings.ndim != 2:
        raise ValueError(f"Expected 2D embeddings, got shape {embeddings.shape}")

    dimension = int(embeddings.shape[1])
    index = faiss.IndexFlatIP(dimension)
    index.add(embeddings)
    faiss.write_index(index, str(index_dir / "dense.faiss"))
    np.save(index_dir / "embeddings.npy", embeddings)
    return len(chunks), dimension


def build_bm25_index(chunks: list[dict], index_dir: Path) -> None:
    from rank_bm25 import BM25Okapi

    tokenized_corpus = [tokenize_for_bm25(chunk["text"]) for chunk in chunks]
    bm25 = BM25Okapi(tokenized_corpus)
    with (index_dir / "bm25.pkl").open("wb") as handle:
        pickle.dump(
            {
                "bm25": bm25,
                "tokenized_corpus": tokenized_corpus,
            },
            handle,
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build dense BGE-M3 + BM25 indexes for Markdown RAG chunks.")
    parser.add_argument("--chunks", type=Path, default=Path("rag/artifacts/chunks.jsonl"))
    parser.add_argument("--index-dir", type=Path, default=Path("rag/index"))
    parser.add_argument("--model-name", default="BAAI/bge-m3")
    parser.add_argument("--batch-size", type=int, default=8)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    require_dependencies()
    args.index_dir.mkdir(parents=True, exist_ok=True)

    chunks = load_chunks(args.chunks)
    shutil.copyfile(args.chunks, args.index_dir / "chunks.jsonl")
    chunk_count, dimension = build_dense_index(chunks, args.model_name, args.batch_size, args.index_dir)
    build_bm25_index(chunks, args.index_dir)

    manifest = {
        "model_name": args.model_name,
        "chunk_count": chunk_count,
        "embedding_dimension": dimension,
        "dense_index": "dense.faiss",
        "bm25_index": "bm25.pkl",
        "chunks": "chunks.jsonl",
    }
    save_json(args.index_dir / "manifest.json", manifest)
    print(json.dumps({"index_dir": str(args.index_dir), **manifest}, indent=2))


if __name__ == "__main__":
    main()
