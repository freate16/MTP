import os
import sys
import torch # CRITICAL: Import torch first to prevent WinError 1114 on Windows
import numpy as np
import pandas as pd
import datetime as dt
import geopandas as gpd
import joblib
import duckdb
import shap
import logging

# Ensure project root is in sys.path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# ==========================================
# Paths
# ==========================================
STATIC_DATA_PATH = os.path.join(PROJECT_ROOT, "gis_data", "stage2_dataset_15.gpkg")
XGB_MODEL_PATH = os.path.join(PROJECT_ROOT, "models", "xgb_best_results", "best_f2_xgb_model.joblib")

# ==========================================
# Unified Data Fetch & Imputation
# ==========================================
def impute_raw_window(raw_window: np.ndarray) -> np.ndarray:
    """
    Scans the (T, N, F) window fetched by Earth Engine. The last 5 days are usually
    NaN due to the lag. We fill them using the rolling mean of the 7 days prior.
    """
    T, N, F = raw_window.shape
    imputed_window = raw_window.copy()

    for n in range(N):
        for f in range(F):
            series = imputed_window[:, n, f]
            valid_idx = np.where(~np.isnan(series))[0]
            if len(valid_idx) == 0:
                imputed_window[:, n, f] = 0.0
                continue

            last_valid = valid_idx[-1]
            if last_valid < T - 1:
                start_hist = max(0, last_valid - 6)
                hist_mean = np.nanmean(series[start_hist:last_valid+1])
                imputed_window[last_valid+1:, n, f] = hist_mean

    return imputed_window

def fetch_unified_weather(glake_id: str):
    """
    1. Isolates the GNO node and its k-hop subgraph.
    2. Fetches 90-day ERA5 data (required for XGBoost).
    3. Imputes the last 5 days lag using rolling means.
    4. Extracts the Central Node's data as a DataFrame for XGBoost.
    5. Returns the full tensor array for GNN (sliced to 60 days later), DataFrame for XGBoost, and context.
    """
    import torch
    from gnn.inference import (
        initialize_earth_engine, load_model_and_graph, load_graph_nodes,
        build_k_hop_subgraph, fetch_era5_land_daily_for_nodes,
        NODE_HOPS, FEATURE_COLS
    )

    print("\n[1/3] 🌍 Initializing Google Earth Engine for Live ERA5 Retrieval...")
    initialize_earth_engine()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    model, edge_index = load_model_and_graph(device)
    nodes_gdf = load_graph_nodes()

    lake_row = nodes_gdf[nodes_gdf["GLAKE_ID"] == glake_id]
    if lake_row.empty:
        raise ValueError(f"No GNN node mapping found for {glake_id}")

    center_node = int(lake_row["node_index"].iloc[0])
    node_ids, sub_edge_index, center_local = build_k_hop_subgraph(edge_index, center_node, hops=NODE_HOPS)      
    sub_nodes = nodes_gdf.set_index("node_index").loc[node_ids].reset_index()

    target_date = dt.date.today()
    # We explicitly fetch 90 days for XGBoost, even though GNN only needs 60.
    raw_window, all_dates = fetch_era5_land_daily_for_nodes(sub_nodes, target_date, history_days=90)

    print("      >> Imputing recent 5-day lag with 7-day rolling mean...")
    imputed_window = impute_raw_window(raw_window)

    # Extract only the central lake's sequence to a pandas dataframe for XGBoost
    center_ts = imputed_window[:, center_local, :]
    df_records = []
    # XGBoost needs the first 90 days (history)
    for t_idx in range(90):
        row_dict = {"GLAKE_ID": glake_id, "date": all_dates[t_idx]}
        for f_idx, col_name in enumerate(FEATURE_COLS):
            row_dict[col_name] = center_ts[t_idx, f_idx]
        df_records.append(row_dict)

    weather_df = pd.DataFrame(df_records)

    return imputed_window, weather_df, model, edge_index, sub_edge_index, center_local, device, all_dates       

# ==========================================
# XGBoost Pipeline
# ==========================================
def run_xgboost_inference(glake_id: str, weather_seq_df: pd.DataFrame):
    print(f"\n[2/3] 🌳 Running XGBoost GLOF Context Model for {glake_id}...")

    temp_csv = os.path.join(SCRIPT_DIR, f"temp_{glake_id}_weather.csv")
    weather_seq_df.to_csv(temp_csv, index=False)

    query = f"""
    WITH era5 AS (
        SELECT
            GLAKE_ID,
            CAST("date" AS DATE) AS obs_date,
            total_precipitation_sum,
            snowmelt_sum,
            surface_runoff_sum,
            sub_surface_runoff_sum,
            snowfall_sum,
            temperature_2m,
            dewpoint_temperature_2m,
            snow_depth_water_equivalent,
            surface_pressure
        FROM read_csv_auto('{temp_csv}')
    ),
    lake_targets AS (
        SELECT GLAKE_ID, MAX(obs_date) as event_date
        FROM era5 GROUP BY GLAKE_ID
    )
    SELECT
        t.GLAKE_ID,

        -- 3d
        SUM(CASE WHEN e.obs_date BETWEEN t.event_date - INTERVAL 2 DAYS AND t.event_date THEN e.total_precipitation_sum END) AS total_precipitation_sum_3d,
        SUM(CASE WHEN e.obs_date BETWEEN t.event_date - INTERVAL 2 DAYS AND t.event_date THEN e.snowmelt_sum END) AS snowmelt_sum_3d,
        SUM(CASE WHEN e.obs_date BETWEEN t.event_date - INTERVAL 2 DAYS AND t.event_date THEN e.surface_runoff_sum END) AS surface_runoff_sum_3d,

        -- 7d
        SUM(CASE WHEN e.obs_date BETWEEN t.event_date - INTERVAL 6 DAYS AND t.event_date THEN e.total_precipitation_sum END) AS total_precipitation_sum_7d,
        SUM(CASE WHEN e.obs_date BETWEEN t.event_date - INTERVAL 6 DAYS AND t.event_date THEN e.snowmelt_sum END) AS snowmelt_sum_7d,
        SUM(CASE WHEN e.obs_date BETWEEN t.event_date - INTERVAL 6 DAYS AND t.event_date THEN e.surface_runoff_sum END) AS surface_runoff_sum_7d,
        SUM(CASE WHEN e.obs_date BETWEEN t.event_date - INTERVAL 6 DAYS AND t.event_date THEN e.sub_surface_runoff_sum END) AS sub_surface_runoff_sum_7d,
        SUM(CASE WHEN e.obs_date BETWEEN t.event_date - INTERVAL 6 DAYS AND t.event_date THEN e.snowfall_sum END) AS snowfall_sum_7d,
        AVG(CASE WHEN e.obs_date BETWEEN t.event_date - INTERVAL 6 DAYS AND t.event_date THEN e.temperature_2m END) AS temperature_2m_mean_7d,
        AVG(CASE WHEN e.obs_date BETWEEN t.event_date - INTERVAL 6 DAYS AND t.event_date THEN e.dewpoint_temperature_2m END) AS dewpoint_temperature_2m_mean_7d,
        AVG(CASE WHEN e.obs_date BETWEEN t.event_date - INTERVAL 6 DAYS AND t.event_date THEN e.snow_depth_water_equivalent END) AS snow_depth_water_equivalent_mean_7d,
        AVG(CASE WHEN e.obs_date BETWEEN t.event_date - INTERVAL 6 DAYS AND t.event_date THEN e.surface_pressure END) AS surface_pressure_mean_7d,

        -- 30d
        SUM(CASE WHEN e.obs_date BETWEEN t.event_date - INTERVAL 29 DAYS AND t.event_date THEN e.total_precipitation_sum END) AS total_precipitation_sum_30d,
        SUM(CASE WHEN e.obs_date BETWEEN t.event_date - INTERVAL 29 DAYS AND t.event_date THEN e.snowmelt_sum END) AS snowmelt_sum_30d,
        SUM(CASE WHEN e.obs_date BETWEEN t.event_date - INTERVAL 29 DAYS AND t.event_date THEN e.surface_runoff_sum END) AS surface_runoff_sum_30d,
        SUM(CASE WHEN e.obs_date BETWEEN t.event_date - INTERVAL 29 DAYS AND t.event_date THEN e.sub_surface_runoff_sum END) AS sub_surface_runoff_sum_30d,
        SUM(CASE WHEN e.obs_date BETWEEN t.event_date - INTERVAL 29 DAYS AND t.event_date THEN e.snowfall_sum END) AS snowfall_sum_30d,
        AVG(CASE WHEN e.obs_date BETWEEN t.event_date - INTERVAL 29 DAYS AND t.event_date THEN e.temperature_2m END) AS temperature_2m_mean_30d,
        AVG(CASE WHEN e.obs_date BETWEEN t.event_date - INTERVAL 29 DAYS AND t.event_date THEN e.snow_depth_water_equivalent END) AS snow_depth_water_equivalent_mean_30d,

        -- 90d
        SUM(CASE WHEN e.obs_date BETWEEN t.event_date - INTERVAL 89 DAYS AND t.event_date THEN e.total_precipitation_sum END) AS total_precipitation_sum_90d,
        SUM(CASE WHEN e.obs_date BETWEEN t.event_date - INTERVAL 89 DAYS AND t.event_date THEN e.snowmelt_sum END) AS snowmelt_sum_90d,
        SUM(CASE WHEN e.obs_date BETWEEN t.event_date - INTERVAL 89 DAYS AND t.event_date THEN e.sub_surface_runoff_sum END) AS sub_surface_runoff_sum_90d,
        SUM(CASE WHEN e.obs_date BETWEEN t.event_date - INTERVAL 89 DAYS AND t.event_date THEN e.snowfall_sum END) AS snowfall_sum_90d,
        AVG(CASE WHEN e.obs_date BETWEEN t.event_date - INTERVAL 89 DAYS AND t.event_date THEN e.temperature_2m END) AS temperature_2m_mean_90d,
        AVG(CASE WHEN e.obs_date BETWEEN t.event_date - INTERVAL 89 DAYS AND t.event_date THEN e.snow_depth_water_equivalent END) AS snow_depth_water_equivalent_mean_90d
    FROM lake_targets t
    JOIN era5 e ON t.GLAKE_ID = e.GLAKE_ID
    GROUP BY t.GLAKE_ID
    """
    con = duckdb.connect()
    agg_weather_df = con.execute(query).df()
    con.close()
    if os.path.exists(temp_csv): os.remove(temp_csv)

    static_df = pd.DataFrame(gpd.read_file(STATIC_DATA_PATH).drop(columns="geometry"))
    lake_static = static_df[static_df['GLAKE_ID'].str.upper() == glake_id.upper()].copy()
    if lake_static.empty:
        return {"error": f"Static data for {glake_id} not found."}

    xgb_input = pd.merge(lake_static, agg_weather_df, on="GLAKE_ID", how="inner")

    try:
        xgb_input['precip_anomaly_7d_90d'] = xgb_input['total_precipitation_sum_7d'] / (xgb_input['total_precipitation_sum_90d'] / 90 * 7 + 1e-5)
        xgb_input['snowmelt_anomaly_7d_30d'] = xgb_input['snowmelt_sum_7d'] / (xgb_input['snowmelt_sum_30d'] / 30 * 7 + 1e-5)
        xgb_input['temp_spike_7d_over_30d'] = xgb_input['temperature_2m_mean_7d'] - xgb_input['temperature_2m_mean_30d']
    except Exception as e:
        pass

    model = joblib.load(XGB_MODEL_PATH)
    features_used = model.feature_names_in_

    for col in features_used:
        if col not in xgb_input.columns:
            xgb_input[col] = 0.0

    X = xgb_input[features_used]
    prob = float(model.predict_proba(X)[0, 1])

    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X)

    feature_impacts = list(zip(features_used, shap_values[0]))
    positive_drivers = sorted([f for f in feature_impacts if f[1] > 0], key=lambda x: x[1], reverse=True)[:3]   

    return {
        "probability": prob,
        "top_drivers": [f"{feat}: {val:.3f}" for feat, val in positive_drivers],
        "driver_names": [f[0] for f in positive_drivers]
    }


def run_xgboost_batch(weather_seq_df: pd.DataFrame):
    """Run XGBoost model for multiple GLAKE_IDs at once using DuckDB aggregations."""
    print("\n[2/3] 🌳 Running batched XGBoost for multiple lakes...")
    temp_csv = os.path.join(SCRIPT_DIR, f"temp_batch_weather.csv")
    weather_seq_df.to_csv(temp_csv, index=False)

    query = f"""
    WITH era5 AS (
        SELECT
            GLAKE_ID,
            CAST("date" AS DATE) AS obs_date,
            total_precipitation_sum,
            snowmelt_sum,
            surface_runoff_sum,
            sub_surface_runoff_sum,
            snowfall_sum,
            temperature_2m,
            dewpoint_temperature_2m,
            snow_depth_water_equivalent,
            surface_pressure
        FROM read_csv_auto('{temp_csv}')
    ),
    lake_targets AS (
        SELECT GLAKE_ID, MAX(obs_date) as event_date
        FROM era5 GROUP BY GLAKE_ID
    )
    SELECT
        t.GLAKE_ID,
        -- aggregations identical to single-run
        SUM(CASE WHEN e.obs_date BETWEEN t.event_date - INTERVAL 2 DAYS AND t.event_date THEN e.total_precipitation_sum END) AS total_precipitation_sum_3d,
        SUM(CASE WHEN e.obs_date BETWEEN t.event_date - INTERVAL 2 DAYS AND t.event_date THEN e.snowmelt_sum END) AS snowmelt_sum_3d,
        SUM(CASE WHEN e.obs_date BETWEEN t.event_date - INTERVAL 2 DAYS AND t.event_date THEN e.surface_runoff_sum END) AS surface_runoff_sum_3d,
        SUM(CASE WHEN e.obs_date BETWEEN t.event_date - INTERVAL 6 DAYS AND t.event_date THEN e.total_precipitation_sum END) AS total_precipitation_sum_7d,
        SUM(CASE WHEN e.obs_date BETWEEN t.event_date - INTERVAL 6 DAYS AND t.event_date THEN e.snowmelt_sum END) AS snowmelt_sum_7d,
        SUM(CASE WHEN e.obs_date BETWEEN t.event_date - INTERVAL 6 DAYS AND t.event_date THEN e.surface_runoff_sum END) AS surface_runoff_sum_7d,
        SUM(CASE WHEN e.obs_date BETWEEN t.event_date - INTERVAL 6 DAYS AND t.event_date THEN e.sub_surface_runoff_sum END) AS sub_surface_runoff_sum_7d,
        SUM(CASE WHEN e.obs_date BETWEEN t.event_date - INTERVAL 6 DAYS AND t.event_date THEN e.snowfall_sum END) AS snowfall_sum_7d,
        AVG(CASE WHEN e.obs_date BETWEEN t.event_date - INTERVAL 6 DAYS AND t.event_date THEN e.temperature_2m END) AS temperature_2m_mean_7d,
        AVG(CASE WHEN e.obs_date BETWEEN t.event_date - INTERVAL 6 DAYS AND t.event_date THEN e.dewpoint_temperature_2m END) AS dewpoint_temperature_2m_mean_7d,
        AVG(CASE WHEN e.obs_date BETWEEN t.event_date - INTERVAL 6 DAYS AND t.event_date THEN e.snow_depth_water_equivalent END) AS snow_depth_water_equivalent_mean_7d,
        AVG(CASE WHEN e.obs_date BETWEEN t.event_date - INTERVAL 6 DAYS AND t.event_date THEN e.surface_pressure END) AS surface_pressure_mean_7d,
        SUM(CASE WHEN e.obs_date BETWEEN t.event_date - INTERVAL 29 DAYS AND t.event_date THEN e.total_precipitation_sum END) AS total_precipitation_sum_30d,
        SUM(CASE WHEN e.obs_date BETWEEN t.event_date - INTERVAL 29 DAYS AND t.event_date THEN e.snowmelt_sum END) AS snowmelt_sum_30d,
        SUM(CASE WHEN e.obs_date BETWEEN t.event_date - INTERVAL 29 DAYS AND t.event_date THEN e.surface_runoff_sum END) AS surface_runoff_sum_30d,
        SUM(CASE WHEN e.obs_date BETWEEN t.event_date - INTERVAL 29 DAYS AND t.event_date THEN e.sub_surface_runoff_sum END) AS sub_surface_runoff_sum_30d,
        SUM(CASE WHEN e.obs_date BETWEEN t.event_date - INTERVAL 29 DAYS AND t.event_date THEN e.snowfall_sum END) AS snowfall_sum_30d,
        AVG(CASE WHEN e.obs_date BETWEEN t.event_date - INTERVAL 29 DAYS AND t.event_date THEN e.temperature_2m END) AS temperature_2m_mean_30d,
        AVG(CASE WHEN e.obs_date BETWEEN t.event_date - INTERVAL 29 DAYS AND t.event_date THEN e.snow_depth_water_equivalent END) AS snow_depth_water_equivalent_mean_30d,
        SUM(CASE WHEN e.obs_date BETWEEN t.event_date - INTERVAL 89 DAYS AND t.event_date THEN e.total_precipitation_sum END) AS total_precipitation_sum_90d,
        SUM(CASE WHEN e.obs_date BETWEEN t.event_date - INTERVAL 89 DAYS AND t.event_date THEN e.snowmelt_sum END) AS snowmelt_sum_90d,
        SUM(CASE WHEN e.obs_date BETWEEN t.event_date - INTERVAL 89 DAYS AND t.event_date THEN e.sub_surface_runoff_sum END) AS sub_surface_runoff_sum_90d,
        SUM(CASE WHEN e.obs_date BETWEEN t.event_date - INTERVAL 89 DAYS AND t.event_date THEN e.snowfall_sum END) AS snowfall_sum_90d,
        AVG(CASE WHEN e.obs_date BETWEEN t.event_date - INTERVAL 89 DAYS AND t.event_date THEN e.temperature_2m END) AS temperature_2m_mean_90d,
        AVG(CASE WHEN e.obs_date BETWEEN t.event_date - INTERVAL 89 DAYS AND t.event_date THEN e.snow_depth_water_equivalent END) AS snow_depth_water_equivalent_mean_90d
    FROM lake_targets t
    JOIN era5 e ON t.GLAKE_ID = e.GLAKE_ID
    GROUP BY t.GLAKE_ID
    """
    con = duckdb.connect()
    try:
        agg_weather_df = con.execute(query).df()
    finally:
        con.close()
    if os.path.exists(temp_csv):
        os.remove(temp_csv)

    static_df = pd.DataFrame(gpd.read_file(STATIC_DATA_PATH).drop(columns="geometry"))
    xgb_input = pd.merge(static_df, agg_weather_df, on="GLAKE_ID", how="inner")
    if xgb_input.empty:
        return {}

    try:
        xgb_input['precip_anomaly_7d_90d'] = xgb_input['total_precipitation_sum_7d'] / (xgb_input['total_precipitation_sum_90d'] / 90 * 7 + 1e-5)
        xgb_input['snowmelt_anomaly_7d_30d'] = xgb_input['snowmelt_sum_7d'] / (xgb_input['snowmelt_sum_30d'] / 30 * 7 + 1e-5)
        xgb_input['temp_spike_7d_over_30d'] = xgb_input['temperature_2m_mean_7d'] - xgb_input['temperature_2m_mean_30d']
    except Exception:
        pass

    model = joblib.load(XGB_MODEL_PATH)
    features_used = model.feature_names_in_

    for col in features_used:
        if col not in xgb_input.columns:
            xgb_input[col] = 0.0

    X = xgb_input[features_used]
    probs = model.predict_proba(X)[:, 1]

    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X)

    results = {}
    for i, gid in enumerate(xgb_input['GLAKE_ID'].values):
        prob = float(probs[i])
        # shap_values may be list or ndarray depending on SHAP version
        try:
            sv = shap_values[i]
        except Exception:
            sv = shap_values[1][i]
        feature_impacts = list(zip(features_used, sv))
        positive_drivers = sorted([f for f in feature_impacts if f[1] > 0], key=lambda x: x[1], reverse=True)[:3]
        results[gid] = {
            "probability": prob,
            "top_drivers": [f"{feat}: {val:.3f}" for feat, val in positive_drivers],
            "driver_names": [f[0] for f in positive_drivers]
        }

    return results

# ==========================================
# GNN Pipeline (Dynamic Thresholds)
# ==========================================
def run_gnn_inference(imputed_window, model, sub_edge_index, center_local, device):
    import torch
    from gnn.inference import build_model_input, TARGET_COLS, HISTORY_DAYS

    logging.getLogger(__name__).debug("Running GNN Physical Forecast for center_local=%s on device=%s", center_local, device)

    # 1. Forward pass
    # imputed_window is 93 days (90 hist + 3 forecast placeholder).
    # GNN expects 60 days history. So we take the LAST 60 days of history.
    # HISTORY_DAYS is 60 (imported from gnn.inference).
    
    # Slice to take the last 60 days of history + the forecast days
    start_slice = 90 - HISTORY_DAYS # 90 - 60 = 30
    gnn_input_window = imputed_window[start_slice:, :, :]
    
    x_tensor, _ = build_model_input(gnn_input_window)
    x_tensor = x_tensor.to(device)
    sub_edge_index = sub_edge_index.to(device)
    with torch.no_grad():
        pred = model(x_tensor, sub_edge_index).squeeze(0).cpu().numpy()

    # FIX: Clip negative predictions to 0.0 for physical consistency
    pred = np.maximum(pred, 0.0)

    center_pred = pred[center_local]
    # 2. Dynamic Threshold Logic (use surface runoff historical stats)
    runoff_idx = TARGET_COLS.index("surface_runoff_sum")
    from gnn.inference import FEATURE_COLS
    feature_runoff_idx = FEATURE_COLS.index("surface_runoff_sum")

    # Use the same sliced window for historical stats
    historical_runoff = gnn_input_window[:HISTORY_DAYS, center_local, feature_runoff_idx]
    hist_mean = np.mean(historical_runoff)
    hist_std = np.std(historical_runoff) + 1e-8
    dynamic_threshold = hist_mean + (3.0 * hist_std)

    # 3. Assess the Forecasts: compute mean across forecast steps for each target
    forecasts = {}
    for i, target_name in enumerate(TARGET_COLS):
        # center_pred shape: (out_steps, out_vars)
        try:
            target_vals = center_pred[:, i]
        except Exception:
            target_vals = center_pred[:, i] if center_pred.ndim >= 2 else np.array([center_pred[i]])
        forecasts[f"{target_name}_mean"] = float(np.mean(target_vals))
        forecasts[f"{target_name}_max"] = float(np.max(target_vals))

    forecasted_runoff_mean = forecasts.get("surface_runoff_sum_mean", 0.0)
    risk_level = "HIGH" if forecasted_runoff_mean > dynamic_threshold else "LOW"

    out = {
        "risk_level": risk_level,
        "dynamic_threshold": dynamic_threshold,
        "historical_mean": hist_mean,
        "historical_std": hist_std,
    }
    out.update(forecasts)
    return out

# ==========================================
# Unified Runner
# ==========================================
def explain_glof_prediction(glake_id: str):
    """
    Executes BOTH models sequentially and returns natural language evidence.
    """
    try:
        # Step 1: Shared Live Fetch via GEE
        (imputed_window, weather_seq_df,
         gnn_model, edge_index, sub_edge_index,
         center_local, device, all_dates) = fetch_unified_weather(glake_id)

        # Step 2: XGBoost
        xgb_res = run_xgboost_inference(glake_id, weather_seq_df)
        if "error" in xgb_res:
            return f"Error running models: {xgb_res.get('error')}"

        # Step 3: GNN
        print("\n[3/3] 🌀 Running GNN Physical Forecast Model...", flush=True)
        gnn_res = run_gnn_inference(imputed_window, gnn_model, sub_edge_index, center_local, device)

    except Exception as e:
        import traceback
        traceback.print_exc()
        return f"Error running dual inference models for {glake_id}: {str(e)}"

    prob_pct = xgb_res['probability'] * 100
    top_drivers = ", ".join(xgb_res.get("driver_names", []))

    risk = gnn_res.get('risk_level', "UNKNOWN")
    dyn_threshold = gnn_res.get('dynamic_threshold', 0)
    surf_mean = gnn_res.get('surface_runoff_sum_mean')
    subsurf_mean = gnn_res.get('sub_surface_runoff_sum_mean')
    snowmelt_mean = gnn_res.get('snowmelt_sum_mean')

    explanation = (
        f"XGBoost Prediction: {prob_pct:.1f}% probability of GLOF. This is the primary signal.\n"
        f"Primary Driving Features (SHAP): {top_drivers}\n\n"
        f"GNN Physical Summary: the model predicts surface runoff {surf_mean:.5f} m, sub-surface runoff {subsurf_mean:.5f} m, and snowmelt {snowmelt_mean:.5f} m over the next 3 days. "
        f"Overall GNN trigger: {risk} (threshold={dyn_threshold:.5f}, based on 3x the 60-day runoff std).\n\n"  
        f"This lake looks low-risk from the XGBoost score, but the GNN suggests stronger runoff activity, so it is worth watching rather than treating as an immediate alarm. If both models are high, that would be a stronger warning sign."
    )

    return explanation

def explain_regional_glof(lat: float, lon: float, buffer_km: float):
    """
    Finds all lakes within a radius of (lat, lon) and runs the dual-inference pipeline.
    """
    from shapely.geometry import Point
    # Import GNN helpers
    from gnn.inference import (
        initialize_earth_engine,
        fetch_era5_land_daily_for_nodes,
        load_model_and_graph,
        load_graph_nodes,
        build_k_hop_subgraph,
        NODE_HOPS,
        FEATURE_COLS,
        HISTORY_DAYS,
    )

    # Load full static geodata and graph node mapping
    if not os.path.exists(STATIC_DATA_PATH):
        return "Error: Lake geometry database not found."

    lakes_gdf = gpd.read_file(STATIC_DATA_PATH)
    metric_crs = lakes_gdf.crs

    pt = Point(lon, lat)
    pt_gdf = gpd.GeoDataFrame(geometry=[pt], crs="EPSG:4326").to_crs(metric_crs)
    pt_metric = pt_gdf.geometry.iloc[0]

    buffered_area = pt_metric.buffer(buffer_km * 1000.0)
    regional_lakes = lakes_gdf[lakes_gdf.geometry.intersects(buffered_area)]

    if regional_lakes.empty:
        return f"No lakes found within {buffer_km}km of {lat}, {lon}."

    regional_lakes = regional_lakes.reset_index(drop=True)
    max_lakes = 20
    if len(regional_lakes) > max_lakes:
        regional_lakes = regional_lakes.head(max_lakes)

    nodes_all = load_graph_nodes()
    import torch
    model_tmp, edge_index = load_model_and_graph(torch.device('cpu'))

    candidate_nodes = nodes_all[nodes_all['GLAKE_ID'].isin(regional_lakes['GLAKE_ID'])].reset_index(drop=True)  
    if candidate_nodes.empty:
        return f"No mapped graph nodes for lakes within {buffer_km}km of {lat}, {lon}."

    union_node_ids = set()
    for node_idx in candidate_nodes['node_index'].astype(int).values:
        node_ids, _, _ = build_k_hop_subgraph(edge_index, int(node_idx), hops=NODE_HOPS)
        union_node_ids.update(node_ids)

    regional_nodes = nodes_all[nodes_all['node_index'].isin(sorted(union_node_ids))].reset_index(drop=True)     
    if regional_nodes.empty:
        return f"No mapped graph nodes for lakes within {buffer_km}km of {lat}, {lon}."

    print("\n[1/3] 🌍 Initializing Google Earth Engine for Live ERA5 Retrieval...", flush=True)
    initialize_earth_engine()
    target_date = dt.date.today()
    # Fetch 90 days for XGBoost compatibility
    raw_window, all_dates = fetch_era5_land_daily_for_nodes(regional_nodes, target_date, history_days=90)
    imputed_window = impute_raw_window(raw_window)

    # Build weather dataframe for XGBoost batch (first 90 days history only)
    records = []
    for local_idx in range(imputed_window.shape[1]):
        gid = regional_nodes.iloc[local_idx]['GLAKE_ID']
        for t_idx in range(90):
            row = {"GLAKE_ID": gid, "date": all_dates[t_idx]}
            for f_idx, col in enumerate(FEATURE_COLS):
                row[col] = float(imputed_window[t_idx, local_idx, f_idx]) if not np.isnan(imputed_window[t_idx, local_idx, f_idx]) else None
            records.append(row)

    weather_df = pd.DataFrame.from_records(records)

    print("\n[2/3] 🌳 Running batched XGBoost for multiple lakes...", flush=True)
    xgb_results = run_xgboost_batch(weather_df)

    import torch
    model, edge_index = load_model_and_graph(torch.device('cpu'))

    per_lake_results = []
    node_index_to_local = {int(r['node_index']): i for i, r in regional_nodes.iterrows()}
    print("\n[3/3] 🌀 Running GNN Physical Forecast Model...", flush=True)
    for local_idx, node_row in regional_nodes.iterrows():
        glake_id = node_row['GLAKE_ID']
        xres = xgb_results.get(glake_id)
        if xres:
            prob_pct = xres['probability'] * 100
            xgb_text = f"XGBoost Prediction: {prob_pct:.1f}% probability of GLOF."
        else:
            xgb_text = "XGBoost Prediction: not available for this lake."

        center_node = int(node_row['node_index'])
        node_ids, sub_edge_index, center_local = build_k_hop_subgraph(edge_index, center_node, hops=NODE_HOPS)  

        if all(n in node_index_to_local for n in node_ids):
            positions = [node_index_to_local[n] for n in node_ids]
            sub_window = imputed_window[:, positions, :]
            gnn_res = run_gnn_inference(sub_window, model, sub_edge_index, center_local, torch.device('cpu'))   
        else:
            try:
                (sub_imputed, _, fetched_model, _, sub_edge_index, center_local, device, _) = fetch_unified_weather(glake_id)
                gnn_res = run_gnn_inference(sub_imputed, fetched_model, sub_edge_index, center_local, device)   
            except Exception as e:
                gnn_res = {"error": str(e)}

        if not isinstance(gnn_res, dict) or 'error' in gnn_res:
            err = gnn_res.get('error') if isinstance(gnn_res, dict) else str(gnn_res)
            gnn_text = f"GNN Prediction: error - {err}"
        else:
            surf_mean = gnn_res.get('surface_runoff_sum_mean')
            risk = gnn_res.get('risk_level', 'UNKNOWN')
            if surf_mean is None:
                gnn_text = f"GNN summary: overall trigger {risk}."
            else:
                subsurf_mean = gnn_res.get('sub_surface_runoff_sum_mean')
                snowmelt_mean = gnn_res.get('snowmelt_sum_mean')
                gnn_text = (
                    f"GNN summary: surface runoff {surf_mean:.5f} m, sub-surface runoff {subsurf_mean:.5f} m, " 
                    f"snowmelt {snowmelt_mean:.5f} m; overall trigger {risk}."
                )

        per_lake_results.append({"GLAKE_ID": glake_id, "xgb": xres, "gnn": gnn_res, "xgb_text": xgb_text, "gnn_text": gnn_text})

    summary_lines = ["XGB SUMMARY"]
    ranked_results = sorted(
        per_lake_results,
        key=lambda item: item['xgb']['probability'] if item.get('xgb') else -1.0,
        reverse=True,
    )
    max_reported = min(8, len(ranked_results))
    for item in ranked_results[:max_reported]:
        gid = item['GLAKE_ID']
        prob = item['xgb']['probability'] * 100 if item['xgb'] else None
        if prob is not None:
            line = f"- {gid}: {prob:.1f}%"
        else:
            line = f"- {gid}: N/A"
        summary_lines.append(line)

    if len(ranked_results) > max_reported:
        summary_lines.append(f"- ... {len(ranked_results) - max_reported} more lakes omitted for brevity")      

    gnn_high = sum(1 for item in per_lake_results if item.get('gnn', {}).get('risk_level') == 'HIGH')
    gnn_low = sum(1 for item in per_lake_results if item.get('gnn', {}).get('risk_level') == 'LOW')
    valid_runoffs = [item['gnn']['surface_runoff_sum_mean'] for item in per_lake_results if item.get('gnn') and 'surface_runoff_sum_mean' in item['gnn'] and item['gnn']['surface_runoff_sum_mean'] is not None]
    gnn_summary_lines = ["GNN SUMMARY"]
    if valid_runoffs:
        subsurf_vals = [item['gnn'].get('sub_surface_runoff_sum_mean') for item in per_lake_results if item.get('gnn') and 'sub_surface_runoff_sum_mean' in item['gnn']]
        snowmelt_vals = [item['gnn'].get('snowmelt_sum_mean') for item in per_lake_results if item.get('gnn') and 'snowmelt_sum_mean' in item['gnn']]
        gnn_summary_lines.append(f"- HIGH: {gnn_high}, LOW: {gnn_low}")
        gnn_summary_lines.append(f"- Surface runoff (avg): {float(np.mean(valid_runoffs)):.5f}, max: {float(np.max(valid_runoffs)):.5f}")
        if subsurf_vals:
            gnn_summary_lines.append(f"- Sub-surface runoff (avg): {float(np.mean(subsurf_vals)):.5f}")
        if snowmelt_vals:
            gnn_summary_lines.append(f"- Snowmelt (avg): {float(np.mean(snowmelt_vals)):.5f}")
        gnn_summary_lines.append("")
        gnn_summary_lines.append("Summary: the GNN predicts 3-day surface runoff, sub-surface runoff, and snowmelt. 'HIGH' means the surface runoff is above a 3x-standard-deviation threshold from the 60-day history; use this as a supporting signal after XGBoost.")
    else:
        gnn_summary_lines.append("- GNN results unavailable.")

    return "\n".join(summary_lines) + "\n\n" + "\n".join(gnn_summary_lines)


def explain_top_glof_lakes(limit: int = 5):
    """Run the dual pipeline for all lakes and return the top-N by XGBoost probability."""
    from gnn.inference import (
        initialize_earth_engine,
        fetch_era5_land_daily_for_nodes,
        load_model_and_graph,
        load_graph_nodes,
        build_k_hop_subgraph,
        NODE_HOPS,
        FEATURE_COLS,
        HISTORY_DAYS,
    )

    if not os.path.exists(STATIC_DATA_PATH):
        return "Error: Lake geometry database not found."

    nodes_all = load_graph_nodes()
    if nodes_all.empty:
        return "Error: No graph nodes available for lake ranking."

    print("\n[1/3] 🌍 Initializing Google Earth Engine for Live ERA5 Retrieval...", flush=True)
    initialize_earth_engine()

    import torch
    model, edge_index = load_model_and_graph(torch.device("cpu"))

    target_date = dt.date.today()
    node_batches = [nodes_all.iloc[i : i + 100].reset_index(drop=True) for i in range(0, len(nodes_all), 100)]  
    per_lake_results = []
    node_index_to_local = {int(r["node_index"]): i for i, r in nodes_all.iterrows()}

    print("\n[2/3] 🌳 Running batched XGBoost for multiple lakes...", flush=True)
    for batch_index, batch_nodes in enumerate(node_batches, start=1):
        print(f"Batch {batch_index}/{len(node_batches)}: fetching ERA5 for {len(batch_nodes)} lakes...", flush=True)
        raw_window, all_dates = fetch_era5_land_daily_for_nodes(batch_nodes, target_date, history_days=90)
        imputed_window = impute_raw_window(raw_window)
        batch_node_index_to_local = {int(r["node_index"]): i for i, r in batch_nodes.iterrows()}

        records = []
        for local_idx in range(imputed_window.shape[1]):
            gid = batch_nodes.iloc[local_idx]["GLAKE_ID"]
            for t_idx in range(90):
                row = {"GLAKE_ID": gid, "date": all_dates[t_idx]}
                for f_idx, col in enumerate(FEATURE_COLS):
                    value = imputed_window[t_idx, local_idx, f_idx]
                    row[col] = float(value) if not np.isnan(value) else None
                records.append(row)

        weather_df = pd.DataFrame.from_records(records)
        xgb_results = run_xgboost_batch(weather_df)

        print(f"Batch {batch_index}/{len(node_batches)}: running GNN...", flush=True)
        for _, node_row in batch_nodes.iterrows():
            glake_id = node_row["GLAKE_ID"]
            xres = xgb_results.get(glake_id)
            if xres:
                xgb_text = f"XGBoost Prediction: {xres['probability'] * 100:.1f}% probability of GLOF."
            else:
                xgb_text = "XGBoost Prediction: not available for this lake."

            center_node = int(node_row["node_index"])
            node_ids, sub_edge_index, center_local = build_k_hop_subgraph(edge_index, center_node, hops=NODE_HOPS)
            positions = [batch_node_index_to_local[n] for n in node_ids if n in batch_node_index_to_local]      
            if len(positions) != len(node_ids):
                gnn_res = {"error": "Missing regional nodes in all-lake fetch."}
            else:
                start_slice = 90 - HISTORY_DAYS
                sub_window = imputed_window[start_slice:, positions, :]
                gnn_res = run_gnn_inference(sub_window, model, sub_edge_index, center_local, torch.device("cpu"))

            if not isinstance(gnn_res, dict) or "error" in gnn_res:
                err = gnn_res.get("error") if isinstance(gnn_res, dict) else str(gnn_res)
                gnn_text = f"GNN Prediction: error - {err}"
            else:
                surf_mean = gnn_res.get("surface_runoff_sum_mean")
                risk = gnn_res.get("risk_level", "UNKNOWN")
                if surf_mean is None:
                    gnn_text = f"GNN summary: overall trigger {risk}."
                else:
                    subsurf_mean = gnn_res.get("sub_surface_runoff_sum_mean")
                    snowmelt_mean = gnn_res.get("snowmelt_sum_mean")
                    gnn_text = (
                        f"GNN summary: surface runoff {surf_mean:.5f} m, sub-surface runoff {subsurf_mean:.5f} m, "
                        f"snowmelt {snowmelt_mean:.5f} m; overall trigger {risk}."
                    )

            per_lake_results.append({"GLAKE_ID": glake_id, "xgb": xres, "gnn": gnn_res, "xgb_text": xgb_text, "gnn_text": gnn_text})

    ranked_results = sorted(
        per_lake_results,
        key=lambda item: item["xgb"]["probability"] if item.get("xgb") else -1.0,
        reverse=True,
    )

    top_results = ranked_results[:limit]
    if not top_results:
        return "No lakes were ranked."

    lines = [f"Top {len(top_results)} glacial lakes by forecast GLOF probability:"]
    for idx, item in enumerate(top_results, start=1):
        prob = item["xgb"]["probability"] * 100 if item.get("xgb") else None
        gnn = item.get("gnn", {})
        risk = gnn.get("risk_level", "UNKNOWN") if isinstance(gnn, dict) else "UNKNOWN"
        surf_mean = gnn.get("surface_runoff_sum_mean") if isinstance(gnn, dict) else None
        if prob is None:
            lines.append(f"{idx}. {item['GLAKE_ID']}: probability unavailable; GNN trigger {risk}.")
        else:
            if surf_mean is None:
                lines.append(f"{idx}. {item['GLAKE_ID']}: XGBoost probability {prob:.1f}%; GNN trigger {risk}.")
            else:
                lines.append(
                    f"{idx}. {item['GLAKE_ID']}: XGBoost probability {prob:.1f}%; "
                    f"GNN surface runoff {surf_mean:.5f} m; trigger {risk}."
                )

    return "\n".join(lines)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--lake", default="GL11")
    args = parser.parse_args()
    print(explain_glof_prediction(args.lake))
