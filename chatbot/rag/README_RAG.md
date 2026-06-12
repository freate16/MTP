# GLOF Markdown RAG Pipeline

This pipeline is designed for the Markdown files in `rag/data`.

It does four things:

1. Splits Markdown by headings.
2. Keeps tables and figures as special chunks.
3. Embeds chunks with `BAAI/bge-m3`.
4. Retrieves with hybrid dense FAISS + BM25 keyword search.

## 1. Install Dependencies

From the project root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r rag\requirements-rag.txt
```

If `python` opens the Microsoft Store or is not available, use `uv`:

```powershell
$env:UV_CACHE_DIR = ".uv-cache"
uv venv .venv --python 3.12
.\.venv\Scripts\Activate.ps1
uv pip install -r rag\requirements-rag.txt
```

The first index build will download `BAAI/bge-m3`, so it needs internet access.

## 2. Chunk the Markdown Files

```powershell
python rag\chunk_markdown.py `
  --data-dir rag\data `
  --out rag\artifacts\chunks.jsonl `
  --max-text-tokens 850 `
  --text-overlap-tokens 120 `
  --table-rows-per-chunk 35
```

Recommended defaults for this corpus:

```text
Text chunks: 850 tokens
Text overlap: 120 tokens
Table chunks: 35 rows, table header repeated
Figure chunks: one figure/caption block per chunk
```

Each JSONL row has:

```json
{
  "id": "chunk id",
  "text": "Document/Section metadata plus chunk text",
  "metadata": {
    "source_file": "data/...",
    "document_title": "...",
    "section_path": "...",
    "chunk_type": "text/table/figure",
    "line_start": 1,
    "line_end": 20
  }
}
```

## 3. Build BGE-M3 Embedding Index

```powershell
python rag\build_bge_m3_index.py `
  --chunks rag\artifacts\chunks.jsonl `
  --index-dir rag\index `
  --model-name BAAI/bge-m3 `
  --batch-size 8
```

Outputs:

```text
rag/index/dense.faiss
rag/index/bm25.pkl
rag/index/chunks.jsonl
rag/index/manifest.json
rag/index/embeddings.npy
```

If your GPU has enough memory, increase `--batch-size`.

## 4. Search the Index

```powershell
python rag\search_hybrid.py `
  --index-dir rag\index `
  --query "Which glacial lakes in India showed more than 40 percent increase in August 2025?" `
  --top-k 8
```

For table-heavy or number-heavy queries, hybrid search is important because BM25 catches exact terms such as lake IDs, years, basin names, and `>50 Ha`.

Use optional reranking:

```powershell
python rag\search_hybrid.py `
  --index-dir rag\index `
  --query "What are the methods used for GLOF hazard assessment?" `
  --top-k 8 `
  --rerank-model BAAI/bge-reranker-v2-m3
```

## 5. Using Retrieved Chunks in a Chatbot

Take the top retrieved chunks and pass them to your LLM as context:

```text
You are a GLOF research assistant. Answer only from the context.
If the answer is not present, say you do not know.
Cite source file and line numbers.

Context:
[chunk 1]
[chunk 2]
...

Question:
...
```

Use `metadata.source_file`, `metadata.section_path`, `metadata.line_start`, and `metadata.line_end` for citations.

## 6. Build The Knowledge Graph Store

The TTL file is large, so do not parse it on every question. Build a persistent Oxigraph store once:

```powershell
python rag\build_kg_store.py `
  --ttl graphrag\glof_kg_populated_codex.ttl `
  --store-dir rag\kg_store
```

Use `--force` only if you want to delete and rebuild the store.

## 7. Hybrid GraphRAG With Qwen Through Hugging Face

Put your token in `.env`:

```text
HF_TOKEN=your_huggingface_token
```

Then ask a question:

```powershell
python rag\hybrid_graphrag.py `
  --question "What are the main GLOF triggering mechanisms and how are they related in the knowledge graph?" `
  --route auto `
  --model Qwen/Qwen3-4B-Instruct-2507
```

Routes:

```text
auto    chooses vector, KG, or both
vector  uses document chunks only
kg      uses the TTL knowledge graph only
both    combines document chunks and KG evidence
```

Examples:

```powershell
python rag\hybrid_graphrag.py `
  --question "Which glacial lakes showed more than 40 percent increase in August 2025?" `
  --route vector
```

```powershell
python rag\hybrid_graphrag.py `
  --question "Explain how GLOFTrigger, IceAvalancheTrigger, and RockAvalancheTrigger are connected." `
  --route kg `
  --show-context
```

```powershell
python rag\hybrid_graphrag.py `
  --question "Why do moraine-dammed lakes have high GLOF risk? Use both reports and the ontology." `
  --route both
```

Geospatial KG lookup:

```powershell
python rag\hybrid_graphrag.py `
  --question "Give information about 5 glacial lakes that are around 34.0926 degree lat and 75.4972 degree lon" `
  --route kg `
  --show-context
```

The graph uses `:latitude` and `:longitude` as WGS84 decimal degrees for representative points. Some `geo:asWKT`
polygons are also stored in longitude-latitude degree order, while a few older/source geometries may appear in projected
coordinates. For nearest-lake lookup, the code uses the decimal-degree `:latitude`/`:longitude` values and computes
haversine distance.
