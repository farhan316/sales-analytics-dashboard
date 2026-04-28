"""
=============================================================
  Sales Analytics Dashboard — Step 1: Data Cleaning
  Dataset : Superstore Sales (Kaggle)
  Link    : https://www.kaggle.com/datasets/vivek468/superstore-dataset-final
=============================================================
"""

import pandas as pd
import numpy as np
import os

# ── Paths ─────────────────────────────────────────────────
RAW_PATH    = "data/superstore_raw.csv"
CLEAN_PATH  = "data/superstore_clean.csv"
os.makedirs("data", exist_ok=True)

# ── 1. Load ───────────────────────────────────────────────
print("📂 Loading dataset …")
df = pd.read_csv(RAW_PATH, encoding="latin-1")
print(f"   Raw shape : {df.shape}")
print(f"   Columns   : {list(df.columns)}\n")

# ── 2. Inspect ────────────────────────────────────────────
print("🔍 Missing values:")
print(df.isnull().sum()[df.isnull().sum() > 0], "\n")
print("🔍 Duplicate rows :", df.duplicated().sum(), "\n")
print("🔍 Data types:\n", df.dtypes, "\n")

# ── 3. Rename columns (snake_case) ────────────────────────
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
    .str.replace("-", "_")
)

# ── 4. Parse dates ────────────────────────────────────────
for col in ["order_date", "ship_date"]:
    df[col] = pd.to_datetime(df[col], dayfirst=False, errors="coerce")

# ── 5. Drop duplicates ────────────────────────────────────
before = len(df)
df.drop_duplicates(subset="order_id", keep="first", inplace=True)
print(f"🗑  Dropped {before - len(df)} duplicate order rows\n")

# ── 6. Handle missing values ──────────────────────────────
# Postal code — fill with 0 (some locations lack ZIP)
if "postal_code" in df.columns:
    df["postal_code"] = df["postal_code"].fillna(0).astype(int)

# ── 7. Derived columns ────────────────────────────────────
df["year"]          = df["order_date"].dt.year
df["month"]         = df["order_date"].dt.month
df["month_name"]    = df["order_date"].dt.strftime("%b")
df["quarter"]       = df["order_date"].dt.quarter
df["ship_duration"] = (df["ship_date"] - df["order_date"]).dt.days
df["profit_margin"] = (df["profit"] / df["sales"]).round(4)

# ── 8. Fix negative quantities / sales ────────────────────
df = df[df["quantity"] > 0]
df = df[df["sales"] > 0]

# ── 9. Final sanity check ─────────────────────────────────
print("✅ Clean shape :", df.shape)
print("   Nulls remaining:", df.isnull().sum().sum())
print("   Date range :", df["order_date"].min().date(), "→", df["order_date"].max().date())

# ── 10. Save ──────────────────────────────────────────────
df.to_csv(CLEAN_PATH, index=False)
print(f"\n💾 Saved → {CLEAN_PATH}")
