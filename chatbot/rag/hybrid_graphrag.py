from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path
import sys
import datetime as dt

# Add project root to sys.path to import gnn module
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Optional import wrapper for dual inference (XGBoost + GNN)
try:
    from chatbot.dual_inference import explain_glof_prediction, explain_regional_glof, explain_top_glof_lakes
except ImportError as e:
    print(f"Warning: Dual inference module not loaded: {e}")
    explain_glof_prediction = None
    explain_regional_glof = None
    explain_top_glof_lakes = None

from kg_store import KgStore
from search_hybrid import hybrid_search, load_chunks, load_json


DEFAULT_HF_MODEL = "Qwen/Qwen3-4B-Instruct-2507"

VECTOR_HINTS = {
    "according",
    "article",
    "august",
    "cite",
    "data",
    "dataset",
    "document",
    "figure",
    "how many",
    "paper",
    "report",
    "study",
    "table",
    "year",
}
KG_HINTS = {
    "class",
    "classes",
    "connected",
    "connection",
    "cause",
    "causes",
    "causal",
    "catchment",
    "subcatchment",
    "sub-catchment",
    "downstream",
    "hierarchy",
    "infer",
    "inference",
    "ontology",
    "path",
    "property",
    "reason",
    "relation",
    "relationship",
    "threshold",
    "upstream",
    "sparql",
    "subclass",
    "top",
    "highest",
    "rank",
    "ranking",
    "trigger",
    "why",
    "weather variable",
    "weather variables",
}
GEOSPATIAL_HINTS = {
    "around",
    "coordinate",
    "coordinates",
    "degree",
    "degrees",
    "geo",
    "geometry",
    "lat",
    "latitude",
    "lon",
    "long",
    "longitude",
    "near",
    "nearby",
    "nearest",
    "projection",
    "shapefile",
    "utm",
    "wgs84",
}
FORECAST_HINTS = {
    "forecast",
    "predict",
    "prediction",
    "future",
    "tomorrow",
    "surface runoff",
    "subsurface runoff",
    "snowmelt",
    "run model",
    "probability",
    "susceptibility",
    "chance",
    "chances",
}


def is_tabular_count_query(question: str) -> bool:
    lowered = question.lower()
    has_count_signal = any(term in lowered for term in ["how many", "count", "number of", "total"])
    has_table_signal = any(term in lowered for term in ["table", "row", "rows", "range", "from", "between"])
    has_area_signal = any(term in lowered for term in ["area", "ha", "hectare", "hectares"])
    has_lake_category_signal = any(
        term in lowered
        for term in [
            "glacial lake",
            "moraine dammed",
            "lateral moraine",
            "end-moraine",
            "ice dammed",
            "supra-glacial",
            "erosion lake",
        ]
    )
    return has_count_signal and has_lake_category_signal and (has_table_signal or has_area_signal)


def require_hf() -> None:
    try:
        import dotenv  # noqa: F401
        import huggingface_hub  # noqa: F401
    except Exception as exc:
        raise SystemExit(
            "Missing Hugging Face client dependencies.\n"
            "Install with: pip install -r rag/requirements-rag.txt"
        ) from exc


def load_env_if_available() -> None:
    try:
        from dotenv import load_dotenv
    except Exception:
        return
    load_dotenv()


def choose_route(question: str) -> str:
    lowered = question.lower()
    
    if "hazard index" in lowered:
        return "kg"

    if any(term in lowered for term in ["threshold", "weather variable", "weather variables", "risk value", "risk interpretation"]):
        return "kg"

    if any(term in lowered for term in ["temperature", "precipitation", "dewpoint", "humidity", "wind speed", "snowmelt", "surface runoff", "sub-surface runoff"]) and "threshold" in lowered:
        return "kg"

    if any(term in lowered for term in ["top", "highest", "rank", "ranking", "most probable", "most susceptible"]) and any(
        term in lowered for term in ["lake", "lakes", "glacial lake", "glacial lakes", "glof", "probability", "susceptibility", "risk"]
    ):
        return "forecast"

    if any(hint in lowered for hint in FORECAST_HINTS):
        return "forecast"

    if is_tabular_count_query(question):
        return "both"
        
    if any(hint in lowered for hint in GEOSPATIAL_HINTS) and re.search(r"-?\d+(?:\.\d+)?", lowered):
        return "kg"
    vector_score = sum(1 for hint in VECTOR_HINTS if hint in lowered)
    kg_score = sum(1 for hint in KG_HINTS if hint in lowered)

    if kg_score and vector_score:
        return "both"
    if kg_score >= 2:
        return "kg"
    if kg_score == 1 and any(word in lowered for word in ["explain", "what", "how"]):
        return "both"
    if vector_score:
        return "vector"
    return "both"


def short_chunk_text(text: str, max_chars: int = 1600) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= max_chars:
        return text
    return text[: max_chars - 3].rstrip() + "..."


def retrieve_vector_context(
    question: str,
    *,
    index_dir: Path,
    top_k: int,
    dense_top_k: int,
    bm25_top_k: int,
    alpha: float,
) -> tuple[str, list[dict]]:
    manifest = load_json(index_dir / "manifest.json")
    chunks = load_chunks(index_dir / manifest["chunks"])
    candidates = hybrid_search(
        index_dir=index_dir,
        query=question,
        model_name=manifest["model_name"],
        dense_top_k=dense_top_k,
        bm25_top_k=bm25_top_k,
        alpha=alpha,
    )[:top_k]

    evidence: list[dict] = []
    blocks: list[str] = []
    for rank, (idx, score, dense_score, bm25_score) in enumerate(candidates, start=1):
        chunk = chunks[idx]
        metadata = chunk["metadata"]
        evidence.append(
            {
                "rank": rank,
                "id": chunk["id"],
                "score": score,
                "dense_score": dense_score,
                "bm25_score": bm25_score,
                "source_file": metadata.get("source_file"),
                "section_path": metadata.get("section_path"),
                "line_start": metadata.get("line_start"),
                "line_end": metadata.get("line_end"),
                "chunk_type": metadata.get("chunk_type"),
            }
        )
        citation = (
            f"[V{rank}] {metadata.get('source_file')} "
            f"lines {metadata.get('line_start')}-{metadata.get('line_end')} "
            f"section={metadata.get('section_path')}"
        )
        blocks.append(f"{citation}\n{short_chunk_text(chunk['text'])}")
    return "\n\n".join(blocks), evidence


def retrieve_kg_context(question: str, *, store_dir: Path) -> str:
    kg = KgStore(store_dir)
    return kg.context_for_question(question)


def extract_river_ids(question: str) -> list[str]:
    """Extract numeric river ids mentioned as 'river 170...' or '170... river'."""
    found: list[str] = []
    for left, right in re.findall(r"\briver\s+(\d{5,})\b|\b(\d{5,})\s+river\b", question, flags=re.IGNORECASE):
        river_id = left or right
        if river_id not in found:
            found.append(river_id)
    return found


def direct_kg_answer(question: str, *, store_dir: Path) -> str | None:
    """Answer deterministic graph traversal questions without LLM synthesis."""
    lowered = question.lower()
    glake_ids = extract_glake_ids(question)
    river_ids = extract_river_ids(question)

    wants_upstream = "upstream" in lowered
    wants_lake_river = any(
        term in lowered
        for term in [
            "closest river",
            "nearest river",
            "associated river",
            "which river",
            "what river",
        ]
    )

    if not wants_upstream and not (wants_lake_river and glake_ids):
        if not river_ids or not any(term in lowered for term in ["information", "info", "details", "properties", "about", "tell me"]):
            return None

    kg = KgStore(store_dir)
    blocks: list[str] = []
    if wants_upstream and glake_ids:
        blocks.extend(kg.upstream_rivers_for_lake_text(lake_id) for lake_id in glake_ids)
    elif wants_lake_river and glake_ids:
        blocks.extend(kg.associated_river_for_lake_text(lake_id) for lake_id in glake_ids)

    if wants_upstream and river_ids:
        blocks.extend(kg.upstream_rivers_text(river_id) for river_id in river_ids)
    elif river_ids and any(term in lowered for term in ["information", "info", "details", "properties", "about", "tell me"]):
        for river_id in river_ids:
            props = kg.river_properties_by_id(river_id)
            if props:
                blocks.append("KG river lookup:\n" + "\n".join(props))
            else:
                blocks.append(f"KG river lookup: river {river_id} was not found in the KG.")

    if not blocks:
        return None
    return "\n\n".join(blocks) + "\n\n[KG]"


def build_prompt(question: str, route: str, vector_context: str, kg_context: str, forecast_context: str = "") -> list[dict[str, str]]:
    context_parts = []
    if forecast_context:
        context_parts.append("MODEL FORECAST EVIDENCE\n" + forecast_context)
    if vector_context:
        context_parts.append("DOCUMENT/VECTOR EVIDENCE\n" + vector_context)
    if kg_context:
        context_parts.append("KNOWLEDGE GRAPH EVIDENCE\n" + kg_context)
    context = "\n\n---\n\n".join(context_parts) if context_parts else "No evidence retrieved."

    system = (
        "You are a GLOF research assistant. Answer using only the supplied evidence. "
        "If forecasting evidence is provided, state the exact predicted values from the model. "
        "Use document evidence for report/paper facts and table values. Use knowledge graph evidence "
        "for ontology relations, class hierarchy, triggers, causal links, geospatial lookup, and structured reasoning. "
        "When weather threshold evidence is provided, answer with the variable name, operator, threshold values, unit, and a short risk interpretation. "
        "For geospatial questions, report coordinates, distance, and available lake attributes from the KG. "
        "IMPORTANT: If the user specifically asks for 'hazard index', you must ONLY list the requested lakes and their Hazard Index. Do not mention area, elevation, or distance unless asked. "
        "If the evidence is insufficient, say what is missing. Cite vector evidence as [V1], [V2], etc. "
        "For graph evidence, cite as [KG]. Keep the answer concise and grounded."
    )
    user = f"""Route selected: {route}

Question:
{question}

Evidence:
{context}
"""
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]


def extract_glake_ids(question: str) -> list[str]:
    """Extract one or more GLAKE_IDs from a question while preserving order."""
    patterns = [
        # Common lake-id forms in this KG include both coordinate orderings.
        r"\bGL\d{6}[EN]\d{6}[EN]\b",
        r"\bGL\d+[EN]\d+[EN]\b",
        r"\bGL[_ ]?\d+\b",
    ]
    found: list[str] = []
    for pattern in patterns:
        for match in re.findall(pattern, question, flags=re.IGNORECASE):
            glake_id = match.upper().replace(" ", "_")
            if re.fullmatch(r"GL\d+[EN]\d+[EN]", glake_id):
                # Keep the canonical no-underscore lake-id form for coordinate IDs.
                pass
            elif not glake_id.startswith("GL_") and "E" not in glake_id and "N" not in glake_id:
                glake_id = glake_id.replace("GL", "GL_")
            if glake_id not in found:
                found.append(glake_id)
    return found


def hf_chat(messages: list[dict[str, str]], *, model: str, max_tokens: int, temperature: float) -> str:
    require_hf()
    from huggingface_hub import InferenceClient

    load_env_if_available()
    token = os.getenv("HF_TOKEN") or os.getenv("HUGGINGFACEHUB_API_TOKEN") or os.getenv("HUGGINGFACE_API_KEY")
    if not token:
        raise SystemExit("Missing HF token. Put HF_TOKEN=... in .env or your environment.")

    client = InferenceClient(model=model, token=token)
    response = client.chat_completion(
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature,
    )
    try:
        return response.choices[0].message.content
    except AttributeError:
        return response["choices"][0]["message"]["content"]


def forecast_context_for_question(question: str) -> tuple[str, str | None]:
    """Return forecast evidence and an optional direct answer/clarification."""
    lowered = question.lower()

    if any(term in lowered for term in ["top", "highest", "rank", "ranking", "most probable", "most susceptible"]) and \
       any(term in lowered for term in ["lake", "lakes", "glacial lake", "glacial lakes", "glof", "probability", "susceptibility", "risk"]):
        if explain_top_glof_lakes:
            print("DEBUG: Invoking all-lake forecast ranking pipeline...")
            return explain_top_glof_lakes(limit=5), None
        return "Error: Top-lake forecast ranking module could not be loaded.", None

    # 1. Try to extract one or more specific GLAKE_IDs
    glake_ids = extract_glake_ids(question)

    if glake_ids:
        if explain_glof_prediction:
            outputs = []
            for glake_id in glake_ids:
                print(f"DEBUG: Invoking Dual Pipeline (GNN + XGBoost) for {glake_id}...")
                outputs.append(f"### {glake_id}\n{explain_glof_prediction(glake_id)}")
            return "\n\n".join(outputs), None
        return "Error: Dual inference module could not be loaded.", None

    # 2. Check for lat/lon coordinate regional query
    lat_lon_match = re.search(r"(-?\d+\.\d+).*?(-?\d+\.\d+)", question)
    if lat_lon_match:
        # 3. Ask for buffer if not provided
        buffer_match = re.search(r"(\d+)\s*(km|kilometers|m|miles)", question, re.IGNORECASE)
        if not buffer_match:
            direct = "Please specify how much buffer is wanted for the region (e.g., 'within 20km')."
            return direct, direct

        buffer_val = float(buffer_match.group(1))
        lat, lon = float(lat_lon_match.groups()[0]), float(lat_lon_match.groups()[1])
        print(f"DEBUG: Invoking Regional Dual Pipeline near {lat}, {lon} (Buffer: {buffer_val}km)...")
        if explain_regional_glof:
            return explain_regional_glof(lat, lon, buffer_val), None
        return "Error: Regional inference module could not be loaded.", None

    direct = "Error: Forecast requested but no valid GLAKE_ID (e.g., GL11) or coordinates found in the question."
    return direct, direct


def answer_question(
    question: str,
    *,
    route: str = "auto",
    index_dir: Path | None = None,
    kg_store_dir: Path | None = None,
    model: str = DEFAULT_HF_MODEL,
    vector_top_k: int = 5,
    dense_top_k: int = 30,
    bm25_top_k: int = 30,
    alpha: float = 0.65,
    max_tokens: int = 1024,
    temperature: float = 0.2,
    show_context: bool = False,
) -> dict:
    """Shared programmatic API for the CLI and local website chat server."""
    script_dir = Path(__file__).resolve().parent
    index_dir = index_dir or script_dir / "index"
    kg_store_dir = kg_store_dir or script_dir / "kg_store"

    load_env_if_available()
    selected_route = choose_route(question) if route == "auto" else route

    vector_context = ""
    vector_evidence: list[dict] = []
    kg_context = ""
    forecast_context = ""
    direct_answer: str | None = None

    if selected_route in {"auto", "kg", "both"} or route == "auto":
        try:
            graph_answer = direct_kg_answer(question, store_dir=kg_store_dir)
        except SystemExit:
            graph_answer = None
        if graph_answer:
            return {
                "question": question,
                "route": "kg",
                "answer": graph_answer,
                "vector_evidence": [],
                "has_kg_context": True,
                "has_forecast_context": False,
            }

    if selected_route == "forecast":
        forecast_context, direct_answer = forecast_context_for_question(question)

    if selected_route in {"vector", "both"}:
        vector_context, vector_evidence = retrieve_vector_context(
            question,
            index_dir=index_dir,
            top_k=vector_top_k,
            dense_top_k=dense_top_k,
            bm25_top_k=bm25_top_k,
            alpha=alpha,
        )
    if selected_route in {"kg", "both"}:
        kg_context = retrieve_kg_context(question, store_dir=kg_store_dir)

    if selected_route == "forecast" and forecast_context:
        answer = forecast_context
    elif direct_answer:
        answer = direct_answer
    else:
        messages = build_prompt(question, selected_route, vector_context, kg_context, forecast_context)
        try:
            answer = hf_chat(messages, model=model, max_tokens=max_tokens, temperature=temperature)
        except SystemExit as exc:
            fallback_parts = []
            if forecast_context:
                fallback_parts.append(forecast_context)
            if kg_context:
                fallback_parts.append("Knowledge graph evidence was retrieved, but the HF chat model is unavailable.\n" + short_chunk_text(kg_context, 2200))
            if vector_context:
                fallback_parts.append("Vector evidence was retrieved, but the HF chat model is unavailable.\n" + short_chunk_text(vector_context, 2200))
            if not fallback_parts:
                raise
            answer = "\n\n".join(fallback_parts) + f"\n\nModel synthesis unavailable: {exc}"

    payload = {
        "question": question,
        "route": selected_route,
        "answer": answer,
        "vector_evidence": vector_evidence,
        "has_kg_context": bool(kg_context),
        "has_forecast_context": bool(forecast_context),
    }
    if show_context:
        payload["vector_context"] = vector_context
        payload["kg_context"] = kg_context
        payload["forecast_context"] = forecast_context
    return payload


def parse_args() -> argparse.Namespace:
    script_dir = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description="Hybrid vector + KG GraphRAG chatbot using Hugging Face Qwen.")
    parser.add_argument("--question", required=True)
    parser.add_argument("--route", choices=["auto", "vector", "kg", "both", "forecast"], default="auto")
    parser.add_argument("--index-dir", type=Path, default=script_dir / "index")
    parser.add_argument("--kg-store-dir", type=Path, default=script_dir / "kg_store")
    parser.add_argument("--model", default=DEFAULT_HF_MODEL)
    parser.add_argument("--vector-top-k", type=int, default=5)
    parser.add_argument("--dense-top-k", type=int, default=30)
    parser.add_argument("--bm25-top-k", type=int, default=30)
    parser.add_argument("--alpha", type=float, default=0.65)
    parser.add_argument("--max-tokens", type=int, default=700)
    parser.add_argument("--temperature", type=float, default=0.2)
    parser.add_argument("--show-context", action="store_true")
    parser.add_argument("--json", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = answer_question(
        args.question,
        route=args.route,
        index_dir=args.index_dir,
        kg_store_dir=args.kg_store_dir,
        model=args.model,
        vector_top_k=args.vector_top_k,
        dense_top_k=args.dense_top_k,
        bm25_top_k=args.bm25_top_k,
        alpha=args.alpha,
        max_tokens=args.max_tokens,
        temperature=args.temperature,
        show_context=args.show_context,
    )

    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(f"Route: {payload['route']}\n")
        print(payload["answer"])
        if payload["vector_evidence"]:
            print("\nVector evidence:")
            for item in payload["vector_evidence"]:
                print(
                    f"[V{item['rank']}] {item['source_file']} "
                    f"lines {item['line_start']}-{item['line_end']} ({item['chunk_type']})"
                )


if __name__ == "__main__":
    main()
