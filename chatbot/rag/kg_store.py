from __future__ import annotations

import json
import math
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


CRYO = "https://w3id.org/cryosphere/ontology#"
PREFIXES = {
    "": CRYO,
    "dc": "http://purl.org/dc/elements/1.1/",
    "dcterms": "http://purl.org/dc/terms/",
    "geo": "http://www.opengis.net/ont/geosparql#",
    "owl": "http://www.w3.org/2002/07/owl#",
    "prov": "http://www.w3.org/ns/prov#",
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "skos": "http://www.w3.org/2004/02/skos/core#",
    "sosa": "http://www.w3.org/ns/sosa/",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
}
SPARQL_PREFIXES = "\n".join(
    f"PREFIX {name}: <{iri}>" if name else f"PREFIX : <{iri}>"
    for name, iri in PREFIXES.items()
)

TOKEN_RE = re.compile(r"[A-Za-z][A-Za-z0-9_-]{2,}")
COORD_PAIR_RE = re.compile(
    r"(?P<a>-?\d+(?:\.\d+)?)\s*(?:degree|degrees|deg|°)?\s*(?:lat|latitude)?"
    r"(?:\s*(?:,|and|near|around|at)\s*)+"
    r"(?P<b>-?\d+(?:\.\d+)?)\s*(?:degree|degrees|deg|°)?\s*(?:lon|lng|longitude)?",
    re.IGNORECASE,
)
STOPWORDS = {
    "about",
    "above",
    "after",
    "also",
    "and",
    "answer",
    "are",
    "between",
    "can",
    "does",
    "from",
    "give",
    "have",
    "how",
    "into",
    "needed",
    "show",
    "that",
    "the",
    "their",
    "these",
    "this",
    "what",
    "when",
    "where",
    "which",
    "with",
}


@dataclass
class KgHit:
    uri: str
    label: str
    kind: str = ""
    definition: str = ""
    description: str = ""

    def as_text(self) -> str:
        parts = [f"Entity: {self.label}", f"URI: {self.uri}"]
        if self.kind:
            parts.append(f"Type: {self.kind}")
        if self.definition:
            parts.append(f"Definition: {self.definition}")
        if self.description and self.description != self.definition:
            parts.append(f"Description: {self.description}")
        return "\n".join(parts)


@dataclass
class NearbyFeature:
    uri: str
    label: str
    latitude: float
    longitude: float
    distance_km: float
    lake_type: str = ""
    lake_area_m2: float | None = None
    surface_elevation_m: float | None = None
    susceptibility_label: str = ""
    susceptibility_prob: float | None = None

    def as_text(self, rank: int) -> str:
        parts = [
            f"{rank}. {self.label}",
            f"URI: {self.uri}",
            f"Coordinates: {self.latitude:.6f}, {self.longitude:.6f}",
            f"Distance from query point: {self.distance_km:.2f} km",
        ]
        if self.lake_type:
            parts.append(f"Lake type: {self.lake_type}")
        if self.lake_area_m2 is not None:
            parts.append(f"Lake area: {self.lake_area_m2:.1f} m2 ({self.lake_area_m2 / 10000:.2f} ha)")
        if self.surface_elevation_m is not None:
            parts.append(f"Surface elevation: {self.surface_elevation_m:.1f} m")
        if self.susceptibility_label:
            parts.append(f"Susceptibility: {self.susceptibility_label}")
        if self.susceptibility_prob is not None:
            parts.append(f"Susceptibility probability: {self.susceptibility_prob:.4f}")
        return "\n".join(parts)


def require_pyoxigraph() -> None:
    try:
        import pyoxigraph  # noqa: F401
    except Exception as exc:
        raise SystemExit(
            "Missing dependency: pyoxigraph\n"
            "Install with: pip install -r rag/requirements-rag.txt"
        ) from exc


def sparql_escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')


def term_to_text(term) -> str:
    if term is None:
        return ""
    value = getattr(term, "value", None)
    if value is not None:
        return str(value)
    return str(term)


def compact_uri(uri: str) -> str:
    if uri.startswith(CRYO):
        return ":" + uri[len(CRYO) :]
    for prefix, iri in PREFIXES.items():
        if prefix and uri.startswith(iri):
            return f"{prefix}:{uri[len(iri):]}"
    return uri


def clean_literal(value: str, max_len: int = 500) -> str:
    value = re.sub(r"\s+", " ", value).strip()
    if len(value) > max_len:
        return value[: max_len - 3].rstrip() + "..."
    return value


def extract_keywords(question: str, limit: int = 8) -> list[str]:
    tokens = []
    for token in TOKEN_RE.findall(question):
        lowered = token.lower()
        if lowered not in STOPWORDS and lowered not in tokens:
            tokens.append(lowered)
    return tokens[:limit]


def parse_float(value: str) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def normalize_graph_id(value: str) -> str:
    value = str(value).strip().strip('"')
    if re.fullmatch(r"\d+\.0+", value):
        return value.split(".", 1)[0]
    return value


def parse_lat_lon(question: str) -> tuple[float, float] | None:
    lowered = question.lower()
    lat_match = re.search(r"(-?\d+(?:\.\d+)?)\s*(?:degree|degrees|deg|°)?\s*(?:lat|latitude)\b", lowered)
    lon_match = re.search(r"(-?\d+(?:\.\d+)?)\s*(?:degree|degrees|deg|°)?\s*(?:lon|lng|longitude)\b", lowered)
    if lat_match and lon_match:
        return float(lat_match.group(1)), float(lon_match.group(1))

    match = COORD_PAIR_RE.search(question)
    if not match:
        return None
    first = float(match.group("a"))
    second = float(match.group("b"))
    if -90 <= first <= 90 and -180 <= second <= 180:
        return first, second
    if -90 <= second <= 90 and -180 <= first <= 180:
        return second, first
    return None


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    radius_km = 6371.0088
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return 2 * radius_km * math.asin(math.sqrt(a))


class KgStore:
    def __init__(self, store_dir: Path = Path("rag/kg_store")) -> None:
        require_pyoxigraph()
        from pyoxigraph import Store

        self.store_dir = store_dir
        if not store_dir.exists() or not any(store_dir.iterdir()):
            raise SystemExit(
                f"KG store not found at {store_dir}. Build it first with:\n"
                "python rag\\build_kg_store.py --ttl graphrag\\glof_kg_populated_codex.ttl --store-dir rag\\kg_store"
            )
        store_path = str(store_dir)
        self.store = Store.read_only(store_path)

    @staticmethod
    def build(ttl_path: Path, store_dir: Path = Path("rag/kg_store"), *, force: bool = False) -> dict:
        require_pyoxigraph()
        from pyoxigraph import RdfFormat, Store

        if store_dir.exists() and any(store_dir.iterdir()) and not force:
            return {
                "store_dir": str(store_dir),
                "ttl_path": str(ttl_path),
                "status": "exists",
                "message": "Use --force to rebuild.",
            }

        if force and store_dir.exists():
            # Caller owns this exact store path.
            import shutil

            shutil.rmtree(store_dir)

        store_dir.mkdir(parents=True, exist_ok=True)
        store = Store(str(store_dir))
        store.bulk_load(path=str(ttl_path), format=RdfFormat.TURTLE, lenient=True)
        store.optimize()
        store.flush()

        manifest = {
            "ttl_path": str(ttl_path),
            "store_dir": str(store_dir),
            "format": "turtle",
            "engine": "pyoxigraph",
        }
        (store_dir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
        return manifest

    def select(self, query: str, variables: Iterable[str], limit: int | None = None) -> list[dict[str, str]]:
        rows: list[dict[str, str]] = []
        for solution in self.store.query(query):
            row = {var: term_to_text(solution[var]) if solution[var] is not None else "" for var in variables}
            rows.append(row)
            if limit and len(rows) >= limit:
                break
        return rows

    def entity_search(self, question: str, limit: int = 8) -> list[KgHit]:
        keywords = extract_keywords(question)
        if not keywords:
            return []
        filters = " || ".join(
            f'CONTAINS(LCASE(STR(?label)), "{sparql_escape(keyword)}")'
            for keyword in keywords
        )
        query = f"""
{SPARQL_PREFIXES}
SELECT ?s ?label ?typeLabel ?definition ?description WHERE {{
  ?s (rdfs:label|skos:prefLabel) ?label .
  FILTER(LANG(?label) = "" || LANGMATCHES(LANG(?label), "en"))
  FILTER({filters})
  OPTIONAL {{ ?s a ?type . OPTIONAL {{ ?type rdfs:label ?typeLabel . }} }}
  OPTIONAL {{ ?s skos:definition ?definition . FILTER(LANG(?definition) = "" || LANGMATCHES(LANG(?definition), "en")) }}
  OPTIONAL {{ ?s dc:description ?description . FILTER(LANG(?description) = "" || LANGMATCHES(LANG(?description), "en")) }}
}}
LIMIT {limit * 3}
"""
        rows = self.select(query, ["s", "label", "typeLabel", "definition", "description"])
        seen: set[str] = set()
        hits: list[KgHit] = []
        for row in rows:
            uri = row["s"]
            if uri in seen:
                continue
            seen.add(uri)
            hits.append(
                KgHit(
                    uri=uri,
                    label=clean_literal(row["label"], 120),
                    kind=clean_literal(row.get("typeLabel", ""), 120),
                    definition=clean_literal(row.get("definition", "")),
                    description=clean_literal(row.get("description", "")),
                )
            )
            if len(hits) >= limit:
                break
        return hits

    def neighbourhood(self, uri: str, limit: int = 40) -> list[str]:
        uri = uri.strip("<>")
        query = f"""
{SPARQL_PREFIXES}
SELECT ?direction ?pLabel ?oLabel ?o ?sLabel ?s WHERE {{
  {{
    BIND("out" AS ?direction)
    <{sparql_escape(uri)}> ?p ?o .
    OPTIONAL {{ ?p rdfs:label ?pLabel . }}
    OPTIONAL {{ ?o rdfs:label ?oLabel . }}
  }}
  UNION
  {{
    BIND("in" AS ?direction)
    ?s ?p <{sparql_escape(uri)}> .
    OPTIONAL {{ ?p rdfs:label ?pLabel . }}
    OPTIONAL {{ ?s rdfs:label ?sLabel . }}
  }}
}}
LIMIT {limit}
"""
        rows = self.select(query, ["direction", "pLabel", "oLabel", "o", "sLabel", "s"])
        triples: list[str] = []
        subject = compact_uri(uri)
        for row in rows:
            predicate = row["pLabel"] or "related to"
            if row["direction"] == "out":
                obj = row["oLabel"] or compact_uri(row["o"])
                triples.append(f"{subject} --{predicate}--> {clean_literal(obj, 180)}")
            else:
                subj = row["sLabel"] or compact_uri(row["s"])
                triples.append(f"{clean_literal(subj, 180)} --{predicate}--> {subject}")
        return triples

    def subclass_context(self, entity_uri: str, limit: int = 30) -> list[str]:
        entity_uri = entity_uri.strip("<>")
        query = f"""
{SPARQL_PREFIXES}
SELECT ?childLabel ?parentLabel WHERE {{
  {{
    ?child rdfs:subClassOf <{sparql_escape(entity_uri)}> .
    OPTIONAL {{ ?child rdfs:label ?childLabel . }}
    BIND("" AS ?parentLabel)
  }}
  UNION
  {{
    <{sparql_escape(entity_uri)}> rdfs:subClassOf ?parent .
    OPTIONAL {{ ?parent rdfs:label ?parentLabel . }}
    BIND("" AS ?childLabel)
  }}
}}
LIMIT {limit}
"""
        rows = self.select(query, ["childLabel", "parentLabel"])
        lines: list[str] = []
        for row in rows:
            if row["childLabel"]:
                lines.append(f"Subclass: {clean_literal(row['childLabel'], 160)}")
            if row["parentLabel"]:
                lines.append(f"Parent class: {clean_literal(row['parentLabel'], 160)}")
        return lines

    def trigger_context(self, limit: int = 30) -> list[str]:
        query = f"""
{SPARQL_PREFIXES}
SELECT ?label ?definition ?description WHERE {{
  ?trigger rdfs:subClassOf* :GLOFTrigger .
  OPTIONAL {{ ?trigger rdfs:label ?label . }}
  OPTIONAL {{ ?trigger skos:definition ?definition . }}
  OPTIONAL {{ ?trigger dc:description ?description . }}
  FILTER(BOUND(?label))
}}
LIMIT {limit}
"""
        rows = self.select(query, ["label", "definition", "description"])
        return [
            f"{clean_literal(row['label'], 120)}: {clean_literal(row['definition'] or row['description'], 420)}"
            for row in rows
            if row["label"]
        ]

    def risk_context(self, limit: int = 30) -> list[str]:
        query = f"""
{SPARQL_PREFIXES}
SELECT ?label ?definition ?description WHERE {{
  ?s (rdfs:label|skos:prefLabel) ?label .
  FILTER(REGEX(LCASE(STR(?label)), "risk|hazard|exposure|vulnerab|susceptib|indicator"))
  OPTIONAL {{ ?s skos:definition ?definition . }}
  OPTIONAL {{ ?s dc:description ?description . }}
}}
LIMIT {limit}
"""
        rows = self.select(query, ["label", "definition", "description"])
        return [
            f"{clean_literal(row['label'], 120)}: {clean_literal(row['definition'] or row['description'], 420)}"
            for row in rows
            if row["label"]
        ]

    def threshold_context(self, limit: int = 30) -> list[str]:
        query = f"""
{SPARQL_PREFIXES}
SELECT ?label ?var ?op ?mod ?high ?very ?unit ?formula WHERE {{
  ?s a :RiskIndicator .
  OPTIONAL {{ ?s rdfs:label ?label . }}
  OPTIONAL {{ ?s :evaluatesWeatherVariable ?var . }}
  OPTIONAL {{ ?s :thresholdOperator ?op . }}
  OPTIONAL {{ ?s :moderateRiskThreshold ?mod . }}
  OPTIONAL {{ ?s :highRiskThreshold ?high . }}
  OPTIONAL {{ ?s :veryHighRiskThreshold ?very . }}
  OPTIONAL {{ ?s :weatherUnit ?unit . }}
  OPTIONAL {{ ?s :weatherRiskFormula ?formula . }}
  FILTER(BOUND(?mod) || BOUND(?formula))
}}
LIMIT {limit}
"""
        rows = self.select(query, ["label", "var", "op", "mod", "high", "very", "unit", "formula"])
        lines = []
        for row in rows:
            label = clean_literal(row["label"], 120)
            if row["formula"]:
                lines.append(f"Risk Formula ({label}): {clean_literal(row['formula'], 200)}")
            elif row["mod"]:
                var = compact_uri(row["var"])
                op = row["op"] or ">="
                unit = row["unit"] or ""
                lines.append(
                    f"Thresholds for {label} (Variable: {var}): "
                    f"Moderate {op} {row['mod']} {unit}, "
                    f"High {op} {row['high']} {unit}, "
                    f"Very High {op} {row['very']} {unit}"
                )
        return lines

    def nearby_glacial_lakes(self, lat: float, lon: float, limit: int = 5, radius_km: float = 50.0) -> list[NearbyFeature]:
        query = f"""
{SPARQL_PREFIXES}
SELECT ?lake ?label ?wkt ?lakeType ?lakeArea ?surfaceElevation ?susceptibilityLabel ?susceptibilityProb WHERE {{
  ?lake a :GlacierLake ;
        geo:hasGeometry ?geom .
  ?geom geo:asWKT ?wkt .
  OPTIONAL {{ ?lake rdfs:label ?label . }}
  OPTIONAL {{ ?lake :lakeType ?lakeType . }}
  OPTIONAL {{ ?lake :lakeArea ?lakeArea . }}
  OPTIONAL {{ ?lake :surfaceElevationM ?surfaceElevation . }}
  OPTIONAL {{ ?lake :susceptibilityLabel ?susceptibilityLabel . }}
  OPTIONAL {{ ?lake :susceptibilityProb ?susceptibilityProb . }}
}}
"""
        rows = self.select(
            query,
            [
                "lake",
                "label",
                "wkt",
                "lakeType",
                "lakeArea",
                "surfaceElevation",
                "susceptibilityLabel",
                "susceptibilityProb",
            ],
        )
        features: list[NearbyFeature] = []
        
        for row in rows:
            wkt_str = row.get("wkt", "")
            if not wkt_str:
                continue
                
            # Extract first coordinate pair from WKT: MULTIPOLYGON (((lon lat, ...)))
            # or POLYGON((lon lat, ...))
            match = re.search(r"\(\s*(-?\d+(?:\.\d+)?)\s+(-?\d+(?:\.\d+)?)", wkt_str)
            if not match:
                continue
                
            row_lon = parse_float(match.group(1))
            row_lat = parse_float(match.group(2))
            
            if row_lat is None or row_lon is None:
                continue
            distance = haversine_km(lat, lon, row_lat, row_lon)
            if distance > radius_km:
                continue
            uri = row["lake"]
            label = row["label"] or uri.rsplit("/", 1)[-1].replace(">", "")
            features.append(
                NearbyFeature(
                    uri=uri,
                    label=clean_literal(label, 160),
                    latitude=row_lat,
                    longitude=row_lon,
                    distance_km=distance,
                    lake_type=clean_literal(row.get("lakeType", ""), 80),
                    lake_area_m2=parse_float(row.get("lakeArea", "")),
                    surface_elevation_m=parse_float(row.get("surfaceElevation", "")),
                    susceptibility_label=clean_literal(row.get("susceptibilityLabel", ""), 80),
                    susceptibility_prob=parse_float(row.get("susceptibilityProb", "")),
                )
            )
        return sorted(features, key=lambda feature: feature.distance_km)[:limit]

    def lake_properties_by_id(self, lake_id: str) -> list[str]:
        query = f"""
{SPARQL_PREFIXES}
SELECT ?p ?pLabel ?o ?oLabel WHERE {{
  <https://w3id.org/cryosphere/ontology#lake/{lake_id}> ?p ?o .
  OPTIONAL {{ ?p rdfs:label ?pLabel . }}
  OPTIONAL {{ ?o rdfs:label ?oLabel . }}
}}
"""
        rows = self.select(query, ["p", "pLabel", "o", "oLabel"])
        if not rows:
            return []
        
        lines = [f"=== Properties for Lake ID: {lake_id} ==="]
        for row in rows:
            p_clean = row["pLabel"] or compact_uri(row["p"])
            o_clean = row["oLabel"] or clean_literal(row["o"], 120)
            if p_clean.startswith(":"):
                p_clean = p_clean[1:]
            lines.append(f"- {p_clean}: {o_clean}")
        return lines

    def river_properties_by_id(self, river_id: str) -> list[str]:
        river_id = normalize_graph_id(river_id)
        query = f"""
{SPARQL_PREFIXES}
SELECT ?p ?pLabel ?o ?oLabel WHERE {{
  <https://w3id.org/cryosphere/ontology#river/{sparql_escape(river_id)}> ?p ?o .
  OPTIONAL {{ ?p rdfs:label ?pLabel . }}
  OPTIONAL {{ ?o rdfs:label ?oLabel . }}
}}
"""
        rows = self.select(query, ["p", "pLabel", "o", "oLabel"])
        if not rows:
            return []

        lines = [f"=== Properties for River ID: {river_id} ==="]
        for row in rows:
            p_clean = row["pLabel"] or compact_uri(row["p"])
            o_clean = row["oLabel"] or clean_literal(row["o"], 180)
            if p_clean.startswith(":"):
                p_clean = p_clean[1:]
            lines.append(f"- {p_clean}: {o_clean}")
        return lines

    def river_summary(self, river_id: str) -> dict[str, str]:
        river_id = normalize_graph_id(river_id)
        query = f"""
{SPARQL_PREFIXES}
SELECT ?river ?label ?rid ?downstream ?downstreamLabel ?catchment ?nUp WHERE {{
  BIND(<{CRYO}river/{sparql_escape(river_id)}> AS ?river)
  ?river a :River .
  OPTIONAL {{ ?river rdfs:label ?label . }}
  OPTIONAL {{ ?river :riverId ?rid . }}
  OPTIONAL {{ ?river :downstreamOf ?downstream . OPTIONAL {{ ?downstream rdfs:label ?downstreamLabel . }} }}
  OPTIONAL {{ ?river :hasCatchment ?catchment . }}
  OPTIONAL {{ ?river :nBifurcationsUpstream ?nUp . }}
}}
LIMIT 10
"""
        rows = self.select(
            query,
            ["river", "label", "rid", "downstream", "downstreamLabel", "catchment", "nUp"],
            limit=10,
        )
        if not rows:
            return {}
        row = rows[0]
        return {
            "uri": row["river"],
            "id": row["rid"] or river_id,
            "label": clean_literal(row["label"] or f"river/{river_id}", 120),
            "downstream_uri": row.get("downstream", ""),
            "downstream_label": clean_literal(row.get("downstreamLabel", ""), 120),
            "catchment_uri": row.get("catchment", ""),
            "n_bifurcations_upstream": row.get("nUp", ""),
        }

    def upstream_rivers(self, river_id: str, limit: int = 30) -> list[dict[str, str]]:
        river_id = normalize_graph_id(river_id)
        query = f"""
{SPARQL_PREFIXES}
SELECT ?up ?upLabel ?upId ?path WHERE {{
  BIND(<{CRYO}river/{sparql_escape(river_id)}> AS ?river)
  {{
    ?up :downstreamOf ?river .
    BIND("incoming :downstreamOf" AS ?path)
  }}
  UNION
  {{
    ?river :upstreamOf ?up .
    BIND("outgoing :upstreamOf" AS ?path)
  }}
  ?up a :River .
  OPTIONAL {{ ?up rdfs:label ?upLabel . }}
  OPTIONAL {{ ?up :riverId ?upId . }}
}}
LIMIT {limit}
"""
        rows = self.select(query, ["up", "upLabel", "upId", "path"], limit=limit)
        seen: set[str] = set()
        rivers: list[dict[str, str]] = []
        for row in rows:
            uri = row["up"]
            if uri in seen:
                continue
            seen.add(uri)
            rid = row["upId"] or uri.rsplit("/", 1)[-1]
            rivers.append(
                {
                    "uri": uri,
                    "id": normalize_graph_id(rid),
                    "label": clean_literal(row["upLabel"] or f"river/{normalize_graph_id(rid)}", 120),
                    "path": row["path"],
                }
            )
        return rivers

    def upstream_rivers_text(self, river_id: str, limit: int = 30) -> str:
        river_id = normalize_graph_id(river_id)
        summary = self.river_summary(river_id)
        if not summary:
            return f"KG river lookup: river {river_id} was not found in the KG."

        upstream = self.upstream_rivers(river_id, limit=limit)
        lines = [
            f"KG river upstream lookup for river {river_id}:",
            f"- Target river: {summary['label']} ({compact_uri(summary['uri'])})",
        ]
        if summary.get("catchment_uri"):
            lines.append(f"- Catchment/sub-catchment: {compact_uri(summary['catchment_uri'])}")
        if summary.get("downstream_uri"):
            downstream_label = summary.get("downstream_label") or compact_uri(summary["downstream_uri"])
            lines.append(f"- Downstream river in KG: {downstream_label} ({compact_uri(summary['downstream_uri'])})")
        if summary.get("n_bifurcations_upstream"):
            lines.append(f"- nBifurcationsUpstream: {summary['n_bifurcations_upstream']}")

        if upstream:
            lines.append("- Upstream river reaches:")
            for item in upstream:
                lines.append(f"  * {item['id']}: {item['label']} ({compact_uri(item['uri'])})")
        else:
            lines.append("- No upstream river reaches are connected to this river in the KG.")
        return "\n".join(lines)

    def associated_river_for_lake(self, lake_id: str) -> dict[str, str]:
        lake_id = lake_id.upper()
        lake_uri = f"{CRYO}lake/{sparql_escape(lake_id)}"

        object_query = f"""
{SPARQL_PREFIXES}
SELECT ?lake ?sub ?subId ?river ?riverLabel ?riverId WHERE {{
  BIND(<{lake_uri}> AS ?lake)
  ?lake a :GlacierLake ;
        :hasSubCatchment ?sub .
  OPTIONAL {{ ?sub :subCatchmentId ?subId . }}
  OPTIONAL {{
    {{ ?sub :isSubCatchmentOfRiver ?river . }}
    UNION
    {{ ?sub :isCatchmentOf ?river . }}
    UNION
    {{ ?river :hasCatchment ?sub . }}
  }}
  OPTIONAL {{ ?river rdfs:label ?riverLabel . }}
  OPTIONAL {{ ?river :riverId ?riverId . }}
}}
LIMIT 10
"""
        rows = self.select(object_query, ["lake", "sub", "subId", "river", "riverLabel", "riverId"], limit=10)
        if rows:
            row = rows[0]
            sub_id = normalize_graph_id(row.get("subId") or row["sub"].rsplit("/", 1)[-1])
            river_uri = row.get("river") or f"{CRYO}river/{sub_id}"
            river_id = normalize_graph_id(row.get("riverId") or river_uri.rsplit("/", 1)[-1])
            return {
                "lake_uri": row["lake"],
                "subcatchment_uri": row["sub"],
                "subcatchment_id": sub_id,
                "river_uri": river_uri,
                "river_id": river_id,
                "river_label": clean_literal(row.get("riverLabel") or f"river/{river_id}", 120),
                "source": ":hasSubCatchment",
            }

        literal_query = f"""
{SPARQL_PREFIXES}
SELECT ?lake ?rawSub ?river ?riverLabel ?riverId WHERE {{
  BIND(<{lake_uri}> AS ?lake)
  ?lake a :GlacierLake ;
        :locatedInSubCatchment ?rawSub .
  BIND(IRI(CONCAT("{CRYO}river/", REPLACE(STR(?rawSub), "\\\\.0+$", ""))) AS ?river)
  OPTIONAL {{ ?river rdfs:label ?riverLabel . }}
  OPTIONAL {{ ?river :riverId ?riverId . }}
}}
LIMIT 5
"""
        rows = self.select(literal_query, ["lake", "rawSub", "river", "riverLabel", "riverId"], limit=5)
        if not rows:
            return {}
        row = rows[0]
        sub_id = normalize_graph_id(row["rawSub"])
        river_id = normalize_graph_id(row.get("riverId") or sub_id)
        return {
            "lake_uri": row["lake"],
            "subcatchment_uri": f"{CRYO}watershed/{sub_id}",
            "subcatchment_id": sub_id,
            "river_uri": row["river"] or f"{CRYO}river/{sub_id}",
            "river_id": river_id,
            "river_label": clean_literal(row.get("riverLabel") or f"river/{river_id}", 120),
            "source": ":locatedInSubCatchment literal",
        }

    def associated_river_for_lake_text(self, lake_id: str) -> str:
        lake_id = lake_id.upper()
        link = self.associated_river_for_lake(lake_id)
        if not link:
            return f"KG lake-river lookup: lake {lake_id} was not found with a sub-catchment/river link in the KG."
        return "\n".join(
            [
                f"KG lake-river lookup for lake {lake_id}:",
                f"- Lake: {compact_uri(link['lake_uri'])}",
                f"- Sub-catchment: {link['subcatchment_id']} ({compact_uri(link['subcatchment_uri'])})",
                f"- Associated/closest river by sub-catchment id: {link['river_label']} ({compact_uri(link['river_uri'])})",
                f"- Link source: {link['source']}",
            ]
        )

    def upstream_rivers_for_lake_text(self, lake_id: str, limit: int = 30) -> str:
        lake_id = lake_id.upper()
        link = self.associated_river_for_lake(lake_id)
        if not link:
            return f"KG upstream lookup: lake {lake_id} was not found with a sub-catchment/river link in the KG."

        river_id = link["river_id"]
        upstream = self.upstream_rivers(river_id, limit=limit)
        lines = [
            f"KG upstream lookup for lake {lake_id}:",
            f"- Lake sub-catchment: {link['subcatchment_id']} ({compact_uri(link['subcatchment_uri'])})",
            f"- Sub-catchment river: {link['river_label']} ({compact_uri(link['river_uri'])})",
            f"- Link source: {link['source']}",
        ]
        if upstream:
            lines.append("- Upstream river reaches of the sub-catchment river:")
            for item in upstream:
                lines.append(f"  * {item['id']}: {item['label']} ({compact_uri(item['uri'])})")
        else:
            lines.append("- No upstream river reaches are connected to the sub-catchment river in the KG.")

        summary = self.river_summary(river_id)
        if summary.get("downstream_uri"):
            downstream_label = summary.get("downstream_label") or compact_uri(summary["downstream_uri"])
            lines.append(f"- Downstream river from this river: {downstream_label} ({compact_uri(summary['downstream_uri'])})")
        return "\n".join(lines)

    def context_for_question(self, question: str, entity_limit: int = 6) -> str:
        sections: list[str] = []
        
        # Exact lake IDs (accept either N/E or E/N ordering, e.g. GL281050N902670E or GL281050E902670N)
        lake_ids = re.findall(r"\bGL\d+(?:N\d+E|E\d+N)\b", question, flags=re.IGNORECASE)
        lowered = question.lower()
        if "upstream" in lowered and lake_ids:
            for lake_id in lake_ids:
                sections.append("KG lake-river upstream traversal:\n" + self.upstream_rivers_for_lake_text(lake_id.upper()))
        elif lake_ids and any(term in lowered for term in ["closest river", "nearest river", "which river", "associated river"]):
            for lake_id in lake_ids:
                sections.append("KG lake-river traversal:\n" + self.associated_river_for_lake_text(lake_id.upper()))

        river_ids = re.findall(r"\briver\s+(\d{5,})\b|\b(\d{5,})\s+river\b", question, flags=re.IGNORECASE)
        flat_river_ids = [normalize_graph_id(a or b) for a, b in river_ids]
        if "upstream" in lowered and flat_river_ids:
            for river_id in flat_river_ids[:3]:
                sections.append("KG river upstream traversal:\n" + self.upstream_rivers_text(river_id))
        elif flat_river_ids:
            for river_id in flat_river_ids[:3]:
                props = self.river_properties_by_id(river_id)
                if props:
                    sections.append("KG River Context:\n" + "\n".join(props))

        for lake_id in lake_ids:
            props = self.lake_properties_by_id(lake_id.upper())
            if props:
                sections.append("KG Lake Context:\n" + "\n".join(props))
        coords = parse_lat_lon(question)
        if coords:
            lat, lon = coords
            lakes = self.nearby_glacial_lakes(lat, lon, limit=5, radius_km=50.0)
            if lakes:
                sections.append(
                    f"KG geospatial context: nearest glacial lakes to {lat:.6f}, {lon:.6f} "
                    "(coordinates are WGS84 decimal degrees; distance is haversine over representative points):\n"
                    + "\n\n".join(lake.as_text(rank) for rank, lake in enumerate(lakes, start=1))
                )
            else:
                sections.append(
                    f"KG geospatial context: no GlacierLake instances found within 50 km of {lat:.6f}, {lon:.6f}."
                )

        hits = self.entity_search(question, limit=entity_limit)
        if hits:
            sections.append("KG entity matches:\n" + "\n\n".join(hit.as_text() for hit in hits))
            relation_lines: list[str] = []
            hierarchy_lines: list[str] = []
            for hit in hits[:3]:
                relation_lines.extend(self.neighbourhood(hit.uri, limit=15))
                hierarchy_lines.extend(self.subclass_context(hit.uri, limit=10))
            if relation_lines:
                sections.append("KG relations:\n" + "\n".join(relation_lines[:45]))
            if hierarchy_lines:
                sections.append("KG class hierarchy:\n" + "\n".join(hierarchy_lines[:30]))

        if any(term in lowered for term in ["trigger", "cause", "causes", "causal", "mechanism"]):
            triggers = self.trigger_context()
            if triggers:
                sections.append("KG trigger reasoning context:\n" + "\n".join(triggers))
        if any(term in lowered for term in ["risk", "hazard", "exposure", "vulnerability", "susceptibility"]):
            risks = self.risk_context()
            if risks:
                sections.append("KG risk reasoning context:\n" + "\n".join(risks))
        if any(term in lowered for term in ["threshold", "weather", "variable", "temperature", "precipitation"]):
            thresholds = self.threshold_context()
            if thresholds:
                sections.append("KG weather thresholds context:\n" + "\n".join(thresholds))

        return "\n\n".join(sections)
