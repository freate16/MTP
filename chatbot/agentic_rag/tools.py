import sys
import torch # CRITICAL: Import torch first to prevent WinError 1114 on Windows
import os
import math
from datetime import date, datetime
from pathlib import Path
import warnings
import contextlib
import io
import re

# Suppress noisy warnings
warnings.filterwarnings("ignore")

# Heavy GIS/ML Imports (Top-level to prevent DLL conflicts on Windows)
try:
    import numpy as np
    import pandas as pd
    import geopandas as gpd
    import rasterio
    import fiona
    import pyproj
    import ee
    import geemap
    import matplotlib.pyplot as plt
    import segmentation_models_pytorch as smp
    from rasterio.features import rasterize
    from scipy.ndimage import label
    from shapely.geometry import box, Point
    from shapely.ops import transform as shapely_transform
except Exception as e:
    print(f"Warning: Failed to load some GIS/ML libraries: {e}")

# Setup paths to import existing modules
DEPLOYMENT_ROOT = Path(__file__).resolve().parent.parent.parent
PROJECT_ROOT = DEPLOYMENT_ROOT
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
RAG_ROOT = PROJECT_ROOT / "chatbot" / "rag"
if str(RAG_ROOT) not in sys.path:
    sys.path.insert(0, str(RAG_ROOT))

from chatbot.rag.kg_store import KgStore
from chatbot.rag.hybrid_graphrag import retrieve_vector_context
# The import block handles potential missing tools gracefully
try:
    from chatbot.dual_inference import explain_glof_prediction
except ImportError:
    explain_glof_prediction = None

KG_STORE_DIR = PROJECT_ROOT / "chatbot" / "rag" / "kg_store"
INDEX_DIR = PROJECT_ROOT / "chatbot" / "rag" / "index"

# Configuration for GIS Data
DATA_DIR = PROJECT_ROOT / "gis_data"
LAKES_PATH = DATA_DIR / "stage2_dataset_15.gpkg"
RIVERS_PATH = DATA_DIR / "river_network.gpkg"
BUILDINGS_PATH = DATA_DIR / "final_merged_clipped_buildings.gpkg"

# --- Detection Tool Constants ---
CKPT_PATH = PROJECT_ROOT / "models" / "lake_segmentation" / "finetuned_model_best.pth"
DETECTION_OUT_DIR = PROJECT_ROOT / "agent_detection_outputs"

# Normalization stats for Detection model
S2_MEAN = torch.tensor([857.6, 1044.0, 1356.7, 1574.4, 1786.2, 2076.5, 2215.2, 2277.8, 2348.5, 2243.7, 2665.0, 2217.2]).view(12, 1, 1)
S2_STD  = torch.tensor([626.3, 709.2, 748.7, 825.5, 773.5, 786.1, 810.8, 834.9, 833.6, 729.6, 875.7, 851.3]).view(12, 1, 1)
S1_MEAN = torch.tensor([-9.25, -18.00]).view(2, 1, 1)
S1_STD  = torch.tensor([5.90, 5.92]).view(2, 1, 1)
DEM_MEAN = torch.tensor([4299.8]).view(1, 1, 1)
DEM_STD  = torch.tensor([901.0]).view(1, 1, 1)

# We create a persistent global dictionary so variables persist between python executions
GLOBAL_PYTHON_STATE = {}

def execute_python_code(code: str) -> str:
    """
    Use this tool to execute arbitrary Python code for spatial reasoning and data analysis.
    SCHEMA GUIDE:
    - Primary dataset: r'D:\\Rubel\\M.Tech\\MTP\\Phase 2\\model_data\\Final data\\stage2_dataset_15.gpkg'
    - Dataset CRS: ESRI:102025 (Asia North Albers, units=meters).
    - Elevation Columns: Use 'Elevation' or 'surface_elevation_m' for lake elevation.
    - LAKE TYPE MAPPING: Use 'lake_type' column with these codes:
      * M(e): End-moraine Dammed
      * M(l): Lateral Moraine Dammed
      * M(lg): Lateral Moraine Dammed (with ice)
      * M(o): Other Moraine Dammed
      * O: Other Glacial Lake
      * E(c): Cirque Erosion
      * E(o): Other Glacial Erosion
      * E(v): Glacier Trough Valley Erosion
    - MULTI-LAKE QUERY (CRITICAL FOR CASCADING GLOFS): To compare elevations of multiple lakes, pass their GLAKE_IDs in a list.
      Example:
      ```python
      import geopandas as gpd
      lakes = gpd.read_file(r'D:\\Rubel\\M.Tech\\MTP\\Phase 2\\model_data\\Final data\\stage2_dataset_15.gpkg')
      target_ids = ['GL088814E27991N', 'GL088743E27992N']
      subset = lakes[lakes['GLAKE_ID'].isin(target_ids)]
      print(subset[['GLAKE_ID', 'Elevation']].to_string(index=False))
      ```
    - COORDINATE QUERIES (CRITICAL): User provides Lat/Lon (WGS84). You MUST re-project the point to the dataset CRS (ESRI:102025) before calculating distances.
      Example:
      ```python
      import geopandas as gpd
      from shapely.geometry import Point
      lakes = gpd.read_file(r'D:\\Rubel\\M.Tech\\MTP\\Phase 2\\model_data\\Final data\\stage2_dataset_15.gpkg')
      # 1. Create point in WGS84 (EPSG:4326), then re-project to dataset's projected CRS (ESRI:102025)
      user_pt = gpd.GeoDataFrame([{'geometry': Point(88.70, 28.98)}], crs="EPSG:4326").to_crs(lakes.crs).geometry.iloc[0]
      # 2. Query within 10km (10000 meters)
      nearby = lakes[lakes.geometry.distance(user_pt) < 10000]
      if not nearby.empty:
          avg_elev = nearby['Elevation'].mean()
          print(f"Found {len(nearby)} lakes. Average Elevation: {avg_elev:.2f}m")
      else:
          print("No lakes found within 10km of coordinates.")
      ```
    Input: A valid, executable Python script. Use print() for results.
    """
    # Clean up markdown formatting if the LLM adds it
    code = code.strip()
    if code.startswith("```python"):
        code = code[9:]
    elif code.startswith("```"):
        code = code[3:]
    if code.endswith("```"):
        code = code[:-3]
    
    # Capture standard output
    output_buffer = io.StringIO()
    try:
        with contextlib.redirect_stdout(output_buffer):
            # Execute the code in the persistent global state
            exec(code, GLOBAL_PYTHON_STATE)
        output = output_buffer.getvalue()
        if not output.strip():
            return "Code executed successfully, but nothing was printed. Use print() to output results."
        return output
    except Exception as e:
        import traceback
        return f"Python Error:\n{traceback.format_exc()}"

def get_dataset_info(dummy_input: str = "") -> str:
    """
    Returns the schema and summary statistics of the glacial lake dataset.
    Use this BEFORE writing Python code if you are unsure about column names or unique values.
    Input: Any string (ignored).
    """
    try:
        lakes = gpd.read_file(LAKES_PATH)
        info = [f"Dataset Schema (Top 20 columns of {len(lakes.columns)}):", ", ".join(lakes.columns[:20])]
        info.append("\nSample lake_type values: " + ", ".join(lakes['lake_type'].dropna().unique()[:10]))
        info.append(f"\nTotal Records: {len(lakes)}")
        return "\n".join(info)
    except Exception as e:
        return f"Error reading schema: {str(e)}"

def query_lakes_by_subcatchment(subcatchment_id: str) -> str:
    """
    Finds all glacial lakes belonging to a specific sub-catchment or basin ID.
    Use this when the user provides a numeric basin ID (e.g., '170067682').
    Returns a list of Lake IDs and their basic properties (Elevation, CAGR, Area, Type).
    Input: The numeric sub-catchment ID.
    """
    try:
        # Normalize input
        sid_str = subcatchment_id.strip().replace("'", "").replace('"', "")
        sid = float(sid_str)
        lakes = gpd.read_file(LAKES_PATH)
        # Handle potential variations in column name
        col = 'sub-catchment_id' if 'sub-catchment_id' in lakes.columns else 'sub-catchment'
        in_basin = lakes[lakes[col] == sid]
        if in_basin.empty:
            return f"No lakes found in sub-catchment {subcatchment_id}."
        
        # Sort by CAGR to help the agent find the "highest"
        if 'area_cagr_total_pct' in in_basin.columns:
            in_basin = in_basin.sort_values(by='area_cagr_total_pct', ascending=False)
            
        res = [f"Found {len(in_basin)} lake(s) in sub-catchment {subcatchment_id}:"]
        for _, row in in_basin.head(15).iterrows():
            cagr = row.get('area_cagr_total_pct', 0.0)
            elev = row.get('Elevation', row.get('surface_elevation_m', 'N/A'))
            if isinstance(elev, float): elev = f"{elev:.1f}m"
            res.append(f"- ID: {row['GLAKE_ID']} | Elev: {elev} | CAGR: {cagr:.4f}% | Type: {row.get('lake_type', 'N/A')}")
        return "\n".join(res)
    except Exception as e:
        return f"Error querying sub-catchment: {str(e)}"

def query_lake_properties_kg(lake_id: str) -> str:
    """
    Use this tool to get exact, structured facts about a specific glacial lake from the Knowledge Graph.
    This includes area, volume, elevation, dam type, and growth trends (CAGR).
    Input: The exact Lake ID (e.g., 'GL088561E28014N').
    Returns: A structured string of lake properties.
    """
    kg = KgStore(KG_STORE_DIR)
    props = kg.lake_properties_by_id(lake_id)
    if not props:
        return f"Lake ID {lake_id} not found in the Knowledge Graph."
    return "\n".join(props)

def query_downstream_rivers_kg(lake_id: str) -> str:
    """
    Use this tool to perform topological reasoning. It finds which rivers are connected 
    to a lake and traces the downstream path.
    Input: The exact Lake ID.
    Returns: A list of connected rivers and downstream exposure elements.
    """
    kg = KgStore(KG_STORE_DIR)
    res = kg.associated_river_for_lake_text(lake_id)
    if not res:
        return f"No downstream river connection found for Lake {lake_id}."
    return res
def is_tabular_query(query: str) -> bool:
    lowered = query.lower()
    has_table_signal = any(term in lowered for term in ["table", "distribution", "range", "stat", "count", "number of"])
    has_category_signal = any(term in lowered for term in ["elevation", "area", "type", "moraine", "erosion"])
    return has_table_signal and has_category_signal

def search_scientific_papers(query: str) -> str:
    """
    Use this tool to search ingested PDFs, scientific papers, and literature reports.
    Use this when you need background knowledge, causes, mechanisms, or historical facts.
    Returns excerpts and structured Markdown tables from scientific literature.
    Input: A search query string (e.g., 'Table for elevation distribution in Ganga basin').
    """
    # Adjust parameters for tabular/statistical queries to favor BM25 (keywords)
    top_k = 5
    alpha = 0.65
    if is_tabular_query(query):
        top_k = 10  # Increase depth to catch tables near headers
        alpha = 0.45 # Favor BM25 (keywords) for structured table lookup
        print(f"DEBUG: Tabular query detected. Using hybrid alpha={alpha}, top_k={top_k}")

    from chatbot.rag.hybrid_graphrag import retrieve_vector_context
    context, evidence = retrieve_vector_context(
        query, 
        index_dir=INDEX_DIR, 
        top_k=top_k,
        dense_top_k=30,
        bm25_top_k=30,
        alpha=alpha
    )
    if not context:
        return "No relevant scientific papers found for this query."
    return context


def get_glof_risk_forecast(lake_id: str) -> str:
    """
    Use this tool to run live machine learning predictions (XGBoost & GNN) for a glacial lake.
    It returns the current GLOF susceptibility probability, hazard index, and recent weather anomalies.
    Input: The exact Lake ID.
    Returns: A forecast report string.
    """
    if not explain_glof_prediction:
        return "Forecasting model is offline or unavailable."
    try:
        explanation = explain_glof_prediction(lake_id)
        if not explanation:
             return f"No forecast data available for {lake_id}."
        return explanation
    except Exception as e:
        return f"Error running forecast for {lake_id}: {str(e)}"

def get_regional_glof_forecast(input_str: str) -> str:
    """
    Runs a batched GLOF risk forecast for all lakes within a specified radius (buffer) 
    of a central point (lat/lon). This is much faster than querying lakes individually.
    Use this when the user asks about risk in a "region", "area", "basin", or "near [coordinates]".
    Input: A comma-separated string "lat, lon, buffer_km" (e.g., '27.895, 87.013, 10.0').
    """
    try:
        parts = [p.strip() for p in input_str.split(',')]
        if len(parts) < 2:
            return "Error: Regional forecast requires at least 'lat, lon'. Example: '27.895, 87.013, 5.0'"
        
        lat = float(parts[0])
        lon = float(parts[1])
        buffer_km = float(parts[2]) if len(parts) > 2 else 50.0
        
        from chatbot.dual_inference import explain_regional_glof
        return explain_regional_glof(lat, lon, buffer_km)
    except Exception as e:
        return f"Error parsing regional forecast input: {str(e)}"

def gaussian_window_2d(size, sigma=None, device="cpu"):
    import torch
    if sigma is None: sigma = size / 4.0
    coords = torch.arange(size, device=device, dtype=torch.float32) - (size - 1) / 2.0
    g1 = torch.exp(-(coords ** 2) / (2.0 * sigma ** 2))
    g2 = g1[:, None] * g1[None, :]
    return g2 / g2.max()

def predict_sliding_window(model, tensor, window=224, stride=64, batch_size=4, device="cuda"):
    import torch
    """Runs inference over a large image using an overlapping sliding window."""
    _, H, W = tensor.shape
    pad_h = max(0, window - H)
    pad_w = max(0, window - W)
    if pad_h or pad_w:
        tensor = torch.nn.functional.pad(tensor.unsqueeze(0), (0, pad_w, 0, pad_h), mode='reflect').squeeze(0)
        _, H, W = tensor.shape

    starts_y = list(range(0, H - window + 1, stride))
    starts_x = list(range(0, W - window + 1, stride))
    if starts_y[-1] + window < H: starts_y.append(H - window)
    if starts_x[-1] + window < W: starts_x.append(W - window)
    coords = [(y, x) for y in starts_y for x in starts_x]

    weights = gaussian_window_2d(window, sigma=window/6.0, device=device)
    pred_logits = torch.zeros((H, W), device=device, dtype=torch.float32)
    pred_weights = torch.zeros((H, W), device=device, dtype=torch.float32)

    for offset in range(0, len(coords), batch_size):
        chunk = coords[offset: offset + batch_size]
        batch = torch.stack([tensor[:, y:y+window, x:x+window] for y, x in chunk]).to(device)
        
        with torch.amp.autocast(device_type="cuda", enabled=(device == "cuda" or str(device) == "cuda")):
            logits = model(batch)
            
        for i, (y, x) in enumerate(chunk):
            pred_logits[y:y+window, x:x+window] += logits[i, 0].float() * weights
            pred_weights[y:y+window, x:x+window] += weights

    prob = torch.sigmoid(pred_logits / pred_weights.clamp_min(1e-6)).cpu().numpy()
    if pad_h or pad_w:
        prob = prob[:H-pad_h, :W-pad_w]
    return prob

def detect_lakes_and_calculate_area(input_str: str) -> str:
    """
    Perform deep-learning based glacial lake detection and area trend analysis using Sentinel-2, Sentinel-1, and DEM data from GEE.
    WARNING: This tool is slow. USE ONLY IF requested by the user.
    Input format: "lake_id, mode, start, end"
    Modes: 'yearly' or 'monthly'.
    Example Yearly: 'GL088561E28014N, yearly, 2021, 2025'
    Example Monthly: 'GL088561E28014N, monthly, 2024-06, 2025-01'
    """
    import numpy as np
    import pandas as pd
    import torch
    import segmentation_models_pytorch as smp
    import ee
    import geemap
    import rasterio
    import matplotlib.pyplot as plt
    from rasterio.features import rasterize
    from scipy.ndimage import label
    from shapely.geometry import box
    from shapely.ops import transform as shapely_transform
    import geopandas as gpd
    import pyproj
    from datetime import datetime
    from dateutil.relativedelta import relativedelta
    from pathlib import Path

    parts = [p.strip() for p in input_str.split(',')]
    if len(parts) != 4:
        return "Invalid input format. Use: 'lake_id, mode, start, end'. Example: 'GL088561E28014N, monthly, 2024-06, 2025-01'"
    
    lake_id, mode, start_str, end_str = parts[0], parts[1].lower(), parts[2], parts[3]

    try:
        LAKES_PATH = Path(__file__).resolve().parent.parent.parent / "gis_data" / "stage2_dataset_15.gpkg"
        DETECTION_OUT_DIR = Path(__file__).resolve().parent.parent.parent / "agent_detection_outputs"
        
        # 1. Load Lake Geometry
        lakes_db = gpd.read_file(LAKES_PATH)
        target = lakes_db[lakes_db['GLAKE_ID'].str.upper() == lake_id.upper()]
        if target.empty: return f"Lake {lake_id} not found."
        
        target_wgs84 = target.to_crs("EPSG:4326")
        bbox = list(target_wgs84.total_bounds)
        bbox = [bbox[0]-0.01, bbox[1]-0.01, bbox[2]+0.01, bbox[3]+0.01]
        
        lake_geom = target_wgs84.geometry.iloc[0]

        # 2. Time Periods
        time_periods = []
        if mode == 'yearly':
            s_year, e_year = int(start_str), int(end_str)
            for y in range(s_year, e_year + 1):
                time_periods.append({"label": str(y), "start": f"{y}-07-01", "end": f"{y}-10-31"})
        elif mode == 'monthly':
            s_date = datetime.strptime(start_str, "%Y-%m")
            e_date = datetime.strptime(end_str, "%Y-%m")
            curr_date = s_date
            while curr_date <= e_date:
                next_month = curr_date + relativedelta(months=1)
                end_of_month = next_month - relativedelta(days=1)
                time_periods.append({
                    "label": curr_date.strftime("%Y-%m"),
                    "start": curr_date.strftime("%Y-%m-%d"),
                    "end": end_of_month.strftime("%Y-%m-%d")
                })
                curr_date = next_month
        else:
            return "Invalid mode. Use 'yearly' or 'monthly'."

        # 3. GEE Init & Model Load
        try: ee.Initialize()
        except: ee.Authenticate(); ee.Initialize()

        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model = smp.Unet(encoder_name="se_resnext50_32x4d", encoder_weights=None, in_channels=15, classes=1, activation=None)
        
        ckpt_path = Path(__file__).resolve().parent.parent.parent / "models" / "lake_segmentation" / "finetuned_model_best.pth"
        if not ckpt_path.exists(): return f"Model weights not found at {ckpt_path}"
        
        ckpt = torch.load(ckpt_path, map_location=device)
        model.load_state_dict(ckpt["state_dict"])
        model.to(device).eval()

        results = []
        out_dir = DETECTION_OUT_DIR / lake_id
        out_dir.mkdir(parents=True, exist_ok=True)

        for period in time_periods:
            date_str = period['label']
            aoi = ee.Geometry.BBox(*bbox)
            
            s2 = ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED").filterBounds(aoi).filterDate(period['start'], period['end']).median()
            s1 = ee.ImageCollection("COPERNICUS/S1_GRD").filterBounds(aoi).filterDate(period['start'], period['end']).select(['VV', 'VH']).median()
            dem = ee.ImageCollection("COPERNICUS/DEM/GLO30").filterBounds(aoi).select('DEM').mosaic()
            composite = ee.Image.cat([s2.select(['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B8A', 'B9', 'B11', 'B12']), s1, dem]).clip(aoi).toFloat()
            
            tif_path = out_dir / f"{date_str}_comp.tif"
            import contextlib, io as io2
            with contextlib.redirect_stdout(io2.StringIO()), contextlib.redirect_stderr(io2.StringIO()):
                geemap.download_ee_image(composite, str(tif_path), region=aoi, crs="EPSG:32645", scale=10)

            with rasterio.open(tif_path) as ds:
                arr = ds.read()
                transform = ds.transform
                pixel_area = abs(transform.a * transform.e) / 1e6
                
                t = torch.from_numpy(np.nan_to_num(arr)).float()
                
                S2_MEAN = torch.tensor([857.6, 1044.0, 1356.7, 1574.4, 1786.2, 2076.5, 2215.2, 2277.8, 2348.5, 2243.7, 2665.0, 2217.2]).view(12, 1, 1)
                S2_STD  = torch.tensor([626.3, 709.2, 748.7, 825.5, 773.5, 786.1, 810.8, 834.9, 833.6, 729.6, 875.7, 851.3]).view(12, 1, 1)
                S1_MEAN = torch.tensor([-9.25, -18.00]).view(2, 1, 1)
                S1_STD  = torch.tensor([5.90, 5.92]).view(2, 1, 1)
                DEM_MEAN = torch.tensor([4299.8]).view(1, 1, 1)
                DEM_STD  = torch.tensor([901.0]).view(1, 1, 1)
                
                t[0:12] = torch.clamp((t[0:12] - S2_MEAN) / S2_STD, -10, 10)
                t[12:14] = torch.clamp((t[12:14] - S1_MEAN) / S1_STD, -10, 10)
                t[14:15] = torch.clamp((t[14:15] - DEM_MEAN) / DEM_STD, -10, 10)
                
                with torch.no_grad():
                    prob_mask = predict_sliding_window(model, t, device=device)
                    
                binary_mask = prob_mask >= 0.8
                
                # Visual Overlay
                rgb = np.stack([arr[3], arr[2], arr[1]], axis=-1)
                rgb_img = np.zeros_like(rgb, dtype=np.uint8)
                for i in range(3):
                    channel = rgb[:, :, i]
                    valid = channel[np.isfinite(channel) & (channel > 0)]
                    if valid.size > 0:
                        lo, hi = np.percentile(valid, [2, 98])
                        if hi <= lo: hi = lo + 1.0
                        rgb_img[:, :, i] = (np.clip((channel - lo) / (hi - lo), 0, 1) * 255).astype(np.uint8)
                
                overlay_color = np.zeros((*binary_mask.shape, 3), dtype=np.uint8)
                overlay_color[binary_mask] = [0, 220, 255]
                overlay = (0.7 * rgb_img.astype(np.float32) + 0.3 * overlay_color.astype(np.float32)).astype(np.uint8)
                plt.imsave(str(out_dir / f"{date_str}_prediction.png"), overlay)
                
                labeled, num = label(binary_mask)
                counts = np.bincount(labeled.ravel())

                project = pyproj.Transformer.from_crs("EPSG:4326", ds.crs, always_xy=True).transform
                geom_proj = shapely_transform(project, lake_geom)
                zone = rasterize([(geom_proj, 1)], out_shape=binary_mask.shape, transform=transform, fill=0)
                
                intersect_ids = np.unique(labeled[zone == 1])
                intersect_ids = intersect_ids[intersect_ids > 0]
                area = counts[intersect_ids].sum() * pixel_area
                results.append({"date": date_str, "area_km2": float(area)})

        summary = [f"--- Satellite Lake Detection Report: {lake_id} ({mode.upper()}) ---"]
        area_str = " -> ".join([f"{r['date']}: {r['area_km2']:.3f}km2" for r in results])
        summary.append(f"Trend: {area_str}")
        summary.append(f"Files saved to: {out_dir.resolve()}")
        return "\n".join(summary)

    except Exception as e:
        import traceback
        return f"Detection Error: {str(e)}\n{traceback.format_exc()}"

def simulate_glof_flood_impact(lake_id: str) -> str:

    """
    Runs a GIS simulation to estimate GLOF impact.
    1. Calculates peak discharge using Huggel's empirical formula.
    2. Traces the flood zone 50km downstream along the river network.
    3. Identifies specific buildings at risk by fixing CRS projection issues.
    Input: The exact Lake ID.
    Returns: A text report of the estimated discharge and count of buildings at risk.
    """
    import geopandas as gpd
    from shapely.geometry import box
    
    print(f"Simulating flood impact for {lake_id}...")
    
    try:
        # 1. Load Lake Data
        lakes = gpd.read_file(LAKES_PATH)
        target_lake = lakes[lakes['GLAKE_ID'].str.upper() == lake_id.upper()]
        if target_lake.empty:
            return f"Lake {lake_id} not found in the spatial database."
        
        lake_geom = target_lake.geometry.iloc[0]
        metric_crs = lakes.crs
        
        # 2. Get Volume and Peak Discharge
        # Prioritize existing volume data
        if 'volume_m3' in target_lake.columns and not target_lake['volume_m3'].isna().iloc[0]:
            est_volume = target_lake['volume_m3'].iloc[0]
            source_note = " (from database)"
        else:
            # Fallback to empirical formula using correct area column name
            lake_area = target_lake['area_m2'].iloc[0] if 'area_m2' in target_lake.columns else 100000
            est_volume = 0.04 * (lake_area ** 1.2)
            source_note = " (estimated from area)"
            
        # Empirical Peak Discharge (Huggel et al., 2002 approximation)
        q_max = 0.0048 * (est_volume ** 0.896)
        
        # 3. Find Downstream Path (Improved Topological Tracing)
        rivers = gpd.read_file(RIVERS_PATH)
        if rivers.crs != metric_crs:
            rivers = rivers.to_crs(metric_crs)
            
        # Better Tracing Logic:
        # 1. Use KG to find the associated river if possible
        kg = KgStore(KG_STORE_DIR)
        link = kg.associated_river_for_lake(lake_id)
        start_river_id = None
        if link and link.get('river_id'):
            try:
                # Handle cases like "30002024.0" or "30002024"
                start_river_id = int(float(link['river_id']))
            except (ValueError, TypeError):
                pass
        
        # 2. If no KG link or ID mismatch, find the nearest river segment
        if start_river_id is None or start_river_id not in rivers['river_id'].values:
            # Spatial fallback: Find nearest segment
            distances = rivers.geometry.distance(lake_geom)
            nearest_idx = distances.idxmin()
            start_river_id = rivers.loc[nearest_idx, 'river_id']
            print(f"Using nearest river segment fallback: {start_river_id}")
        else:
            print(f"Using KG-linked river segment: {start_river_id}")

        # 3. Trace downstream using 'downstream_line_ids' topology
        def trace_downstream(df, start_id, max_dist=50000):
            path_ids = []
            curr_id = start_id
            total_dist = 0
            # Pre-filter for performance: create a lookup dictionary
            river_lookup = df.set_index('river_id')[['downstream_line_ids', 'geometry']].to_dict('index')
            
            while curr_id in river_lookup and total_dist < max_dist:
                if curr_id in path_ids: break # Cycle detection
                path_ids.append(curr_id)
                row = river_lookup[curr_id]
                total_dist += row['geometry'].length
                
                next_ids_str = str(row['downstream_line_ids'])
                if not next_ids_str or next_ids_str == 'None' or next_ids_str == '':
                    break
                try:
                    # Take first downstream branch (primary flow path)
                    curr_id = int(float(next_ids_str.split(',')[0]))
                except (ValueError, TypeError):
                    break
            return path_ids

        path_ids = trace_downstream(rivers, start_river_id)
        potential_path = rivers[rivers['river_id'].isin(path_ids)]
        
        if potential_path.empty:
            flood_zone = lake_geom.buffer(2000) 
            path_desc = "Radial 2km hazard zone (no rivers found nearby)."
        else:
            # Create a 1km hazard zone along connected rivers
            union_rivers = potential_path.union_all() if hasattr(potential_path, 'union_all') else potential_path.unary_union
            flood_zone = union_rivers.buffer(1000)
            path_desc = f"Downstream path along {len(potential_path)} topological river segments (1km hazard buffer)."
            
        # 4. Identify Buildings at Risk (CRITICAL CRS FIX)
        # Bbox for read_file MUST match the file's CRS (EPSG:4326)
        flood_zone_4326 = gpd.GeoSeries([flood_zone], crs=metric_crs).to_crs("EPSG:4326").iloc[0]
        bbox = flood_zone_4326.bounds
        
        print(f"Loading buildings in bbox: {bbox}")
        buildings = gpd.read_file(BUILDINGS_PATH, bbox=bbox)
        
        if buildings.empty:
            return f"--- GLOF IMPACT SIMULATION REPORT: {lake_id} ---\nEstimated Qmax: {q_max:.2f} m3/s\nNote: No buildings found in the mapped {path_desc}"
            
        if buildings.crs != metric_crs:
            buildings = buildings.to_crs(metric_crs)
            
        at_risk = buildings[buildings.geometry.intersects(flood_zone)]
        
        report = [
            f"--- GLOF IMPACT SIMULATION REPORT: {lake_id} ---",
            f"Estimated Peak Discharge (Qmax): {q_max:.2f} m3/s",
            f"Estimated Lake Volume: {est_volume:,.0f} m3",
            f"Hazard Path: {path_desc}",
            f"Total Buildings at Risk: {len(at_risk)} structure(s).",
        ]
        
        if not at_risk.empty:
            if 'type' in at_risk.columns:
                types = at_risk['type'].fillna('unknown').value_counts().to_dict()
                type_str = ", ".join([f"{count} {t}" for t, count in types.items()])
                report.append(f"Inundated Structures: {type_str}")
            
            # Distance to nearest building
            min_dist = at_risk.geometry.distance(lake_geom).min()
            report.append(f"Nearest structure is {min_dist/1000:.2f} km downstream.")
        
        return "\n".join(report)

    except Exception as e:
        import traceback
        return f"Simulation Error: {str(e)}\n{traceback.format_exc()}"

def query_knowledge_graph(query: str) -> str:
    """
    Use this tool to search the semantic Knowledge Graph for definitions, concepts, triggers, risks, and thresholds.
    Use this when the user asks about "thresholds", "causes", "hazard index", "weather variables", or ontological classes.
    Input: The search query string.
    """
    try:
        kg = KgStore(KG_STORE_DIR)
        context = kg.context_for_question(query)
        if not context:
            return "No relevant information found in the Knowledge Graph for this query."
        return context
    except Exception as e:
        return f"KG Error: {str(e)}"

# Dictionary mapping tool names to functions for the Agent loop
TOOLS = {
    "get_dataset_info": get_dataset_info,
    "execute_python_code": execute_python_code,
    "query_lakes_by_subcatchment": query_lakes_by_subcatchment,
    "query_lake_properties_kg": query_lake_properties_kg,
    "query_downstream_rivers_kg": query_downstream_rivers_kg,
    "query_knowledge_graph": query_knowledge_graph,
    "search_scientific_papers": search_scientific_papers,
    "get_glof_risk_forecast": get_glof_risk_forecast,
    "get_regional_glof_forecast": get_regional_glof_forecast,
    "simulate_glof_flood_impact": simulate_glof_flood_impact,
    "detect_lakes_and_calculate_area": detect_lakes_and_calculate_area
}

def get_tool_descriptions() -> str:
    """Helper to inject tool descriptions into the prompt."""
    desc = []
    for name, func in TOOLS.items():
        desc.append(f"Tool Name: {name}\nDescription: {func.__doc__.strip()}\n")
    return "\n---\n".join(desc)
