# 🇵🇭 FY 2026 GAA Budget Dashboard

A production-ready Streamlit dashboard for analyzing the Philippines' **FY 2026 General Appropriations Act** national budget dataset.

Built during the **KIRO Data Engineering & Data Science Workshop**.

## 📊 Dashboard Features

| Section | Description |
|---|---|
| 📊 Top 10 Departments | Horizontal bar chart of highest budget allocations |
| 🍩 Budget Composition | Donut chart of expense categories (MOOE, PS, CO) |
| 🗺️ Regional Allocation | Geographic spending concentration by region |
| 💰 Special Funds | National Tax Allotment, Debt Payments, BARMM, etc. |
| 🧠 Macro Insights | Fiscal polarization & structural bottleneck analysis |

## 🚀 Run Locally

```bash
git clone https://github.com/CardinalSeen/fy2026-gaa-dashboard.git
cd fy2026-gaa-dashboard
pip install -r requirements.txt
streamlit run dashboard.py
```

## 🗂️ Data Files

| File | Size | Description |
|---|---|---|
| `optimized_gaa_2026.parquet` | 10.5 MB | Full cleaned dataset (736,847 rows) |
| `summary_top10_departments.parquet` | ~4 KB | Pre-aggregated Top 10 summary |

> The raw `FY2026_GAA.xlsx` (62 MB) and `cleaned_gaa_2026.csv` (232 MB) are excluded via `.gitignore` due to GitHub file size limits.

## 🛠️ Tech Stack

- **Python 3.12**
- **Pandas** — data wrangling & aggregation
- **Matplotlib / Seaborn** — corporate-grade visualizations
- **PyArrow** — Parquet I/O for fast load times
- **Streamlit** — dashboard framework

## 📐 Data Engineering Pipeline

1. Drop grand total summary rows
2. Clean float-type budget codes (`FUNDCD`, `UACS_EXP_CD`, `UACS_OBJ_CD`)
3. Fill sparse operational columns with `'Not Applicable'`
4. Standardize text columns (`.strip().upper()`)
5. Downcast dtypes → 67.5% RAM reduction (548 MB → 178 MB)
6. Convert to Parquet + Snappy → 95.4% file size reduction

---
*KIRO Workshop · 2026*
