# Power BI Dashboard Design Plan
## Superstore Sales Analytics Dashboard

---

## 📐 Dashboard Layout (3 Pages)

---

### PAGE 1 — Executive Overview

**Purpose:** C-suite summary — one-glance health check

#### KPI Cards (Top Row)
| KPI Card | Measure | Format |
|---|---|---|
| Total Revenue | `SUM(Sales[Sales])` | `$#,##0` |
| Total Profit | `SUM(Sales[Profit])` | `$#,##0` |
| Profit Margin | `DIVIDE([Total Profit],[Total Revenue])` | `0.0%` |
| Total Orders | `DISTINCTCOUNT(Sales[Order ID])` | `#,##0` |
| Avg Order Value | `DIVIDE([Total Revenue],[Total Orders])` | `$#,##0` |
| YoY Sales Growth | `([Sales CY]-[Sales PY])/[Sales PY]` | `+0.0%` |

#### Visuals
- **Line Chart** — Monthly Sales & Profit Trend (with forecast line)
- **Bar Chart** — Sales by Region (sorted descending)
- **Donut Chart** — Revenue Share by Segment
- **Map Visual** — Sales by State (filled map, bubble size = profit)

#### Slicers (Left Panel)
- Year (2014–2017)
- Region (multi-select)
- Segment (Consumer / Corporate / Home Office)
- Category (Furniture / Office Supplies / Technology)

---

### PAGE 2 — Product & Category Deep Dive

**Purpose:** Merchandising & product manager view

#### Visuals
- **Clustered Bar** — Top 15 Products by Sales
- **Matrix/Table** — Sub-Category | Sales | Profit | Margin | YoY Δ
- **Scatter Plot** — Discount Rate vs Profit Margin (bubble = order count)
- **Treemap** — Revenue by Category → Sub-Category (drill-down)
- **Waterfall Chart** — Profit bridge by Sub-Category

#### DAX Measures for this page
```dax
Profit Margin % = DIVIDE(SUM(Sales[Profit]), SUM(Sales[Sales]))

Loss Making Products =
CALCULATE(
    COUNTROWS(Sales),
    Sales[Profit] < 0
)

Discount Impact =
SUMX(
    Sales,
    Sales[Sales] * Sales[Discount]
)
```

#### Slicers
- Sub-Category (multi-select)
- Discount Band (0–10%, 10–20%, 20–30%, 30%+)
- Ship Mode

---

### PAGE 3 — Regional & Time Intelligence

**Purpose:** Sales ops & territory management

#### Visuals
- **Filled Map** — Profit Margin by State (Red = loss, Green = profit)
- **Heatmap Matrix** — Year × Quarter Sales (conditional formatting)
- **Line Chart** — Regional Sales Trend (4 lines, one per region)
- **Stacked Bar** — Ship Mode breakdown by Region
- **Table** — Bottom 10 States by Profit (with conditional formatting)

#### Time Intelligence DAX
```dax
Sales PY =
CALCULATE([Total Revenue], SAMEPERIODLASTYEAR(Dates[Date]))

Sales YTD =
TOTALYTD([Total Revenue], Dates[Date])

Sales Rolling 3M =
CALCULATE(
    [Total Revenue],
    DATESINPERIOD(Dates[Date], LASTDATE(Dates[Date]), -3, MONTH)
)

QoQ Growth =
VAR current = [Total Revenue]
VAR previous = CALCULATE([Total Revenue], PREVIOUSQUARTER(Dates[Date]))
RETURN DIVIDE(current - previous, previous)
```

---

## 🗃️ Data Model

```
Dates (dim)
  └── order_date (PK)

Products (dim)
  └── product_id (PK)
  └── product_name, category, sub_category

Customers (dim)
  └── customer_id (PK)
  └── customer_name, segment

Geography (dim)
  └── state, city, region, postal_code

Orders (fact)
  └── order_id (FK → Dates, Products, Customers, Geography)
  └── sales, profit, quantity, discount, ship_mode, ship_date
```

**Relationships:** All one-to-many from dimension tables to Orders fact table.

---

## 🎨 Design Tokens

| Element | Value |
|---|---|
| Primary color | `#2563EB` (blue) |
| Profit color | `#059669` (green) |
| Loss color | `#DC2626` (red) |
| Background | `#F8FAFC` |
| Card background | `#FFFFFF` |
| Font | Segoe UI (Power BI default) |
| Border radius | 8px |
| Shadow | Subtle drop shadow on cards |

---

## ✅ Power BI Checklist

- [ ] Import CSV → Transform in Power Query
- [ ] Create Date dimension table (CALENDARAUTO)
- [ ] Build all DAX measures in a dedicated Measures table
- [ ] Enable row-level security (RLS) by Region
- [ ] Add tooltips on all visuals
- [ ] Mobile layout configured for Pages 1 & 2
- [ ] Publish to Power BI Service
- [ ] Schedule daily refresh
- [ ] Share dashboard link with stakeholders
