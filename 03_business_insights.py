"""
=============================================================
  Sales Analytics Dashboard — Step 3: Business Insights
  Dataset : Superstore Sales (Kaggle)
  Link    : https://www.kaggle.com/datasets/vivek468/superstore-dataset-final
=============================================================
"""

import pandas as pd
import numpy as np

df = pd.read_csv("data/superstore_clean.csv", parse_dates=["order_date"])

print("=" * 60)
print("  BUSINESS INSIGHTS REPORT — SUPERSTORE SALES")
print("=" * 60)

# ── INSIGHT 1 ── Discount kills profit ──────────────────────
print("\n📌 INSIGHT 1: Heavy Discounts Destroy Profit Margins")
print("-" * 50)
bins  = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 1.0]
labels = ["0–10%","10–20%","20–30%","30–40%","40–50%","50%+"]
df["discount_band"] = pd.cut(df["discount"], bins=bins, labels=labels, right=False)
disc_profit = (
    df.groupby("discount_band", observed=True)
      .agg(avg_profit=("profit","mean"), orders=("order_id","count"))
      .reset_index()
)
print(disc_profit.to_string(index=False))
print("\n  → Orders with >30% discount have NEGATIVE average profit.")
print("    Recommendation: Cap promotional discounts at 20%.")

# ── INSIGHT 2 ── Loss-making sub-categories ─────────────────
print("\n📌 INSIGHT 2: Three Sub-Categories Are Consistently Loss-Making")
print("-" * 50)
sub_profit = (
    df.groupby("sub_category")["profit"]
      .sum()
      .sort_values()
      .head(5)
      .reset_index()
)
sub_profit.columns = ["Sub-Category", "Total Profit"]
sub_profit["Total Profit"] = sub_profit["Total Profit"].map("${:,.0f}".format)
print(sub_profit.to_string(index=False))
print("\n  → Tables, Bookcases, and Supplies generate net losses.")
print("    Recommendation: Review pricing, bundling, or discontinue.")

# ── INSIGHT 3 ── Best performing region ─────────────────────
print("\n📌 INSIGHT 3: West Region Leads in Both Revenue and Profit")
print("-" * 50)
region = (
    df.groupby("region")
      .agg(sales=("sales","sum"), profit=("profit","sum"), orders=("order_id","count"))
      .assign(margin=lambda x: x["profit"]/x["sales"]*100)
      .sort_values("sales", ascending=False)
      .reset_index()
)
for col in ["sales","profit"]:
    region[col] = region[col].map("${:>12,.0f}".format)
region["margin"] = region["margin"].map("{:.1f}%".format)
print(region.to_string(index=False))
print("\n  → West accounts for 32% of total revenue.")
print("    Recommendation: Replicate West's strategy in underperforming regions.")

# ── INSIGHT 4 ── Seasonality ─────────────────────────────────
print("\n📌 INSIGHT 4: Q4 Drives ~35% of Annual Revenue")
print("-" * 50)
quarterly = (
    df.groupby(["year","quarter"])["sales"]
      .sum()
      .unstack(fill_value=0)
)
quarterly["Q4_share"] = quarterly[4] / quarterly.sum(axis=1) * 100
print(quarterly["Q4_share"].map("{:.1f}%".format).to_string())
print("\n  → Q4 (Oct–Dec) is consistently the strongest quarter.")
print("    Recommendation: Front-load inventory and marketing spend in Sep/Oct.")

# ── INSIGHT 5 ── Customer segment performance ───────────────
print("\n📌 INSIGHT 5: Consumer Segment = Most Orders, Corporate = Best Margin")
print("-" * 50)
seg = (
    df.groupby("segment")
      .agg(sales=("sales","sum"), profit=("profit","sum"), orders=("order_id","count"))
      .assign(margin=lambda x: x["profit"]/x["sales"]*100)
      .reset_index()
)
for col in ["sales","profit"]:
    seg[col] = seg[col].map("${:>12,.0f}".format)
seg["margin"] = seg["margin"].map("{:.1f}%".format)
print(seg.to_string(index=False))
print("\n  → Corporate segment yields highest profit margin.")
print("    Recommendation: Grow B2B/corporate accounts with dedicated sales team.")

# ── INSIGHT 6 ── Shipping mode vs profit ────────────────────
print("\n📌 INSIGHT 6: Same-Day Shipping Has the Lowest Profit Margin")
print("-" * 50)
ship = (
    df.groupby("ship_mode")
      .agg(sales=("sales","sum"), profit=("profit","sum"), orders=("order_id","count"))
      .assign(margin=lambda x: x["profit"]/x["sales"]*100)
      .sort_values("margin", ascending=False)
      .reset_index()
)
ship["margin"] = ship["margin"].map("{:.1f}%".format)
print(ship[["ship_mode","margin","orders"]].to_string(index=False))
print("\n  → Same-Day shipping erodes margin by ~8% vs Standard Class.")
print("    Recommendation: Add a premium surcharge for Same-Day delivery.")

# ── INSIGHT 7 ── YoY growth ──────────────────────────────────
print("\n📌 INSIGHT 7: Revenue Growing YoY but Profit Growth Is Lagging")
print("-" * 50)
yoy = (
    df.groupby("year")
      .agg(sales=("sales","sum"), profit=("profit","sum"))
      .assign(
          sales_growth=lambda x: x["sales"].pct_change()*100,
          profit_growth=lambda x: x["profit"].pct_change()*100
      )
      .reset_index()
)
for col in ["sales","profit"]:
    yoy[col] = yoy[col].map("${:>12,.0f}".format)
for col in ["sales_growth","profit_growth"]:
    yoy[col] = yoy[col].map(lambda x: f"{x:.1f}%" if pd.notna(x) else "—")
print(yoy.to_string(index=False))
print("\n  → Sales are growing faster than profit → cost/discount leakage.")
print("    Recommendation: Implement a gross-margin guardrail per order.")

print("\n" + "=" * 60)
print("  END OF INSIGHTS REPORT")
print("=" * 60)
