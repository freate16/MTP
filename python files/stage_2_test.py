import pandas as pd
import geopandas as gpd
import numpy as np
import joblib
import os
import duckdb

# ==========================================
# Configuration & Paths
# ==========================================
WEATHER_DATA_PATH = r"C:\Users\rubel\Downloads\era5_lakes_test.csv"
LAKE_STATIC_DATA_PATH = r"model_data\Final data\stage2_dataset_15.gpkg"
MODEL_PATH = r"model_data\Final data\best_f2_xgb_model.joblib"
OUTPUT_PATH = r"model_data\Final data\stage_2_test_predictions.csv"
NODE_MAPPING_PATH = r"gnn\node_mapping.csv" # Adjust if your true location differs

# ==========================================
# Data Loading & Merging
# ==========================================
def run_predictions():
    print("1. Loading static datasets...")
    if not os.path.exists(WEATHER_DATA_PATH):
        print(f"Error: Weather data not found at {WEATHER_DATA_PATH}")
        return
        
    static_lakes_gdf = gpd.read_file(LAKE_STATIC_DATA_PATH)
    lakes_df = pd.DataFrame(static_lakes_gdf.drop(columns="geometry"))
    lakes_df['GLAKE_ID'] = lakes_df['GLAKE_ID'].astype(str).str.strip().str.upper()

    print(f"2. Building temporal aggregates matching against node mapping...")
    try:
        node_map = pd.read_csv(NODE_MAPPING_PATH)
        node_map_path_escaped = NODE_MAPPING_PATH.replace('\\', '/')
        weather_data_path_escaped = WEATHER_DATA_PATH.replace('\\', '/')
    except FileNotFoundError:
        print(f"Error: mapping file missing at {NODE_MAPPING_PATH}")
        # fallback to directly trying to process if possible
        node_map_path_escaped = None

    if node_map_path_escaped:
        query = f"""
        WITH raw_era5 AS (
            SELECT 
                fid AS era5_fid,
                CAST(CAST("date" AS VARCHAR) AS DATE) AS obs_date,
                total_precipitation_sum,
                snowmelt_sum,
                surface_runoff_sum,
                sub_surface_runoff_sum,
                snowfall_sum,
                temperature_2m,
                dewpoint_temperature_2m,
                snow_depth_water_equivalent,
                surface_pressure
            FROM read_csv_auto('{weather_data_path_escaped}')
        ),
        mapping AS (
            SELECT 
                era5_fid,
                GLAKE_ID 
            FROM read_csv_auto('{node_map_path_escaped}')
        ),
        mapped_era5 AS (
            SELECT 
                m.GLAKE_ID,
                e.* EXCLUDE (era5_fid)
            FROM mapping m
            JOIN raw_era5 e ON m.era5_fid = e.era5_fid
        ),
        lake_targets AS (
            SELECT 
                GLAKE_ID, 
                MAX(obs_date) as event_date
            FROM mapped_era5 
            GROUP BY GLAKE_ID
        )
        SELECT 
            t.GLAKE_ID,
            
            -- 3 DAY WINDOW
            SUM(CASE WHEN e.obs_date BETWEEN t.event_date - INTERVAL 2 DAYS AND t.event_date THEN e.total_precipitation_sum END) AS total_precipitation_sum_3d,
            SUM(CASE WHEN e.obs_date BETWEEN t.event_date - INTERVAL 2 DAYS AND t.event_date THEN e.snowmelt_sum END) AS snowmelt_sum_3d,
            SUM(CASE WHEN e.obs_date BETWEEN t.event_date - INTERVAL 2 DAYS AND t.event_date THEN e.surface_runoff_sum END) AS surface_runoff_sum_3d,
            AVG(CASE WHEN e.obs_date BETWEEN t.event_date - INTERVAL 2 DAYS AND t.event_date THEN e.surface_pressure END) AS surface_pressure_mean_3d,
            AVG(CASE WHEN e.obs_date BETWEEN t.event_date - INTERVAL 2 DAYS AND t.event_date THEN e.dewpoint_temperature_2m END) AS dewpoint_temperature_2m_mean_3d,

            -- 7 DAY WINDOW
            SUM(CASE WHEN e.obs_date BETWEEN t.event_date - INTERVAL 6 DAYS AND t.event_date THEN e.total_precipitation_sum END) AS total_precipitation_sum_7d,
            SUM(CASE WHEN e.obs_date BETWEEN t.event_date - INTERVAL 6 DAYS AND t.event_date THEN e.snowmelt_sum END) AS snowmelt_sum_7d,
            SUM(CASE WHEN e.obs_date BETWEEN t.event_date - INTERVAL 6 DAYS AND t.event_date THEN e.surface_runoff_sum END) AS surface_runoff_sum_7d,
            SUM(CASE WHEN e.obs_date BETWEEN t.event_date - INTERVAL 6 DAYS AND t.event_date THEN e.sub_surface_runoff_sum END) AS sub_surface_runoff_sum_7d,
            SUM(CASE WHEN e.obs_date BETWEEN t.event_date - INTERVAL 6 DAYS AND t.event_date THEN e.snowfall_sum END) AS snowfall_sum_7d,
            AVG(CASE WHEN e.obs_date BETWEEN t.event_date - INTERVAL 6 DAYS AND t.event_date THEN e.temperature_2m END) AS temperature_2m_mean_7d,
            AVG(CASE WHEN e.obs_date BETWEEN t.event_date - INTERVAL 6 DAYS AND t.event_date THEN e.dewpoint_temperature_2m END) AS dewpoint_temperature_2m_mean_7d,
            AVG(CASE WHEN e.obs_date BETWEEN t.event_date - INTERVAL 6 DAYS AND t.event_date THEN e.snow_depth_water_equivalent END) AS snow_depth_water_equivalent_mean_7d,
            AVG(CASE WHEN e.obs_date BETWEEN t.event_date - INTERVAL 6 DAYS AND t.event_date THEN e.surface_pressure END) AS surface_pressure_mean_7d,

            -- 30 DAY WINDOW
            SUM(CASE WHEN e.obs_date BETWEEN t.event_date - INTERVAL 29 DAYS AND t.event_date THEN e.total_precipitation_sum END) AS total_precipitation_sum_30d,
            SUM(CASE WHEN e.obs_date BETWEEN t.event_date - INTERVAL 29 DAYS AND t.event_date THEN e.snowmelt_sum END) AS snowmelt_sum_30d,
            SUM(CASE WHEN e.obs_date BETWEEN t.event_date - INTERVAL 29 DAYS AND t.event_date THEN e.surface_runoff_sum END) AS surface_runoff_sum_30d,
            SUM(CASE WHEN e.obs_date BETWEEN t.event_date - INTERVAL 29 DAYS AND t.event_date THEN e.sub_surface_runoff_sum END) AS sub_surface_runoff_sum_30d,
            SUM(CASE WHEN e.obs_date BETWEEN t.event_date - INTERVAL 29 DAYS AND t.event_date THEN e.snowfall_sum END) AS snowfall_sum_30d,
            AVG(CASE WHEN e.obs_date BETWEEN t.event_date - INTERVAL 29 DAYS AND t.event_date THEN e.temperature_2m END) AS temperature_2m_mean_30d,
            AVG(CASE WHEN e.obs_date BETWEEN t.event_date - INTERVAL 29 DAYS AND t.event_date THEN e.snow_depth_water_equivalent END) AS snow_depth_water_equivalent_mean_30d,

            -- 90 DAY WINDOW
            SUM(CASE WHEN e.obs_date BETWEEN t.event_date - INTERVAL 89 DAYS AND t.event_date THEN e.total_precipitation_sum END) AS total_precipitation_sum_90d,
            SUM(CASE WHEN e.obs_date BETWEEN t.event_date - INTERVAL 89 DAYS AND t.event_date THEN e.snowmelt_sum END) AS snowmelt_sum_90d,
            SUM(CASE WHEN e.obs_date BETWEEN t.event_date - INTERVAL 89 DAYS AND t.event_date THEN e.sub_surface_runoff_sum END) AS sub_surface_runoff_sum_90d,
            SUM(CASE WHEN e.obs_date BETWEEN t.event_date - INTERVAL 89 DAYS AND t.event_date THEN e.snowfall_sum END) AS snowfall_sum_90d,
            AVG(CASE WHEN e.obs_date BETWEEN t.event_date - INTERVAL 89 DAYS AND t.event_date THEN e.temperature_2m END) AS temperature_2m_mean_90d,
            AVG(CASE WHEN e.obs_date BETWEEN t.event_date - INTERVAL 89 DAYS AND t.event_date THEN e.snow_depth_water_equivalent END) AS snow_depth_water_equivalent_mean_90d

        FROM lake_targets t
        JOIN mapped_era5 e ON t.GLAKE_ID = e.GLAKE_ID
        GROUP BY t.GLAKE_ID
        """

        con = duckdb.connect()
        try:
            weather_df = con.execute(query).df()
        except Exception as e:
            print(f"Error querying CSV natively: {e}")
            return
        finally:
            con.close()
    
    print("3. Merging processed weather aggregates with static lake properties...")
    weather_df['GLAKE_ID'] = weather_df['GLAKE_ID'].astype(str).str.strip().str.upper()
    gdf = pd.merge(lakes_df, weather_df, on="GLAKE_ID", how="inner")
    print(f"   Successfully matched {len(gdf)} lakes for prediction.")

    # ==========================================
    # Feature Engineering
    # ==========================================
    print("3. Applying Feature Engineering...")
    
    try:
        # Climate Anomalies
        gdf['precip_anomaly_7d_90d'] = gdf['total_precipitation_sum_7d'] / (gdf['total_precipitation_sum_90d'] / 90 * 7 + 1e-5)
        gdf['snowmelt_anomaly_7d_30d'] = gdf['snowmelt_sum_7d'] / (gdf['snowmelt_sum_30d'] / 30 * 7 + 1e-5)
        gdf['temp_spike_7d_over_30d'] = gdf['temperature_2m_mean_7d'] - gdf['temperature_2m_mean_30d']
        gdf['runoff_shock'] = gdf['surface_runoff_sum_3d'] / (gdf['surface_runoff_sum_30d'] / 10 + 1e-5)
        
        # Physics Proxies
        gdf['dam_instability_index'] = (gdf['dam_height_m'] * gdf['dam_slope_deg']) / (gdf['dam_width_m'] + 1)
        gdf['ice_avalanche_calving_proxy'] = gdf['v_mean_2020'] * gdf['contact_m']
        gdf['hydrostatic_pressure_proxy'] = gdf['volume_m3'] * gdf['max_depth_m']
        
        # Hydrological Loading
        gdf['watershed_to_lake_area_ratio'] = gdf['watershed_area_km2'] / (gdf['area_2020_km2'] + 1e-5)
        # How much precip is entering the lake relative to its volume?
        gdf['precip_loading_factor'] = (gdf['total_precipitation_sum_7d'] * gdf['watershed_area_km2']) / (gdf['volume_m3'] + 1e-5)

        # Melt-dominated vs rain-dominated events
        gdf['snowmelt_fraction_7d'] = (
            gdf['snowmelt_sum_7d'] /
            (gdf['snowmelt_sum_7d'] + 
             gdf['total_precipitation_sum_7d'] + 1e-8)
        )
        gdf['melt_acceleration'] = (
            gdf['snowmelt_sum_7d'] - 
            gdf['snowmelt_sum_30d'] / 4
        )
        gdf['melt_heat_index'] = (
            gdf['snowmelt_sum_7d'] *
            gdf['temperature_2m_mean_7d']
        )
    except KeyError as e:
        print(f"\nError computing features! Missing expected column: {e}")
        print("Please ensure the weather CSV contains columns like 'total_precipitation_sum_7d', 'snowmelt_sum_30d', etc.")
        return

    # ==========================================
    # Model Inference
    # ==========================================
    print("4. Loading XGBoost model and aligning features...")
    model = joblib.load(MODEL_PATH)
    
    # Grab the exact feature order the model expects
    expected_features = model.feature_names_in_
    
    # Check for missing features in our new dataframe
    missing_cols = [c for c in expected_features if c not in gdf.columns]
    if missing_cols:
        print(f"   Warning: {len(missing_cols)} features expected by the model are missing.")
        print(f"   Sample missing: {missing_cols[:5]}")
        print("   Filling missing features with NaN so script can proceed.")
        for col in missing_cols:
            gdf[col] = np.nan
            
    # Isolate X to only the expected features
    X_test = gdf[expected_features]
    
    print("5. Predicting Susceptibility Probabilities...")
    probabilities = model.predict_proba(X_test)[:, 1]
    
    gdf['glof_prob'] = probabilities
    
    # Sort from highest risk to lowest
    results_df = gdf.sort_values(by='glof_prob', ascending=False)
    
    # Extract ID, Probability, and Model Features for saving
    output_cols = ['GLAKE_ID', 'glof_prob'] + list(expected_features)
    results_out = results_df[output_cols]
    
    results_out.to_csv(OUTPUT_PATH, index=False)
    print(f"\n=== FINISHED ===")
    print(f"Full predictions saved to: {OUTPUT_PATH}")
    
    print("\n--- TOP 10 HIGHEST RISK LAKES IN THIS SNAPSHOT ---")
    print(results_out[['GLAKE_ID', 'glof_prob']].head(10).to_string(index=False))

if __name__ == "__main__":
    run_predictions()
