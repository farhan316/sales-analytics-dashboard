"""
=============================================================
  Sales Analytics Dashboard — Step 2: EDA & Visualizations
  Dataset : Superstore Sales (Kaggle)
  Link    : https://www.kaggle.com/datasets/vivek468/superstore-dataset-final
=============================================================
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import warnings, os

warnings.filterwarnings("ignore")
os.makedirs("outputs/figures", exist_ok=True)

# ── Style ─────────────────────────────────────────────────
PALETTE   = ["#2563EB", "#7C3AED", "#059669", "#DC2626", "#D97706"]
BG_COLOR  = "#F8FAFC"
GRID_CLR  = "#E2E8F0"
TEXT_CLR  = "#1E293B"
ACCENT    = "#2563EB"

plt.rcParams.update({
    "figure.facecolor" : BG_COLOR,
    "axes.facecolor"   : BG_COLOR,
    "axes.edgecolor"   : GRID_CLR,
    "axes.labelcolor"  : TEXT_CLR,
    "axes.titlesize"   : 14,
    "axes.titleweight" : "bold",
    "axes.titlecolor"  : TEXT_CLR,
    "xtick.color"      : TEXT_CLR,
    "ytick.color"      : TEXT_CLR,
    "grid.color"       : GRID_CLR,
    "grid.linestyle"   : "--",
    "grid.alpha"       : 0.7,
    "font.family"      : "DejaVu Sans",
})

# ── Load clean data ───────────────────────────────────────
df = pd.read_csv("data/superstore_clean.csv", parse_dates=["order_date"])
print(f"✅ Loaded {len(df):,} rows\n")

# =============================================================
# PLOT 1 — Monthly Sales Trend
# =============================================================
def plot_sales_trend(df):
    monthly = (
        df.groupby(["year", "month"])
          .agg(sales=("sales","sum"), profit=("profit","sum"))
          .reset_index()
    )
    monthly["period"] = pd.to_datetime(
        monthly[["year","month"]].assign(day=1)
    )
    monthly.sort_values("period", inplace=True)

    fig, ax = plt.subplots(figsize=(14, 5))
    ax.fill_between(monthly["period"], monthly["sales"], alpha=0.15, color=ACCENT)
    ax.plot(monthly["period"], monthly["sales"], color=ACCENT, lw=2.5, label="Sales")
    ax.plot(monthly["period"], monthly["profit"], color="#059669", lw=2, ls="--", label="Profit")

    ax.set_title("Monthly Sales & Profit Trend")
    ax.set_xlabel("Month")
    ax.set_ylabel("Amount (USD)")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
    ax.legend(framealpha=0)
    ax.grid(True, axis="y")
    fig.tight_layout()
    fig.savefig("outputs/figures/01_sales_trend.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("📊 Plot 1 saved — Monthly Sales Trend")

# =============================================================
# PLOT 2 — Top 10 Products by Sales
# =============================================================
def plot_top_products(df):
    top = (
        df.groupby("product_name")["sales"]
          .sum()
          .nlargest(10)
          .reset_index()
          .sort_values("sales")
    )

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.barh(top["product_name"], top["sales"],
                   color=ACCENT, edgecolor="none", height=0.6)

    for bar in bars:
        w = bar.get_width()
        ax.text(w + 200, bar.get_y() + bar.get_height()/2,
                f"${w:,.0f}", va="center", fontsize=9, color=TEXT_CLR)

    ax.set_title("Top 10 Products by Revenue")
    ax.set_xlabel("Total Sales (USD)")
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
    ax.grid(True, axis="x")
    fig.tight_layout()
    fig.savefig("outputs/figures/02_top_products.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("📊 Plot 2 saved — Top 10 Products")

# =============================================================
# PLOT 3 — Sales & Profit by Region
# =============================================================
def plot_region(df):
    region = (
        df.groupby("region")
          .agg(sales=("sales","sum"), profit=("profit","sum"))
          .reset_index()
          .melt(id_vars="region", var_name="metric", value_name="amount")
    )

    fig, ax = plt.subplots(figsize=(9, 5))
    sns.barplot(data=region, x="region", y="amount", hue="metric",
                palette=[ACCENT, "#059669"], ax=ax, edgecolor="none")

    ax.set_title("Sales vs Profit by Region")
    ax.set_xlabel("Region")
    ax.set_ylabel("Amount (USD)")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
    ax.legend(title="", framealpha=0)
    ax.grid(True, axis="y")
    fig.tight_layout()
    fig.savefig("outputs/figures/03_region_analysis.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("📊 Plot 3 saved — Region Analysis")

# =============================================================
# PLOT 4 — Category & Sub-Category Profit
# =============================================================
def plot_category_profit(df):
    cat = (
        df.groupby(["category","sub_category"])
          .agg(profit=("profit","sum"))
          .reset_index()
          .sort_values("profit", ascending=False)
    )

    fig, ax = plt.subplots(figsize=(12, 6))
    colors = [PALETTE[0] if p > 0 else PALETTE[3] for p in cat["profit"]]
    ax.bar(range(len(cat)), cat["profit"], color=colors, edgecolor="none")
    ax.set_xticks(range(len(cat)))
    ax.set_xticklabels(cat["sub_category"], rotation=45, ha="right", fontsize=9)
    ax.axhline(0, color=TEXT_CLR, lw=0.8)
    ax.set_title("Profit by Sub-Category (Blue = Profit | Red = Loss)")
    ax.set_ylabel("Total Profit (USD)")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
    ax.grid(True, axis="y")
    fig.tight_layout()
    fig.savefig("outputs/figures/04_category_profit.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("📊 Plot 4 saved — Category Profit")

# =============================================================
# PLOT 5 — Discount vs Profit Scatter
# =============================================================
def plot_discount_profit(df):
    sample = df.sample(min(2000, len(df)), random_state=42)

    fig, ax = plt.subplots(figsize=(9, 5))
    scatter = ax.scatter(
        sample["discount"], sample["profit"],
        c=sample["profit"], cmap="RdYlGn",
        alpha=0.5, s=20, edgecolors="none"
    )
    plt.colorbar(scatter, ax=ax, label="Profit (USD)")
    ax.axhline(0, color=TEXT_CLR, lw=1, ls="--")
    ax.axvline(0.3, color=PALETTE[3], lw=1, ls="--", alpha=0.7, label="30% Discount line")
    ax.set_title("Discount Rate vs Profit (Each dot = 1 Order)")
    ax.set_xlabel("Discount Rate")
    ax.set_ylabel("Profit (USD)")
    ax.legend(framealpha=0, fontsize=9)
    ax.grid(True)
    fig.tight_layout()
    fig.savefig("outputs/figures/05_discount_profit.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("📊 Plot 5 saved — Discount vs Profit")

# =============================================================
# PLOT 6 — Ship Mode Distribution
# =============================================================
def plot_ship_mode(df):
    ship = df["ship_mode"].value_counts()
    colors = [PALETTE[i % len(PALETTE)] for i in range(len(ship))]

    fig, ax = plt.subplots(figsize=(7, 7))
    wedges, texts, autotexts = ax.pie(
        ship, labels=ship.index, autopct="%1.1f%%",
        colors=colors, startangle=140,
        wedgeprops={"edgecolor": BG_COLOR, "linewidth": 3},
        textprops={"color": TEXT_CLR}
    )
    for at in autotexts:
        at.set_fontsize(10)
        at.set_fontweight("bold")
        at.set_color("white")

    ax.set_title("Orders by Ship Mode", pad=20)
    fig.tight_layout()
    fig.savefig("outputs/figures/06_ship_mode.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("📊 Plot 6 saved — Ship Mode")

# =============================================================
# PLOT 7 — Quarterly Sales Heatmap
# =============================================================
def plot_quarterly_heatmap(df):
    pivot = df.pivot_table(
        index="year", columns="quarter",
        values="sales", aggfunc="sum"
    )
    pivot.columns = [f"Q{c}" for c in pivot.columns]

    fig, ax = plt.subplots(figsize=(8, 4))
    sns.heatmap(
        pivot, annot=True, fmt=",.0f", cmap="Blues",
        linewidths=0.5, linecolor=BG_COLOR, ax=ax,
        cbar_kws={"label": "Sales (USD)"}
    )
    ax.set_title("Quarterly Sales Heatmap by Year")
    ax.set_xlabel("Quarter")
    ax.set_ylabel("Year")
    fig.tight_layout()
    fig.savefig("outputs/figures/07_quarterly_heatmap.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("📊 Plot 7 saved — Quarterly Heatmap")

# =============================================================
# RUN ALL
# =============================================================
if __name__ == "__main__":
    print("=" * 55)
    print("  EXPLORATORY DATA ANALYSIS")
    print("=" * 55)

    # Summary stats
    print("\n📋 KEY METRICS:")
    print(f"   Total Revenue : ${df['sales'].sum():>12,.2f}")
    print(f"   Total Profit  : ${df['profit'].sum():>12,.2f}")
    print(f"   Profit Margin : {df['profit'].sum()/df['sales'].sum()*100:.2f}%")
    print(f"   Total Orders  : {df['order_id'].nunique():>12,}")
    print(f"   Unique Products: {df['product_name'].nunique():>11,}")
    print(f"   Customers     : {df['customer_id'].nunique():>12,}")
    print()

    plot_sales_trend(df)
    plot_top_products(df)
    plot_region(df)
    plot_category_profit(df)
    plot_discount_profit(df)
    plot_ship_mode(df)
    plot_quarterly_heatmap(df)

    print("\n✅ All plots saved to outputs/figures/")
