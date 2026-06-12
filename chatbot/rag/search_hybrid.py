from __future__ import annotations

import argparse
import json
import pickle
import re
from pathlib import Path


TOKEN_RE = re.compile(r"[A-Za-z0-9_./+-]+")


def require_dependencies(use_reranker: bool) -> None:
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
    if use_reranker:
        try:
            from sentence_transformers import CrossEncoder  # noqa: F401
        except Exception:
            missing.append("sentence-transformers[cross-encoder]")
    if missing:
        raise SystemExit(
            "Missing dependencies: "
            + ", ".join(missing)
            + "\nInstall them with: pip install -r rag/requirements-rag.txt"
        )


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_chunks(path: Path) -> list[dict]:
    chunks: list[dict] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                chunks.append(json.loads(line))
    return chunks


def tokenize_for_bm25(text: str) -> list[str]:
    return [token.lower() for token in TOKEN_RE.findall(text)]


def minmax(scores: dict[int, float]) -> dict[int, float]:
    if not scores:
        return {}
    values = list(scores.values())
    low = min(values)
    high = max(values)
    if high == low:
        return {idx: 1.0 for idx in scores}
    return {idx: (score - low) / (high - low) for idx, score in scores.items()}


def load_bm25(index_dir: Path):
    with (index_dir / "bm25.pkl").open("rb") as handle:
        payload = pickle.load(handle)
    return payload["bm25"]


def dense_search(index_dir: Path, query: str, model_name: str, top_k: int) -> dict[int, float]:
    import faiss
    import os
    import requests
    import numpy as np
    
    token = os.getenv("HF_TOKEN") or os.getenv("HUGGINGFACEHUB_API_TOKEN") or os.getenv("HUGGINGFACE_API_KEY")
    if not token:
        raise SystemExit("Missing HF token for embedding API. Put HF_TOKEN=... in .env")

    api_url = f"https://api-inference.huggingface.co/pipeline/feature-extraction/{model_name}"
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.post(api_url, headers=headers, json={"inputs": [query]})
    if response.status_code != 200:
        raise RuntimeError(f"Embedding API failed: {response.text}")
    
    # Response is typically a nested list
    embedding_data = response.json()
    if isinstance(embedding_data, list) and isinstance(embedding_data[0], list):
        embedding = np.array(embedding_data[0], dtype="float32")
    else:
        embedding = np.array(embedding_data, dtype="float32")
        
    norm = np.linalg.norm(embedding)
    if norm > 0:
        embedding = embedding / norm

    query_embedding = np.expand_dims(embedding, axis=0)

    index = faiss.read_index(str(index_dir / "dense.faiss"))
    scores, ids = index.search(query_embedding, top_k)
    return {int(idx): float(score) for idx, score in zip(ids[0], scores[0]) if idx >= 0}


def bm25_search(index_dir: Path, query: str, top_k: int) -> dict[int, float]:
    import numpy as np

    bm25 = load_bm25(index_dir)
    scores = bm25.get_scores(tokenize_for_bm25(query))
    if len(scores) == 0:
        return {}
    top_ids = np.argsort(scores)[::-1][:top_k]
    return {int(idx): float(scores[idx]) for idx in top_ids if scores[idx] > 0}


def hybrid_search(
    index_dir: Path,
    query: str,
    model_name: str,
    dense_top_k: int,
    bm25_top_k: int,
    alpha: float,
) -> list[tuple[int, float, float, float]]:
    dense_scores = dense_search(index_dir, query, model_name, dense_top_k)
    bm25_scores = bm25_search(index_dir, query, bm25_top_k)
    dense_norm = minmax(dense_scores)
    bm25_norm = minmax(bm25_scores)

    candidate_ids = set(dense_norm) | set(bm25_norm)
    merged: list[tuple[int, float, float, float]] = []
    for idx in candidate_ids:
        dense_score = dense_norm.get(idx, 0.0)
        bm25_score = bm25_norm.get(idx, 0.0)
        combined = alpha * dense_score + (1.0 - alpha) * bm25_score
        merged.append((idx, combined, dense_scores.get(idx, 0.0), bm25_scores.get(idx, 0.0)))
    return sorted(merged, key=lambda item: item[1], reverse=True)


def rerank(
    query: str,
    candidates: list[tuple[int, float, float, float]],
    chunks: list[dict],
    rerank_model: str,
    top_k: int,
) -> list[tuple[int, float, float, float]]:
    from sentence_transformers import CrossEncoder

    model = CrossEncoder(rerank_model)
    pairs = [(query, chunks[idx]["text"]) for idx, *_ in candidates]
    scores = model.predict(pairs)
    reranked = []
    for candidate, score in zip(candidates, scores):
        idx, _, dense_score, bm25_score = candidate
        reranked.append((idx, float(score), dense_score, bm25_score))
    return sorted(reranked, key=lambda item: item[1], reverse=True)[:top_k]


def short_snippet(text: str, max_chars: int = 900) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= max_chars:
        return text
    return text[: max_chars - 3].rstrip() + "..."


def format_result(rank: int, chunk: dict, score: float, dense_score: float, bm25_score: float) -> str:
    metadata = chunk["metadata"]
    source = metadata.get("source_file", "")
    section = metadata.get("section_path", "")
    chunk_type = metadata.get("chunk_type", "")
    line_start = metadata.get("line_start", "")
    line_end = metadata.get("line_end", "")
    header = (
        f"[{rank}] score={score:.4f} dense={dense_score:.4f} bm25={bm25_score:.4f} "
        f"type={chunk_type} lines={line_start}-{line_end}\n"
        f"source={source}\n"
        f"section={section}"
    )
    return f"{header}\n{short_snippet(chunk['text'])}\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Hybrid dense + BM25 search over the GLOF RAG index.")
    parser.add_argument("--index-dir", type=Path, default=Path("rag/index"))
    parser.add_argument("--query", required=True)
    parser.add_argument("--top-k", type=int, default=8)
    parser.add_argument("--dense-top-k", type=int, default=30)
    parser.add_argument("--bm25-top-k", type=int, default=30)
    parser.add_argument("--alpha", type=float, default=0.65, help="Weight for dense score. BM25 gets 1-alpha.")
    parser.add_argument("--rerank-model", default="", help="Optional reranker, e.g. BAAI/bge-reranker-v2-m3")
    parser.add_argument("--json", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    require_dependencies(bool(args.rerank_model))
    manifest = load_json(args.index_dir / "manifest.json")
    chunks = load_chunks(args.index_dir / manifest["chunks"])

    candidates = hybrid_search(
        args.index_dir,
        args.query,
        manifest["model_name"],
        args.dense_top_k,
        args.bm25_top_k,
        args.alpha,
    )
    candidates = candidates[: max(args.top_k, 20) if args.rerank_model else args.top_k]
    if args.rerank_model and candidates:
        candidates = rerank(args.query, candidates, chunks, args.rerank_model, args.top_k)

    results = []
    for rank, (idx, score, dense_score, bm25_score) in enumerate(candidates[: args.top_k], start=1):
        chunk = chunks[idx]
        results.append(
            {
                "rank": rank,
                "score": score,
                "dense_score": dense_score,
                "bm25_score": bm25_score,
                "id": chunk["id"],
                "text": chunk["text"],
                "metadata": chunk["metadata"],
            }
        )

    if args.json:
        print(json.dumps({"query": args.query, "results": results}, indent=2, ensure_ascii=False))
        return

    for result in results:
        print(
            format_result(
                result["rank"],
                {"text": result["text"], "metadata": result["metadata"]},
                result["score"],
                result["dense_score"],
                result["bm25_score"],
            )
        )


if __name__ == "__main__":
    main()
