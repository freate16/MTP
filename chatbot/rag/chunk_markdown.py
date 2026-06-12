from __future__ import annotations

import argparse
import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
TABLE_LINE_RE = re.compile(r"^\s*\|.*\|\s*$")
TABLE_CAPTION_RE = re.compile(
    r"^\s*(?:\*\*)?\s*(?:Table|TABLE)\s+[A-Za-z0-9. -]+(?::|\.|\s*$).*?(?:\*\*)?\s*$"
)
FIGURE_RE = re.compile(
    r"^\s*(?:Image\s+/.+?\s+description:|(?:\*\*)?\s*Figure\s+\d+[A-Za-z0-9.:-]*\b)",
    re.IGNORECASE,
)
WORD_RE = re.compile(r"\w+|[^\w\s]", re.UNICODE)
LAKE_ID_RE = re.compile(r"\b\d{2}[_A-Z0-9]{3,12}[_A-Z0-9]*\b")
GENERIC_TITLE_RE = re.compile(
    r"^(abstract|arstract|introduction|summary|executive summary|foreword|acknowledgements?|keywords?)$",
    re.IGNORECASE,
)
SKIP_SECTION_RE = re.compile(
    r"^(contents|references|bibliography|further reading|acknowledgements?|acknowledgments?|"
    r"declaration of competing interest|declaration of competing interests|competing interests?|"
    r"conflict of interest|data availability)$",
    re.IGNORECASE,
)


NOISE_PATTERNS = [
    re.compile(r"^\s*\*{3,}\s*$"),
    re.compile(r"^\s*-{3,}\s*$"),
    re.compile(r"^\s*nrsc\s*$", re.IGNORECASE),
    re.compile(r"^\s*\d+\s*$"),
    re.compile(r"^\s*[ivxlcdm]{1,8}\s*$", re.IGNORECASE),
    re.compile(r"^\s*National Remote Sensing Centre,\s*ISRO,\s*Hyderabad\s*\d*\s*$", re.IGNORECASE),
    re.compile(r"^\s*\d+\s+National Remote Sensing Centre,\s*ISRO,\s*Hyderabad\s*$", re.IGNORECASE),

]


@dataclass
class ChunkConfig:
    max_text_tokens: int = 850
    text_overlap_tokens: int = 120
    min_text_tokens: int = 40
    table_rows_per_chunk: int = 35
    model_name: str | None = "BAAI/bge-m3"


class TokenCounter:
    def __init__(self, model_name: str | None = None) -> None:
        self.tokenizer = None
        if model_name:
            try:
                from transformers import AutoTokenizer

                self.tokenizer = AutoTokenizer.from_pretrained(model_name, local_files_only=True)
            except Exception:
                self.tokenizer = None

    def count(self, text: str) -> int:
        if not text:
            return 0
        if self.tokenizer is not None:
            return len(self.tokenizer.encode(text, add_special_tokens=False))
        return len(WORD_RE.findall(text))


def strip_markdown(text: str) -> str:
    text = text.strip()
    text = re.sub(r"^\*+|\*+$", "", text)
    text = re.sub(r"\*{1,3}", " ", text)
    text = re.sub(r"`+", "", text)
    text = re.sub(r"<br\s*/?>", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>", "", text)
    return re.sub(r"\s+", " ", text).strip()


def clean_line(line: str) -> str:
    line = line.replace("\ufeff", "")
    line = re.sub(r"<br\s*/?>", " ", line, flags=re.IGNORECASE)
    line = re.sub(r"\s+$", "", line)
    return line


def is_noise_line(line: str) -> bool:
    stripped = strip_markdown(line)
    if not stripped:
        return False
    return any(pattern.match(stripped) for pattern in NOISE_PATTERNS)


def is_table_line(line: str) -> bool:
    return bool(TABLE_LINE_RE.match(line))


def is_table_separator(line: str) -> bool:
    cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell or "") for cell in cells)


def is_heading(line: str) -> tuple[int, str] | None:
    match = HEADING_RE.match(line)
    if not match:
        return None
    return len(match.group(1)), strip_markdown(match.group(2))


def looks_like_table_caption(line: str) -> bool:
    return bool(TABLE_CAPTION_RE.match(line.strip())) or bool(
        re.match(r"^Table\s+[A-Za-z0-9. -]+(?::|\.|\s|$)", strip_markdown(line), re.IGNORECASE)
    )


def looks_like_figure(line: str) -> bool:
    return bool(FIGURE_RE.match(line))


def title_from_filename(path: Path) -> str:
    stem = path.stem
    stem = stem.replace("_extraction", "").replace("_gemini", "")
    stem = stem.replace("('", "").replace("', '.pdf')", "")
    stem = stem.replace("_", " ")
    return strip_markdown(stem)


def normalize_document_title(path: Path, first_heading: str | None) -> str:
    if first_heading and not GENERIC_TITLE_RE.match(first_heading):
        return first_heading
    return title_from_filename(path)


def make_chunk_id(source_file: str, chunk_type: str, line_start: int, line_end: int, index: int) -> str:
    raw = f"{source_file}:{chunk_type}:{line_start}:{line_end}:{index}"
    return hashlib.sha1(raw.encode("utf-8")).hexdigest()[:16]


def heading_path(headings: list[str | None]) -> str:
    return " > ".join(heading for heading in headings if heading)


def should_skip_section(headings: list[str | None]) -> bool:
    return any(bool(heading and SKIP_SECTION_RE.match(heading.strip())) for heading in headings)


def prefix_content(
    body: str,
    document_title: str,
    section_path: str,
    chunk_type: str,
    label: str | None = None,
) -> str:
    lines = [f"Document: {document_title}"]
    if section_path:
        lines.append(f"Section: {section_path}")
    lines.append(f"Type: {chunk_type}")
    if label:
        lines.append(label)
    lines.append("")
    lines.append(body.strip())
    return "\n".join(lines).strip()


def split_oversized_paragraph(paragraph: str, counter: TokenCounter, max_tokens: int) -> list[str]:
    sentences = re.split(r"(?<=[.!?])\s+", paragraph)
    pieces: list[str] = []
    current: list[str] = []
    for sentence in sentences:
        if counter.count(sentence) > max_tokens:
            words = WORD_RE.findall(sentence)
            for start in range(0, len(words), max_tokens):
                pieces.append(" ".join(words[start : start + max_tokens]))
            continue
        candidate = " ".join(current + [sentence]).strip()
        if current and counter.count(candidate) > max_tokens:
            pieces.append(" ".join(current).strip())
            current = [sentence]
        else:
            current.append(sentence)
    if current:
        pieces.append(" ".join(current).strip())
    return [piece for piece in pieces if piece]


def overlap_tail(text: str, overlap_tokens: int) -> str:
    if overlap_tokens <= 0:
        return ""
    words = WORD_RE.findall(text)
    return " ".join(words[-overlap_tokens:])


def split_text(text: str, counter: TokenCounter, max_tokens: int, overlap_tokens: int) -> list[str]:
    text = re.sub(r"\n{3,}", "\n\n", text.strip())
    if not text:
        return []
    if counter.count(text) <= max_tokens:
        return [text]

    paragraphs = [paragraph.strip() for paragraph in re.split(r"\n\s*\n", text) if paragraph.strip()]
    expanded: list[str] = []
    for paragraph in paragraphs:
        if counter.count(paragraph) > max_tokens:
            expanded.extend(split_oversized_paragraph(paragraph, counter, max_tokens))
        else:
            expanded.append(paragraph)

    chunks: list[str] = []
    current = ""
    for paragraph in expanded:
        candidate = f"{current}\n\n{paragraph}".strip() if current else paragraph
        if current and counter.count(candidate) > max_tokens:
            chunks.append(current.strip())
            tail = overlap_tail(current, overlap_tokens)
            current = f"{tail}\n\n{paragraph}".strip() if tail else paragraph
        else:
            current = candidate
    if current:
        chunks.append(current.strip())
    return chunks


def parse_table_header(table_lines: list[str]) -> tuple[list[str], str | None]:
    if not table_lines:
        return [], None
    header = [strip_markdown(cell) for cell in table_lines[0].strip().strip("|").split("|")]
    separator = table_lines[1] if len(table_lines) > 1 and is_table_separator(table_lines[1]) else None
    return header, separator


def extract_caption_from_buffer(buffer: list[tuple[int, str]]) -> str | None:
    for _, line in reversed(buffer[-4:]):
        if line.strip() and looks_like_table_caption(line):
            return strip_markdown(line)
    return None


def trim_caption_from_buffer(buffer: list[tuple[int, str]], caption: str | None) -> None:
    if not caption:
        return
    for idx in range(len(buffer) - 1, max(-1, len(buffer) - 5), -1):
        if strip_markdown(buffer[idx][1]) == caption:
            del buffer[idx]
            return


def infer_caption_from_previous(lines: list[str], table_start: int) -> str | None:
    for idx in range(table_start - 1, max(-1, table_start - 5), -1):
        line = lines[idx].strip()
        if not line:
            continue
        if looks_like_table_caption(line):
            return strip_markdown(line)
        break
    return None


def extract_entities(text: str) -> dict[str, list[str]]:
    BASINS = ["Indus", "Ganga", "Brahmaputra"]
    SUBBASINS = [
        "Teesta", "Satluj", "Chenab", "Jhelum", "Ravi", "Beas", "Shyok", "Gandak",
        "Ghaghara", "Kosi", "Sarda", "Upper Ganga", "Yamuna", "Gilgit", "Indus upper",
        "Indus middle", "Amo Chu", "Dibang", "Dihang", "Jia Bharali", "Lhasa Tsangpo",
        "Lohit", "Lower Yarlung Tsangpo", "Manas", "Puna Tsang Chu", "Subansiri",
        "Upper Yarlung Tsangpo"
    ]
    COUNTRIES = ["India", "China", "Nepal", "Bhutan", "Myanmar"]

    def find_terms(terms: list[str]) -> list[str]:
        if not terms:
            return []
        pattern = r"\b(?:" + "|".join(re.escape(t) for t in terms) + r")\b"
        return sorted({m.group(0) for m in re.finditer(pattern, text, flags=re.IGNORECASE)})

    basins = find_terms(BASINS)
    subbasins = find_terms(SUBBASINS)
    countries = find_terms(COUNTRIES)
    lake_ids = sorted(set(LAKE_ID_RE.findall(text)))

    return {
        "basins": basins[:20],
        "subbasins": subbasins[:20],
        "countries": countries[:20],
        "lake_ids": lake_ids[:50],
    }


def collect_table(lines: list[str], start_idx: int) -> tuple[list[str], int]:
    table_lines: list[str] = []
    idx = start_idx
    while idx < len(lines) and is_table_line(lines[idx]):
        table_lines.append(clean_line(lines[idx]))
        idx += 1
    return table_lines, idx


def collect_figure(lines: list[str], start_idx: int) -> tuple[list[str], int]:
    figure_lines = [clean_line(lines[start_idx])]
    idx = start_idx + 1
    while idx < len(lines):
        line = clean_line(lines[idx])
        if not line.strip():
            break
        if is_heading(line) or is_table_line(line):
            break
        # Keep short caption continuations with the figure, but avoid swallowing a whole paragraph.
        if looks_like_figure(line) or len(figure_lines) < 3:
            figure_lines.append(line)
            idx += 1
            continue
        break
    return figure_lines, idx


def emit_text_chunks(
    chunks: list[dict],
    buffer: list[tuple[int, str]],
    *,
    source_file: str,
    document_title: str,
    section_path: str,
    headings: list[str | None],
    counter: TokenCounter,
    config: ChunkConfig,
) -> None:
    if not buffer:
        return

    line_start = buffer[0][0]
    line_end = buffer[-1][0]
    body = "\n".join(line for _, line in buffer).strip()
    body = re.sub(r"\n{3,}", "\n\n", body)
    if not body:
        return

    text_chunks = split_text(body, counter, config.max_text_tokens, config.text_overlap_tokens)
    for piece_index, piece in enumerate(text_chunks):
        if counter.count(piece) < config.min_text_tokens and len(text_chunks) > 1:
            continue
        content = prefix_content(piece, document_title, section_path, "text")
        metadata = {
            "source_file": source_file,
            "document_title": document_title,
            "section_path": section_path,
            "section_headings": [heading for heading in headings if heading],
            "chunk_type": "text",
            "line_start": line_start,
            "line_end": line_end,
            "token_count_estimate": counter.count(content),
            **extract_entities(content),
        }
        chunks.append(
            {
                "id": make_chunk_id(source_file, "text", line_start, line_end, piece_index),
                "text": content,
                "metadata": metadata,
            }
        )


def emit_table_chunks(
    chunks: list[dict],
    table_lines: list[str],
    *,
    caption: str | None,
    source_file: str,
    document_title: str,
    section_path: str,
    headings: list[str | None],
    line_start: int,
    counter: TokenCounter,
    config: ChunkConfig,
) -> None:
    if not table_lines:
        return

    columns, separator = parse_table_header(table_lines)
    header = table_lines[0]
    body_start = 2 if separator else 1
    body_rows = table_lines[body_start:]
    rows_per_chunk = max(1, config.table_rows_per_chunk)
    row_groups = [body_rows[i : i + rows_per_chunk] for i in range(0, len(body_rows), rows_per_chunk)] or [[]]

    for group_index, rows in enumerate(row_groups):
        table_body = [header]
        if separator:
            table_body.append(separator)
        table_body.extend(rows)
        label = f"Table: {caption}" if caption else "Table"
        body = "\n".join(table_body)
        content = prefix_content(body, document_title, section_path, "table", label)
        row_start = group_index * rows_per_chunk + 1
        row_end = row_start + len(rows) - 1 if rows else row_start
        metadata = {
            "source_file": source_file,
            "document_title": document_title,
            "section_path": section_path,
            "section_headings": [heading for heading in headings if heading],
            "chunk_type": "table",
            "table_caption": caption,
            "columns": columns,
            "table_row_start": row_start,
            "table_row_end": row_end,
            "line_start": line_start,
            "line_end": line_start + len(table_lines) - 1,
            "token_count_estimate": counter.count(content),
            **extract_entities(content),
        }
        chunks.append(
            {
                "id": make_chunk_id(source_file, "table", line_start, line_start + len(table_lines) - 1, group_index),
                "text": content,
                "metadata": metadata,
            }
        )


def emit_figure_chunk(
    chunks: list[dict],
    figure_lines: list[str],
    *,
    source_file: str,
    document_title: str,
    section_path: str,
    headings: list[str | None],
    line_start: int,
    counter: TokenCounter,
) -> None:
    body = "\n".join(figure_lines).strip()
    caption = next((strip_markdown(line) for line in figure_lines if re.match(r"^\s*(?:\*\*)?\s*Figure\s+\d+", line, re.IGNORECASE)), None)
    label = f"Figure: {caption}" if caption else "Figure"
    content = prefix_content(body, document_title, section_path, "figure", label)
    metadata = {
        "source_file": source_file,
        "document_title": document_title,
        "section_path": section_path,
        "section_headings": [heading for heading in headings if heading],
        "chunk_type": "figure",
        "figure_caption": caption,
        "line_start": line_start,
        "line_end": line_start + len(figure_lines) - 1,
        "token_count_estimate": counter.count(content),
        **extract_entities(content),
    }
    chunks.append(
        {
            "id": make_chunk_id(source_file, "figure", line_start, line_start + len(figure_lines) - 1, 0),
            "text": content,
            "metadata": metadata,
        }
    )


def chunk_markdown_file(path: Path, data_dir: Path, counter: TokenCounter, config: ChunkConfig) -> list[dict]:
    raw_text = path.read_text(encoding="utf-8", errors="replace")
    lines = [clean_line(line) for line in raw_text.splitlines()]
    chunks: list[dict] = []
    headings: list[str | None] = [None] * 6
    first_heading: str | None = None
    document_title = normalize_document_title(path, first_heading)
    source_file = str(path.relative_to(data_dir.parent)).replace("\\", "/")
    text_buffer: list[tuple[int, str]] = []

    def flush_text() -> None:
        emit_text_chunks(
            chunks,
            text_buffer,
            source_file=source_file,
            document_title=document_title,
            section_path=heading_path(headings),
            headings=headings,
            counter=counter,
            config=config,
        )
        text_buffer.clear()

    idx = 0
    while idx < len(lines):
        line = lines[idx]
        line_no = idx + 1

        heading = is_heading(line)
        if heading:
            flush_text()
            level, title = heading
            if first_heading is None:
                first_heading = title
                document_title = normalize_document_title(path, first_heading)
            headings[level - 1] = title
            for reset_idx in range(level, len(headings)):
                headings[reset_idx] = None
            idx += 1
            continue

        if is_noise_line(line):
            idx += 1
            continue

        if should_skip_section(headings):
            idx += 1
            continue

        if is_table_line(line):
            caption = extract_caption_from_buffer(text_buffer) or infer_caption_from_previous(lines, idx)
            trim_caption_from_buffer(text_buffer, caption)
            flush_text()
            table_lines, next_idx = collect_table(lines, idx)
            emit_table_chunks(
                chunks,
                table_lines,
                caption=caption,
                source_file=source_file,
                document_title=document_title,
                section_path=heading_path(headings),
                headings=headings,
                line_start=line_no,
                counter=counter,
                config=config,
            )
            idx = next_idx
            continue

        if looks_like_figure(line):
            flush_text()
            figure_lines, next_idx = collect_figure(lines, idx)
            emit_figure_chunk(
                chunks,
                figure_lines,
                source_file=source_file,
                document_title=document_title,
                section_path=heading_path(headings),
                headings=headings,
                line_start=line_no,
                counter=counter,
            )
            idx = next_idx
            continue

        text_buffer.append((line_no, line))
        idx += 1

    flush_text()
    return chunks


def write_jsonl(path: Path, rows: Iterable[dict]) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
            count += 1
    return count


def build_chunks(data_dir: Path, config: ChunkConfig) -> list[dict]:
    counter = TokenCounter(config.model_name)
    all_chunks: list[dict] = []
    for path in sorted(data_dir.glob("*.md")):
        all_chunks.extend(chunk_markdown_file(path, data_dir, counter, config))
    return all_chunks


def summarize(chunks: list[dict]) -> dict[str, int]:
    summary: dict[str, int] = {"total": len(chunks)}
    for chunk in chunks:
        chunk_type = chunk["metadata"]["chunk_type"]
        summary[chunk_type] = summary.get(chunk_type, 0) + 1
    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Chunk Markdown files for a GLOF RAG chatbot.")
    parser.add_argument("--data-dir", type=Path, default=Path("rag/data"), help="Directory containing Markdown files.")
    parser.add_argument("--out", type=Path, default=Path("rag/artifacts/chunks.jsonl"), help="Output JSONL path.")
    parser.add_argument("--model-name", default="BAAI/bge-m3", help="Tokenizer model used for token-aware splitting.")
    parser.add_argument("--max-text-tokens", type=int, default=850)
    parser.add_argument("--text-overlap-tokens", type=int, default=120)
    parser.add_argument("--min-text-tokens", type=int, default=40)
    parser.add_argument("--table-rows-per-chunk", type=int, default=35)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = ChunkConfig(
        max_text_tokens=args.max_text_tokens,
        text_overlap_tokens=args.text_overlap_tokens,
        min_text_tokens=args.min_text_tokens,
        table_rows_per_chunk=args.table_rows_per_chunk,
        model_name=args.model_name,
    )
    chunks = build_chunks(args.data_dir, config)
    count = write_jsonl(args.out, chunks)
    print(json.dumps({"output": str(args.out), "written": count, "summary": summarize(chunks)}, indent=2))


if __name__ == "__main__":
    main()
