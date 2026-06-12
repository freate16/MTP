from __future__ import annotations

import datetime as dt
import random
from pathlib import Path
import geopandas as gpd
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as F
from tqdm import tqdm
from shapely.geometry import Polygon
from torch_geometric_temporal.nn.recurrent import GConvGRU
import logging

# Simple in-process cache for ERA5 bulk results to avoid repeated GEE requests
_GEE_CACHE: dict = {}

logger = logging.getLogger(__name__)


_EE = None


SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent

WEIGHT_PATH = SCRIPT_DIR / "gnn" / "glof_gnn_weights_final.pth"
EDGE_INDEX_PATH = SCRIPT_DIR / "edge_index3.pt"
NODE_MAPPING_PATH = SCRIPT_DIR / "node_mapping.csv"
NODE_GEOMETRY_PATH = PROJECT_DIR.parent / "gis_data" / "stage2_dataset_15.gpkg"
EARTH_ENGINE_PROJECT = "mtp-phase-2"

FEATURE_COLS = [
    "temperature_2m",
    "dewpoint_temperature_2m",
    "surface_pressure",
    "total_precipitation_sum",
    "snowfall_sum",
    "snow_depth_water_equivalent",
    "snowmelt_sum",
    "surface_runoff_sum",
    "sub_surface_runoff_sum",
]

TARGET_COLS = [
    "snowmelt_sum",
    "surface_runoff_sum",
    "sub_surface_runoff_sum",
]

AOI_COORDS = [
    (70.203815, 38.355372),
    (99.306191, 34.771871),
    (99.161404, 24.781503),
    (80.628547, 26.37417),
    (71.072543, 34.192719),
    (70.203815, 38.355372),
]
AOI_POLYGON = Polygon(AOI_COORDS)

# Dates are interpreted as DD/MM/YYYY.
TEST_DATES = ["02/02/2026", "08/04/2026", "05/05/2026", "03/02/2026"]

HISTORY_DAYS = 60
FORECAST_DAYS = 3
SEQ_LEN = HISTORY_DAYS + FORECAST_DAYS
NODE_HOPS = 2
RANDOM_SEED = 42


class GLOFPredictor(nn.Module):
    def __init__(self, node_features=9, hidden_channels=64, out_steps=3, out_vars=3, K=2):
        super().__init__()
        self.out_steps = out_steps
        self.out_vars = out_vars
        self.recurrent_1 = GConvGRU(in_channels=node_features, out_channels=hidden_channels, K=K)
        self.recurrent_2 = GConvGRU(in_channels=hidden_channels, out_channels=hidden_channels, K=K)
        self.mlp_head = nn.Sequential(
            nn.Linear(hidden_channels, hidden_channels),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(hidden_channels, out_steps * out_vars)
        )
        self.register_buffer("edge_index", torch.empty((2, 25094), dtype=torch.long))

    def forward(self, x, edge_index, edge_weight=None):
        if x.dim() == 3:
            x = x.unsqueeze(0)
        B, N, T, F_in = x.shape

        if B > 1:
            E = edge_index.size(1)
            offsets = (torch.arange(B, device=edge_index.device) * N).view(B, 1, 1)
            edge_index = (edge_index.unsqueeze(0) + offsets).permute(1, 0, 2).reshape(2, B * E)
            if edge_weight is not None:
                edge_weight = edge_weight.repeat(B)

        x = x.view(B * N, T, F_in)
        h1, h2 = None, None

        for t in range(T):
            h1 = self.recurrent_1(x[:, t, :], edge_index, edge_weight, H=h1)
            h1 = F.relu(h1)
            h2 = self.recurrent_2(h1, edge_index, edge_weight, H=h2)
            h2 = F.relu(h2)

        out = self.mlp_head(h2)
        return out.view(B, N, self.out_steps, self.out_vars)


def initialize_earth_engine() -> None:
    ee = get_earth_engine()
    try:
        ee.Initialize(project=EARTH_ENGINE_PROJECT)
    except Exception:
        ee.Authenticate()
        ee.Initialize(project=EARTH_ENGINE_PROJECT)


def get_earth_engine():
    global _EE
    if _EE is not None:
        return _EE

    try:
        import ee as earth_engine
    except ModuleNotFoundError as exc:
        if exc.name == "fcntl":
            raise ImportError(
                "The wrong PyPI package named 'ee' is installed and is shadowing "
                "Google Earth Engine. Run this in the geo_dl environment: "
                "pip uninstall ee && pip install earthengine-api"
            ) from exc
        raise

    if not hasattr(earth_engine, "ImageCollection"):
        raise ImportError(
            "Imported package 'ee' is not Google Earth Engine. Run: "
            "pip uninstall ee && pip install earthengine-api"
        )

    _EE = earth_engine
    return _EE


def load_graph_nodes() -> gpd.GeoDataFrame:
    mapping = pd.read_csv(NODE_MAPPING_PATH)
    lakes = gpd.read_file(NODE_GEOMETRY_PATH)

    merge_cols = ["GLAKE_ID", "era5_fid"]
    node_cols = merge_cols + ["geometry"]
    nodes = mapping.merge(lakes[node_cols], on=merge_cols, how="left")
    missing_geom = nodes["geometry"].isna().sum()
    if missing_geom:
        raise ValueError(f"{missing_geom} graph nodes could not be matched to lake geometries.")

    nodes_gdf = gpd.GeoDataFrame(nodes, geometry="geometry", crs=lakes.crs)
    nodes_gdf = nodes_gdf.sort_values("node_index").reset_index(drop=True)

    if not nodes_gdf.geometry.geom_type.eq("Point").all():
        nodes_gdf["geometry"] = nodes_gdf.geometry.centroid

    return nodes_gdf


def choose_random_glake_nodes(
    nodes_gdf: gpd.GeoDataFrame,
    polygon: Polygon,
    count: int,
    edge_index: torch.Tensor | None = None,
) -> gpd.GeoDataFrame:
    nodes_wgs84 = nodes_gdf.to_crs("EPSG:4326").copy()
    candidates = nodes_wgs84[nodes_wgs84.geometry.within(polygon)]
    if edge_index is not None:
        connected_nodes = set(torch.unique(edge_index.cpu()).numpy().astype(int).tolist())
        candidates = candidates[candidates["node_index"].isin(connected_nodes)]
    if candidates.empty:
        raise ValueError("No connected trained graph nodes / GLAKE_IDs were found inside the AOI polygon.")

    candidate_indices = candidates.index.tolist()
    if len(candidate_indices) >= count:
        chosen_indices = random.sample(candidate_indices, count)
    else:
        print(
            f"Only {len(candidate_indices)} GLAKE_IDs found inside AOI; "
            "sampling with replacement."
        )
        chosen_indices = random.choices(candidate_indices, k=count)

    return nodes_wgs84.loc[chosen_indices].reset_index(drop=True)


def build_k_hop_subgraph(edge_index: torch.Tensor, center_node: int, hops: int = 2):
    src = edge_index[0].cpu().numpy()
    dst = edge_index[1].cpu().numpy()

    selected = {int(center_node)}
    frontier = {int(center_node)}
    for _ in range(hops):
        if not frontier:
            break
        frontier_arr = np.fromiter(frontier, dtype=np.int64)
        mask = np.isin(src, frontier_arr) | np.isin(dst, frontier_arr)
        neighbors = set(src[mask].astype(int)).union(set(dst[mask].astype(int)))
        frontier = neighbors - selected
        selected.update(neighbors)

    node_ids = sorted(selected)
    node_to_local = {node_id: i for i, node_id in enumerate(node_ids)}
    edge_mask = np.isin(src, node_ids) & np.isin(dst, node_ids)
    sub_src = src[edge_mask]
    sub_dst = dst[edge_mask]

    if len(sub_src) == 0:
        sub_edge_index = torch.empty((2, 0), dtype=torch.long)
    else:
        sub_edges = [[node_to_local[int(s)], node_to_local[int(d)]] for s, d in zip(sub_src, sub_dst)]
        sub_edge_index = torch.tensor(sub_edges, dtype=torch.long).t().contiguous()

    center_local = node_to_local[int(center_node)]
    return node_ids, sub_edge_index, center_local


def parse_date_ddmmyyyy(date_text: str) -> dt.date:
    return dt.datetime.strptime(date_text, "%d/%m/%Y").date()


def fetch_era5_land_daily_for_nodes(
    nodes_gdf: gpd.GeoDataFrame,
    target_date: dt.date,
    history_days: int = HISTORY_DAYS,
    forecast_days: int = FORECAST_DAYS,
) -> tuple[np.ndarray, list[dt.date]]:
    """Fetch 90 history days. The next 3 forecast days are naturally NaN for history array filling.

    Optimized logic:
    1. Rounds coordinates to 1 decimal place (~11km, ERA5 resolution) to prevent redundant queries.
    2. Uses Earth Engine .map() to process all 90 days in a single backend operation, bringing data back in one getInfo().
    """
    ee = get_earth_engine()
    
    # We fetch up to today/target_date. We need strictly history_days worth of past data.
    # We add 1 day so that endDate is exclusive and covers target_date.
    coll = ee.ImageCollection("ECMWF/ERA5_LAND/DAILY_AGGR").select(FEATURE_COLS)
    latest_img = coll.sort('system:time_start', False).first()
    if latest_img is None:
        raise RuntimeError("No ERA5-Land images found in collection")
    latest_date_str = latest_img.date().format('YYYY-MM-dd').getInfo()
    latest_date = dt.date.fromisoformat(latest_date_str)

    # We fetch history_days up to the latest available date. Days after latest_date
    # (including target_date if it is newer) will remain as NaN and be imputed later.
    fetch_end_date = ee.Date(latest_date.isoformat()).advance(1, 'day')
    fetch_start_date = ee.Date(latest_date.isoformat()).advance(-history_days + 1, 'day')

    # all_dates still cover the historical window plus forecast days so downstream
    # code keeps the 90 + 3 shape and we silently impute the missing forward days.
    start_date = latest_date - dt.timedelta(days=history_days - 1)
    all_dates = [start_date + dt.timedelta(days=i) for i in range(history_days + forecast_days)]

    nodes_wgs84 = nodes_gdf.to_crs("EPSG:4326")
    
    # Optimization: Deduplicate coordinates for ERA5 resolution (approx 0.1 degree)
    unique_coords = {}
    node_to_coord = {}
    
    for local_idx, row in enumerate(nodes_wgs84.itertuples()):
        lon, lat = float(row.geometry.x), float(row.geometry.y)
        # Snap to 0.1 degree intervals (~11km spacing of ERA5-Land)
        snapped_lon, snapped_lat = round(lon, 1), round(lat, 1)
        coord_key = f"{snapped_lon}_{snapped_lat}"
        
        node_to_coord[local_idx] = coord_key
        if coord_key not in unique_coords:
            unique_coords[coord_key] = {"lon": snapped_lon, "lat": snapped_lat}

    ee_features = []
    for coord_key, coords in unique_coords.items():
        ee_features.append(
            ee.Feature(
                ee.Geometry.Point([coords["lon"], coords["lat"]]),
                {"coord_key": coord_key}
            )
        )
    point_fc = ee.FeatureCollection(ee_features)

    values = np.full((len(all_dates), len(nodes_wgs84), len(FEATURE_COLS)), np.nan, dtype=np.float32)
    base_collection = coll.filterDate(fetch_start_date, fetch_end_date)

    def extract_stats(image):
        date_str = image.date().format("YYYY-MM-dd")
        stats = image.reduceRegions(collection=point_fc, reducer=ee.Reducer.mean(), scale=11132)
        return stats.map(lambda f: f.set("date", date_str))

    # Chunk the fetch so we can show a progress bar while still reducing the
    # number of getInfo() calls. We fetch in chunks of days (default 10).
    chunk_days = 10
    cache_key = (tuple(sorted(unique_coords.keys())), start_date.isoformat(), latest_date.isoformat(), chunk_days)
    if cache_key in _GEE_CACHE:
        print(f"[ERA5] Reusing cached live fetch for {len(unique_coords)} unique pixels over {history_days} days...")
        logger.debug("Reusing cached ERA5 bulk results for key=%s", cache_key)
        results = _GEE_CACHE[cache_key]
    else:
        print(f"[ERA5] Fetching live ERA5 for {len(unique_coords)} unique pixels over {history_days} days...")
        logger.info("Fetching ERA5 for %d unique pixels over %d days (chunks=%d)...", len(unique_coords), history_days, chunk_days)
        results_features = []
        # build list of python dates for chunking
        python_start = start_date
        total_steps = history_days * len(unique_coords)
        with tqdm(total=history_days, desc="Fetching ERA5 (days)", leave=True) as day_pbar:
            for i in range(0, history_days, chunk_days):
                chunk_start = python_start + dt.timedelta(days=i)
                chunk_end = min(python_start + dt.timedelta(days=i + chunk_days), latest_date + dt.timedelta(days=1))
                # filter the collection for this chunk
                chunk_coll = coll.filterDate(chunk_start.isoformat(), chunk_end.isoformat())
                chunk_results = chunk_coll.map(extract_stats).flatten().getInfo()
                # extend features
                features = chunk_results.get("features", [])
                results_features.extend(features)
                # advance progress by the number of days fetched in the chunk
                day_pbar.update((chunk_end - chunk_start).days)

        results = {"features": results_features}
        _GEE_CACHE[cache_key] = results
    print(f"[ERA5] Completed live fetch for {len(unique_coords)} unique pixels over {history_days} days.")

    # Map the unified results back to the individual lake nodes
    # First, create a dictionary of day -> coord_key -> features
    stats_dict = {}
    for feature in results.get("features", []):
        props = feature.get("properties", {})
        date_str = props.get("date")
        key = props.get("coord_key")
        if date_str and key:
            if date_str not in stats_dict:
                stats_dict[date_str] = {}
            stats_dict[date_str][key] = props

    # Parse and fill array
    for t_idx, day in enumerate(all_dates):
        day_str = day.isoformat()
        if day_str not in stats_dict:
            continue
            
        day_data = stats_dict[day_str]
        for local_idx in range(len(nodes_wgs84)):
            coord_key = node_to_coord[local_idx]
            props = day_data.get(coord_key, {})
            for f_idx, col in enumerate(FEATURE_COLS):
                val = props.get(col)
                if val is not None:
                    values[t_idx, local_idx, f_idx] = float(val)

    return values, all_dates


def build_model_input(raw_window: np.ndarray) -> tuple[torch.Tensor, np.ndarray]:
    """Apply the same normalization logic used in training.

    Training used node-wise mean/std from the 90-day history window, not one
    global scaler. The model target stayed unnormalized, so predictions are
    compared directly with raw ERA5 hydrology values.
    """
    if raw_window.shape[0] != SEQ_LEN:
        raise ValueError(f"Expected {SEQ_LEN} timesteps, got {raw_window.shape[0]}.")

    target = raw_window[HISTORY_DAYS:, :, 6:9].copy()

    mean = np.nanmean(raw_window[:HISTORY_DAYS], axis=0, keepdims=True)
    std = np.nanstd(raw_window[:HISTORY_DAYS], axis=0, keepdims=True) + 1e-8
    normalized_window = (raw_window - mean) / std

    history = normalized_window[:HISTORY_DAYS]
    forecast_input = normalized_window[HISTORY_DAYS:].copy()
    forecast_input[:, :, 6:9] = 0.0

    x_seq = np.concatenate([history, forecast_input], axis=0)
    x_seq = np.nan_to_num(x_seq, nan=0.0, posinf=0.0, neginf=0.0)
    x_seq = x_seq.transpose(1, 0, 2)

    x_tensor = torch.from_numpy(np.ascontiguousarray(x_seq, dtype=np.float32)).unsqueeze(0)
    return x_tensor, target


def masked_metrics(pred: np.ndarray, target: np.ndarray) -> dict[str, float]:
    mask = ~np.isnan(target)
    if not mask.any():
        return {"mae": float("nan"), "rmse": float("nan")}

    diff = pred[mask] - target[mask]
    return {
        "mae": float(np.mean(np.abs(diff))),
        "rmse": float(np.sqrt(np.mean(diff**2))),
    }


def load_model_and_graph(device: torch.device):
    edge_index = torch.load(EDGE_INDEX_PATH, map_location="cpu").long()
    model = GLOFPredictor(node_features=9, hidden_channels=64, out_steps=3, out_vars=3, K=2).to(device)
    model.load_state_dict(torch.load(WEIGHT_PATH, map_location=device))
    model.eval()
    return model, edge_index

_CACHED_MODEL_AND_GRAPH = None

def predict_for_lake(glake_id: str, target_date: dt.date = None) -> str:
    global _CACHED_MODEL_AND_GRAPH
    if target_date is None:
        target_date = dt.date.today()
        
    initialize_earth_engine()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    if _CACHED_MODEL_AND_GRAPH is None:
        _CACHED_MODEL_AND_GRAPH = load_model_and_graph(device)
    model, edge_index = _CACHED_MODEL_AND_GRAPH
    
    nodes_gdf = load_graph_nodes()
    
    # Find the node for the given GLAKE_ID
    lake_row = nodes_gdf[nodes_gdf["GLAKE_ID"] == glake_id]
    if lake_row.empty:
        return f"Error: No trained graph node found for GLAKE_ID '{glake_id}'."
    
    center_node = int(lake_row["node_index"].iloc[0])
    node_ids, sub_edge_index, center_local = build_k_hop_subgraph(edge_index, center_node, hops=NODE_HOPS)
    sub_nodes = nodes_gdf.set_index("node_index").loc[node_ids].reset_index()
    
    try:
        raw_window, all_dates = fetch_era5_land_daily_for_nodes(sub_nodes, target_date)
        x_tensor, target = build_model_input(raw_window)
    except Exception as e:
        return f"Error fetching ERA5 data or building input: {e}"
        
    x_tensor = x_tensor.to(device)
    sub_edge_index = sub_edge_index.to(device)
    
    with torch.no_grad():
        pred = model(x_tensor, sub_edge_index).squeeze(0).cpu().numpy()

    # FIX: Clip negative predictions to 0.0 for physical consistency
    pred = np.maximum(pred, 0.0)

    center_pred = pred[center_local]
    forecast_dates = all_dates[HISTORY_DAYS:]
    
    lines = [f"Forecast for {glake_id} starting {target_date.isoformat()}:"]
    for step_idx, forecast_day in enumerate(forecast_dates):
        lines.append(f"  Date: {forecast_day.isoformat()}")
        for var_idx, var_name in enumerate(TARGET_COLS):
            val = float(center_pred[step_idx, var_idx])
            val_str = f"{val:.4f}"
            lines.append(f"    - {var_name}: {val_str}")
            
    return "\n".join(lines)


def run_inference_check() -> pd.DataFrame:
    random.seed(RANDOM_SEED)
    initialize_earth_engine()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model, edge_index = load_model_and_graph(device)
    nodes_gdf = load_graph_nodes()

    print(f"Model loaded from {WEIGHT_PATH}")
    print(f"Graph loaded from {EDGE_INDEX_PATH}: {edge_index.size(1):,} edges")
    print(f"Running on {device}")

    selected_nodes = choose_random_glake_nodes(
        nodes_gdf,
        AOI_POLYGON,
        count=len(TEST_DATES),
        edge_index=edge_index,
    )

    rows = []
    for date_text, selected_node in zip(TEST_DATES, selected_nodes.itertuples()):
        target_date = parse_date_ddmmyyyy(date_text)
        center_node = int(selected_node.node_index)
        glake_id = selected_node.GLAKE_ID
        lon = float(selected_node.geometry.x)
        lat = float(selected_node.geometry.y)
        node_ids, sub_edge_index, center_local = build_k_hop_subgraph(edge_index, center_node, hops=NODE_HOPS)

        sub_nodes = nodes_gdf.set_index("node_index").loc[node_ids].reset_index()
        print("\n" + "-" * 72)
        print(f"Requested date: {date_text} -> forecast start {target_date.isoformat()}")
        print(f"Random GLAKE_ID: {glake_id} | node_index={center_node}")
        print(f"Lake centroid: lon={lon:.5f}, lat={lat:.5f}")
        print(f"Subgraph: {len(node_ids)} nodes, {sub_edge_index.size(1)} edges, hops={NODE_HOPS}")

        raw_window, all_dates = fetch_era5_land_daily_for_nodes(sub_nodes, target_date)
        x_tensor, target = build_model_input(raw_window)

        x_tensor = x_tensor.to(device)
        sub_edge_index = sub_edge_index.to(device)

        with torch.no_grad():
            pred = model(x_tensor, sub_edge_index).squeeze(0).cpu().numpy()
        
        # FIX: Clip negative predictions to 0.0 for physical consistency
        pred = np.maximum(pred, 0.0)

        center_pred = pred[center_local]
        center_target = target[:, center_local, :]
        metrics = masked_metrics(center_pred, center_target)

        forecast_dates = all_dates[HISTORY_DAYS:]
        print(f"Central-node MAE: {metrics['mae']:.6f}, RMSE: {metrics['rmse']:.6f}")

        for step_idx, forecast_day in enumerate(forecast_dates):
            for var_idx, var_name in enumerate(TARGET_COLS):
                rows.append(
                    {
                        "requested_date": date_text,
                        "forecast_date": forecast_day.isoformat(),
                        "glake_id": glake_id,
                        "node_index": center_node,
                        "node_lon": lon,
                        "node_lat": lat,
                        "subgraph_nodes": len(node_ids),
                        "subgraph_edges": int(sub_edge_index.size(1)),
                        "target_variable": var_name,
                        "prediction": float(center_pred[step_idx, var_idx]),
                        "actual": float(center_target[step_idx, var_idx])
                        if not np.isnan(center_target[step_idx, var_idx])
                        else np.nan,
                        "absolute_error": float(abs(center_pred[step_idx, var_idx] - center_target[step_idx, var_idx]))
                        if not np.isnan(center_target[step_idx, var_idx])
                        else np.nan,
                    }
                )

        case_df = pd.DataFrame(rows).tail(FORECAST_DAYS * len(TARGET_COLS))
        print(case_df[["forecast_date", "target_variable", "prediction", "actual", "absolute_error"]])

    results = pd.DataFrame(rows)
    output_path = SCRIPT_DIR / "inference_accuracy_check.csv"
    results.to_csv(output_path, index=False)
    print(f"\nSaved inference accuracy results to {output_path}")
    return results


if __name__ == "__main__":
    run_inference_check()
