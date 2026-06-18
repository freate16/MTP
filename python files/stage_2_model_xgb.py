import pandas as pd
import numpy as np
import xgboost as xgb
import optuna
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import fbeta_score, average_precision_score, roc_auc_score
import joblib
import json
import geopandas as gpd
# ==========================================
# Helper Function for Recall @ K
# ==========================================
def calc_recall_at_k(y_true, y_probs, k):
    # Sort actuals by predicted probabilities
    ordered_indices = np.argsort(y_probs)[::-1]
    y_true_sorted = np.array(y_true)[ordered_indices]
    
    # Take top k
    top_k_actuals = y_true_sorted[:k]
    
    # Calculate recall: True Positives in top K / Total Actual Positives
    total_positives = np.sum(y_true)
    if total_positives == 0:
        return 0
    return np.sum(top_k_actuals) / total_positives

# ==========================================
# Configuration
# ==========================================
DATA_PATH = r"model_data\Final data\stage_2_final_dataset5.gpkg"
TARGET_COL = "glof_happened"
N_TRIALS = 1500
RANDOM_STATE = 42

# Columns to exclude from training (identifiers, geometry, dates, etc.)
EXCLUDE_COLS = ['GLAKE_ID_glof', 'RGIId','geometry_1990','geometry_2000','geometry_2010', 'geometry_2015','index_right','Type',
        'nearest_rgiid', 'new_trial_score','original_row_id','s1_GL_ID','s2_Lake_type','source_type','susceptibility_band',
        'geometry','_join_id']

# ==========================================
# Data Loading & Prep
# ==========================================

feature_cols = [
    # ── STATIC LAKE MORPHOMETRY ──,
    'surface_elevation_m',
    'area_2020_km2',
    'area_perimeter_ratio',
    'compactness',
    'max_depth_m',
    'volume_m3',
    'perimeter_2020',
    
    # ── DAM CHARACTERISTICS ──
    'dam_slope_deg',
    'dam_height_m',
    'dam_width_m',
    'freeboard_m',
    
    # ── GLACIER INTERACTION ──
    'distance_to_glacier_inv',
    'is_connected',
    'contact_m',              # glacier-lake contact length
    'v_mean_2020',            # ITS_LIVE velocity
    'G11_mean_slope_deg',     # mean glacier slope
    'watershed_area_km2',
    
    # ── HAZARD PROXIES ──
    'eq_susceptibility',
    'ls_susceptibility',
    
    # ── TEMPORAL LAKE DYNAMICS ──
    'expansion_rate_km2_yr',
    'expansion_rate_pct_yr',
    'expansion_consistency',
    'area_std_across_years',
    'area_cv_across_years',
    'area_cagr_total_pct',
    'max_interval_expansion',
    'max_interval_shrink',
    'n_expanding_intervals',
    'n_shrinking_intervals',
    'area_exp_total',
    'area_exp_total_pct',

    # Per-period expansion
    'area_exp_1990_2000', 'area_exp_pct_1990_2000', 'area_cagr_pct_1990_2000',
    'area_exp_2000_2010', 'area_exp_pct_2000_2010', 'area_cagr_pct_2000_2010',
    'area_exp_2010_2015', 'area_exp_pct_2010_2015', 'area_cagr_pct_2010_2015',
    'area_exp_2015_2020', 'area_exp_pct_2015_2020', 'area_cagr_pct_2015_2020',

    # Per-period shrink
    'area_shrink_1990_2000', 'area_shrink_2000_2010',
    'area_shrink_2010_2015', 'area_shrink_2015_2020', 'area_shrink_total',

    # Perimeter history
    'perimeter_1990', 'perimeter_2000', 'perimeter_2010', 'perimeter_2015',

    # Area history
    'area_1990_km2', 'area_2000_km2', 'area_2010_km2', 'area_2015_km2',
    
    # ── LAKE TYPE ──
    'lake_type_encoded',
    
    # ── STAGE 1 OUTPUT — critical feature ──

    # ── CLIMATE — 3d (flux only) ──
    'total_precipitation_sum_3d',
    'snowmelt_sum_3d',
    'surface_runoff_sum_3d',

    # ── CLIMATE — 7d ──
    'total_precipitation_sum_7d',
    'snowmelt_sum_7d',
    'surface_runoff_sum_7d',
    'sub_surface_runoff_sum_7d',
    'snowfall_sum_7d',
    'temperature_2m_mean_7d',
    'dewpoint_temperature_2m_mean_7d',
    'snow_depth_water_equivalent_mean_7d',
    'surface_pressure_mean_7d',

    # ── CLIMATE — 30d ──
    'total_precipitation_sum_30d',
    'snowmelt_sum_30d',
    'surface_runoff_sum_30d',
    'sub_surface_runoff_sum_30d',
    'snowfall_sum_30d',
    'temperature_2m_mean_30d',
    'snow_depth_water_equivalent_mean_30d',

    # ── CLIMATE — 90d ──
    'total_precipitation_sum_90d',
    'snowmelt_sum_90d',
    'sub_surface_runoff_sum_90d',
    'snowfall_sum_90d',
    'temperature_2m_mean_90d',
    'snow_depth_water_equivalent_mean_90d',

    # -- anomalies and proxies
    'precip_anomaly_7d_90d',
    'snowmelt_anomaly_7d_30d',
    'temp_spike_7d_over_30d',
    'runoff_shock',
    'dam_instability_index',
    'ice_avalanche_calving_proxy',
    'hydrostatic_pressure_proxy',
    'watershed_to_lake_area_ratio',
    'precip_loading_factor',
    'snowmelt_fraction_7d',
    'melt_acceleration',
    'melt_heat_index'
]
print("Loading data...")
df = gpd.read_file(DATA_PATH)

# Drop excluded columns
features = [c for c in df.columns if c not in EXCLUDE_COLS and c != TARGET_COL]
X = df[feature_cols]
y = df[TARGET_COL]

print(f"Dataset shape: {X.shape}")
print(f"Positive events: {y.sum()} / {len(y)}")

# Calculate rough ratio for scale_pos_weight
pos_count = y.sum()
neg_count = len(y) - pos_count
imbalance_ratio = neg_count / pos_count

# ==========================================
# Optuna Objective
# ==========================================
def objective(trial):
    # Hyperparameter search space
    params = {
        "objective": "binary:logistic",
        "eval_metric": "aucpr", # Track precision-recall internally
        "tree_method": "hist",
        "random_state": RANDOM_STATE,
        "n_estimators": trial.suggest_int("n_estimators", 50, 1000),
        "max_depth": trial.suggest_int("max_depth", 3, 9),
        "learning_rate": trial.suggest_float("learning_rate", 1e-3, 0.1, log=True),
        "subsample": trial.suggest_float("subsample", 0.5, 1.0),
        "colsample_bytree": trial.suggest_float("colsample_bytree", 0.5, 1.0),
        "gamma": trial.suggest_float("gamma", 0.0, 5.0),
        "min_child_weight": trial.suggest_int("min_child_weight", 1, 10),
        "reg_alpha": trial.suggest_float("reg_alpha", 1e-5, 10.0, log=True),
        "reg_lambda": trial.suggest_float("reg_lambda", 1e-5, 10.0, log=True),
        # Crucial for imbalanced dataset: allows tuning the penalty of false negatives
        "scale_pos_weight": trial.suggest_float("scale_pos_weight", imbalance_ratio * 0.5, imbalance_ratio * 2.5) 
    }

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
    
    oof_probs = np.zeros(len(X))
    oof_preds = np.zeros(len(X))
    
    for train_idx, val_idx in cv.split(X, y):
        X_train, X_val = X.iloc[train_idx], X.iloc[val_idx]
        y_train, y_val = y.iloc[train_idx], y.iloc[val_idx]
        
        model = xgb.XGBClassifier(**params)
        model.fit(
            X_train, y_train,
            eval_set=[(X_val, y_val)],
            verbose=False
        )
        
        # Store out-of-fold predictions
        oof_probs[val_idx] = model.predict_proba(X_val)[:, 1]
        oof_preds[val_idx] = model.predict(X_val)
        
    # Calculate overall metrics on OOF predictions (Cross-Validated Unbiased metrics) 
    # for the objective function.
    f2 = fbeta_score(y, oof_preds, beta=2, zero_division=0)
    ap = average_precision_score(y, oof_probs)
    
    # We must use Out-Of-Fold (oof_probs) to calculate the "whole dataset" metrics. 
    # In 5-fold CV, oof_probs contains exactly 1,500 predictions (1 prediction for 
    # every single row in your dataset), but calculated WITHOUT data leakage. 
    # This gives you the true, unbiased Recall@K over the whole dataset.
    auc = roc_auc_score(y, oof_probs)
    r50 = calc_recall_at_k(y, oof_probs, 50)
    r100 = calc_recall_at_k(y, oof_probs, 100)
    r200 = calc_recall_at_k(y, oof_probs, 200)
    r350 = calc_recall_at_k(y, oof_probs, 350)
    r500 = calc_recall_at_k(y, oof_probs, 500)
    
    # Track them in Optuna trial attributes
    trial.set_user_attr("ap", ap)
    trial.set_user_attr("f2", f2)
    trial.set_user_attr("auc", auc)
    trial.set_user_attr("recall@50", r50)
    trial.set_user_attr("recall@100", r100)
    trial.set_user_attr("recall@200", r200)
    trial.set_user_attr("recall@350", r350)
    trial.set_user_attr("recall@500", r500)
        
    # Return both metrics to enable Multi-Objective Optimization
    return f2, ap

# ==========================================
# Run Multi-Objective Optimization
# ==========================================
if __name__ == "__main__":
    print("Starting Multi-Objective Optuna Study...")
    # Directions: [Maximize F2, Maximize AP]
    study = optuna.create_study(directions=["maximize", "maximize"])
    study.optimize(objective, n_trials=N_TRIALS, show_progress_bar=True)
    
    print("\noptimization finished.")
    print(f"Number of finished trials: {len(study.trials)}")
    
    # Get the Pareto Front trials (the trade-off curve models)
    pareto_front = study.best_trials
    
    print(f"\n--- PARETO FRONT ({len(pareto_front)} optimum trade-off models) ---")
    
    best_f2_trial = max(pareto_front, key=lambda t: t.values[0])
    best_ap_trial = max(pareto_front, key=lambda t: t.values[1])
    
    print("\n1. Model specialized for Best F2 Score (Prioritizes catching events!):")
    print(f"   F2 Score: {best_f2_trial.values[0]:.4f}")
    print(f"   AP Score: {best_f2_trial.values[1]:.4f}")
    print(f"   Params: {best_f2_trial.params}")
    
    print("\n2. Model specialized for Best AP Score (Prioritizes pure probability ranking):")
    print(f"   F2 Score: {best_ap_trial.values[0]:.4f}")
    print(f"   AP Score: {best_ap_trial.values[1]:.4f}")
    print(f"   Params: {best_ap_trial.params}")

    # Optionally retrain and save the most balanced model or best F2 model
    print("\nRetraining the best F2 model on the full dataset...")
    best_params = best_f2_trial.params
    best_params['objective'] = "binary:logistic"
    best_params['tree_method'] = "hist"
    
    final_model = xgb.XGBClassifier(**best_params)
    final_model.fit(X, y)
    
    joblib.dump(final_model, r'model_data\Final data\best_f2_xgb_model.joblib')
    print("Saved 'model_data\\Final data\\best_f2_xgb_model.joblib'")

    # Extract Top 10 models (sorting primarily by F2 score)
    trials_df = study.trials_dataframe()
    # Handle completed trials only
    completed_trials = trials_df[trials_df['state'] == 'COMPLETE'].copy()
    
    if not completed_trials.empty:
        # Sort by F2 (values_0) descending to get top 10
        top_10 = completed_trials.sort_values(by="values_0", ascending=False).head(10)
        
        # Filter and rename hyperparameter columns
        param_cols = [c for c in top_10.columns if c.startswith('params_')]
        top_10_params = top_10[['number'] + param_cols].copy()
        top_10_params.columns = [c.replace('params_', '') for c in top_10_params.columns]
        
        # Filter and rename metric columns
        attr_cols = [c for c in top_10.columns if c.startswith('user_attrs_')]
        top_10_metrics = top_10[['number'] + attr_cols].copy()
        top_10_metrics.columns = [c.replace('user_attrs_', '') for c in top_10_metrics.columns]
        
        top_10_params.to_csv(r'model_data\Final data\top_10_hyperparameters.csv', index=False)
        top_10_metrics.to_csv(r'model_data\Final data\top_10_metrics.csv', index=False)
        print("\nSaved Top 10 Hyperparameters to 'top_10_hyperparameters.csv'")
        print("Saved Top 10 Metrics to 'top_10_metrics.csv'")
