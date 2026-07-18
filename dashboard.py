"""
FY 2026 GAA — Production-Ready Streamlit Dashboard
Data Science Workshop | KIRO
Reads from optimized_gaa_2026.parquet (10.5 MB) — no CSV needed.
"""

import streamlit as st
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.patches as mpatches
import warnings
warnings.filterwarnings('ignore')

# ── Page Config ────────────────────────────────────────────────────
st.set_page_config(
    page_title="FY 2026 GAA Budget Dashboard",
    page_icon="🇵🇭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Corporate Style Constants ──────────────────────────────────────
BG_COLOR    = '#F7F9FC'
PANEL_COLOR = '#FFFFFF'
TEXT_DARK   = '#1A1A2E'
TEXT_MID    = '#4A4A6A'
ACCENT      = '#C9A84C'

NAVY_PALETTE = [
    '#0D2137','#123456','#1B4F72','#21618C',
    '#2E86C1','#3498DB','#5DADE2','#85C1E9',
    '#AED6F1','#D6EAF8'
]
TEAL_PALETTE = [
    '#0A3D62','#1B6CA8','#1289A7','#12CBC4',
    '#1E90FF','#0652DD','#006266','#1B4F72',
    '#21618C','#2E86C1','#3498DB','#5DADE2'
]
DONUT_COLORS = ['#1B4F72','#2E86C1','#C9A84C','#76848F']

plt.rcParams.update({
    'font.family'       : 'DejaVu Sans',
    'axes.facecolor'    : PANEL_COLOR,
    'figure.facecolor'  : BG_COLOR,
    'axes.edgecolor'    : '#CCCCCC',
    'axes.spines.top'   : False,
    'axes.spines.right' : False,
    'axes.spines.left'  : False,
    'axes.grid'         : True,
    'grid.color'        : '#E8ECF0',
    'grid.linewidth'    : 0.6,
    'text.color'        : TEXT_DARK,
    'xtick.color'       : TEXT_MID,
    'ytick.color'       : TEXT_DARK,
    'font.size'         : 10,
})

# ── Data Loader ────────────────────────────────────────────────────
@st.cache_data(show_spinner="Loading FY 2026 GAA dataset...")
def load_data():
    df = pd.read_parquet('optimized_gaa_2026.parquet')
    return df

df = load_data()
grand_total_b = df['AMT'].sum() / 1e9

# ── Label Maps (module-level so charts can reference them) ─────────
DEPT_LABEL_MAP = {
    'AUTOMATIC APPROPRIATIONS'                                   : 'Automatic Appropriations',
    'DEPARTMENT OF EDUCATION (DEPED)'                           : 'DepEd',
    'DEPARTMENT OF PUBLIC WORKS AND HIGHWAYS (DPWH)'            : 'DPWH',
    'NEW GENERAL APPROPRIATIONS'                                 : 'New General Appropriations',
    'DEPARTMENT OF THE INTERIOR AND LOCAL GOVERNMENT (DILG)'    : 'DILG',
    'DEPARTMENT OF NATIONAL DEFENSE (DND)'                      : 'DND',
    'DEPARTMENT OF HEALTH (DOH)'                                : 'DOH',
    'BUDGETARY SUPPORT TO GOVERNMENT CORPORATIONS (BSGC)'       : 'BSGC',
    'DEPARTMENT OF SOCIAL WELFARE AND DEVELOPMENT (DSWD)'       : 'DSWD',
    'DEPARTMENT OF AGRICULTURE (DA)'                            : 'DA',
}
EXP_LABEL_MAP = {
    'MAINTENANCE AND OTHER OPERATING EXPENSES': 'MOOE',
    'PERSONNEL SERVICES'                       : 'Personnel Services',
    'CAPITAL OUTLAYS'                          : 'Capital Outlays',
    'FINANCIAL EXPENSES'                       : 'Financial Expenses',
}
REGION_MAP = {
    1.0 : 'Region I (Ilocos)',           2.0 : 'Region II (Cagayan Valley)',
    3.0 : 'Region III (Central Luzon)',  4.0 : 'Region IV (CALABARZON)',
    5.0 : 'Region V (Bicol)',            6.0 : 'Region VI (Western Visayas)',
    7.0 : 'Region VII (Central Visayas)',8.0 : 'Region VIII (Eastern Visayas)',
    9.0 : 'Region IX (Zamboanga)',       10.0: 'Region X (Northern Mindanao)',
    11.0: 'Region XI (Davao)',           12.0: 'Region XII (SOCCSKSARGEN)',
    13.0: 'NCR (Metro Manila)',          14.0: 'CAR (Cordillera)',
    16.0: 'Region XIII (CARAGA)',        17.0: 'MIMAROPA',
    18.0: 'BARMM',                       19.0: 'Nationwide / Multi-Region',
    0.0 : 'National / Central Office',
}
EXCL_FUNDS = [
    'Specific Budgets of National Government Agencies',
    'Retirement and Life Insurance Premiums'
]

# ── Sidebar ────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🇵🇭 FY 2026 GAA")
    st.caption("General Appropriations Act Dashboard")
    st.divider()
    st.metric("Total National Budget", f"₱{grand_total_b:.2f}B")
    st.metric("Budget Line Items",     f"{len(df):,}")
    st.metric("Departments",           f"{df['UACS_DPT_DSC'].nunique()}")
    st.metric("Agencies",              f"{df['UACS_AGY_DSC'].nunique()}")
    st.divider()
    st.markdown("**Navigation**")
    section = st.radio("Jump to section:", [
        "📊 Top 10 Departments",
        "🍩 Budget Composition",
        "🗺️ Regional Allocation",
        "💰 Special Funds",
        "🧠 Macro Insights",
    ])
    st.divider()
    st.caption("Data Engineering: ✅ Cleaned & Optimized")
    st.caption("Workshop · KIRO · 2026")

# ── Header ─────────────────────────────────────────────────────────
st.markdown("""
<h1 style='color:#1A1A2E;margin-bottom:0'>
    🇵🇭 FY 2026 National Budget Dashboard
</h1>
<p style='color:#4A4A6A;font-size:15px;margin-top:4px'>
    General Appropriations Act · Descriptive Analysis & Visualization
</p>
<hr style='border:1px solid #E8ECF0;margin-top:8px'>
""", unsafe_allow_html=True)

# ── KPI Row ────────────────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)
k1.metric("Grand Total Budget", f"₱{grand_total_b:.2f}B")
k2.metric("Departments",        df['UACS_DPT_DSC'].nunique())
k3.metric("Agencies",           df['UACS_AGY_DSC'].nunique())
k4.metric("Line Items",         f"{len(df):,}")
st.markdown("<hr style='border:1px solid #E8ECF0'>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# CHART 1 — Top 10 Departments
# ══════════════════════════════════════════════════════════════════
st.subheader("📊 Chart 1 — Top 10 Departments by Budget Allocation")
st.info(
    "**Executive Insight:** Automatic Appropriations (₱2.28B) and DepEd (₱1.02B) jointly absorb "
    "49.4% of the entire ₱6.79B national budget — a structural commitment to debt servicing and "
    "universal education that leaves all other agencies sharing the remaining half. DPWH's ₱0.53B "
    "third-place ranking signals a continued infrastructure push, but the steep drop-off after "
    "the top two reveals severe fiscal compression across mid-tier agencies."
)

@st.cache_data
def build_chart1(_df):
    top10 = (
        _df.groupby('UACS_DPT_DSC', observed=True)['AMT']
        .sum().sort_values(ascending=False).head(10).reset_index()
    )
    top10.columns = ['DEPARTMENT', 'TOTAL_AMT']
    top10['TOTAL_B'] = top10['TOTAL_AMT'] / 1e9
    top10['LABEL'] = top10['DEPARTMENT'].map(DEPT_LABEL_MAP).fillna(top10['DEPARTMENT'])
    top10 = top10.sort_values('TOTAL_B', ascending=True)

    fig, ax = plt.subplots(figsize=(11, 6.5))
    fig.patch.set_facecolor(BG_COLOR)
    ax.set_facecolor(PANEL_COLOR)
    bars = ax.barh(top10['LABEL'], top10['TOTAL_B'],
                   color=NAVY_PALETTE[::-1][:10], height=0.65, edgecolor='none')
    bars[-1].set_color(ACCENT)

    for bar, val in zip(bars, top10['TOTAL_B']):
        ax.text(bar.get_width() + 0.02, bar.get_y() + bar.get_height() / 2,
                f'₱{val:.2f}B', va='center', ha='left',
                fontsize=9.5, fontweight='bold', color=TEXT_DARK)

    ax.set_xlabel('Total Budget Allocation (₱ Billions)', fontsize=10,
                  color=TEXT_MID, labelpad=8)
    ax.set_title(
        'Top 10 Departments by Budget Allocation\nFY 2026 General Appropriations Act',
        fontsize=14, fontweight='bold', color=TEXT_DARK, pad=15, loc='left'
    )
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'₱{x:.0f}B'))
    ax.set_xlim(0, top10['TOTAL_B'].max() * 1.22)
    ax.tick_params(axis='y', labelsize=9.5)
    ax.tick_params(axis='x', labelsize=9)
    ax.spines['bottom'].set_color('#CCCCCC')
    fig.text(0.98, 0.02, f'Grand Total: ₱{_df["AMT"].sum()/1e9:.2f}B',
             ha='right', va='bottom', fontsize=8.5, color=TEXT_MID, style='italic')
    plt.tight_layout()
    return fig

st.pyplot(build_chart1(df), use_container_width=True)
st.divider()

# ══════════════════════════════════════════════════════════════════
# CHART 2 — Budget Composition Donut
# ══════════════════════════════════════════════════════════════════
st.subheader("🍩 Chart 2 — National Budget Composition by Expense Category")
st.info(
    "**Executive Insight:** MOOE dominates the expense composition, reflecting the heavy "
    "operational burden of sustaining government service delivery at scale. Personnel Services "
    "ranks second — confirming that public workforce costs are the second largest structural "
    "commitment, directly limiting the share available for Capital Outlays and long-term "
    "productive investment."
)

@st.cache_data
def build_chart2(_df):
    exp_data = (
        _df[_df['UACS_EXP_DSC'].notna()]
        .groupby('UACS_EXP_DSC', observed=True)['AMT']
        .sum().sort_values(ascending=False).reset_index()
    )
    exp_data.columns = ['CATEGORY', 'TOTAL']
    exp_data['SHORT'] = exp_data['CATEGORY'].map(EXP_LABEL_MAP).fillna(exp_data['CATEGORY'])
    total_b = exp_data['TOTAL'].sum() / 1e9

    fig, ax = plt.subplots(figsize=(9, 7))
    fig.patch.set_facecolor(BG_COLOR)
    ax.set_facecolor(BG_COLOR)

    ax.pie(
        exp_data['TOTAL'], labels=None, autopct='%1.1f%%',
        startangle=90, colors=DONUT_COLORS,
        wedgeprops=dict(width=0.5, edgecolor='white', linewidth=2.5),
        pctdistance=0.78,
        textprops={'fontsize': 10.5, 'fontweight': 'bold', 'color': 'white'}
    )
    ax.text(0,  0.08, 'Grand Total',       ha='center', fontsize=10, color=TEXT_MID)
    ax.text(0, -0.18, f'₱{total_b:.2f}B',  ha='center', fontsize=18,
            fontweight='bold', color=TEXT_DARK)

    patches = [mpatches.Patch(color=DONUT_COLORS[i],
               label=f"{row['SHORT']}  —  ₱{row['TOTAL']/1e9:.2f}B")
               for i, (_, row) in enumerate(exp_data.iterrows())]
    ax.legend(handles=patches, loc='lower center', bbox_to_anchor=(0.5, -0.12),
              ncol=2, frameon=False, fontsize=9.5, labelcolor=TEXT_DARK)
    ax.set_title(
        'National Budget Composition by Expense Category\nFY 2026 GAA',
        fontsize=14, fontweight='bold', color=TEXT_DARK, pad=18
    )
    plt.tight_layout()
    return fig, exp_data

fig2, exp_data = build_chart2(df)
col_a, col_b = st.columns([1.2, 1])
with col_a:
    st.pyplot(fig2, use_container_width=True)
with col_b:
    st.markdown("#### Expense Category Breakdown")
    tbl = exp_data.copy()
    tbl['Short Name']  = tbl['CATEGORY'].map(EXP_LABEL_MAP).fillna(tbl['CATEGORY'])
    tbl['Total (₱B)']  = (tbl['TOTAL'] / 1e9).round(3)
    tbl['Share (%)']   = (tbl['TOTAL'] / tbl['TOTAL'].sum() * 100).round(1)
    st.dataframe(tbl[['Short Name','Total (₱B)','Share (%)']].reset_index(drop=True),
                 use_container_width=True, hide_index=True)
st.divider()

# ══════════════════════════════════════════════════════════════════
# CHART 3 — Regional Allocation
# ══════════════════════════════════════════════════════════════════
st.subheader("🗺️ Chart 3 — Regional Budget Allocation Distribution")
st.info(
    "**Executive Insight:** NCR alone commands ₱2.63B (38.7% of the total budget), while the "
    "combined 17 provincial regions receive roughly 36% — a spatial imbalance that entrenches "
    "Metro Manila's centrality in public service delivery. CARAGA (₱0.11B) and CAR (₱0.09B) "
    "sit at the bottom, raising structural equity questions about regional development commitments."
)

@st.cache_data
def build_chart3(_df):
    reg = (
        _df.groupby('UACS_REG_ID')['AMT']
        .sum().reset_index()
        .rename(columns={'UACS_REG_ID': 'REG_ID', 'AMT': 'TOTAL'})
    )
    reg['REGION']  = reg['REG_ID'].map(REGION_MAP).fillna(reg['REG_ID'].astype(str))
    reg['TOTAL_B'] = reg['TOTAL'] / 1e9
    reg = reg.sort_values('TOTAL_B', ascending=True)

    bar_colors = []
    for _, row in reg.iterrows():
        if 'NCR' in str(row['REGION']):        bar_colors.append(ACCENT)
        elif 'National' in str(row['REGION']): bar_colors.append('#0D2137')
        else:                                  bar_colors.append('#2E86C1')

    fig, ax = plt.subplots(figsize=(11, 8))
    fig.patch.set_facecolor(BG_COLOR)
    ax.set_facecolor(PANEL_COLOR)
    bars = ax.barh(reg['REGION'], reg['TOTAL_B'],
                   color=bar_colors, height=0.65, edgecolor='none')

    for bar, val in zip(bars, reg['TOTAL_B']):
        ax.text(bar.get_width() + 0.02, bar.get_y() + bar.get_height() / 2,
                f'₱{val:.2f}B', va='center', ha='left',
                fontsize=8.5, fontweight='bold', color=TEXT_DARK)

    ax.set_xlabel('Total Budget Allocation (₱ Billions)', fontsize=10,
                  color=TEXT_MID, labelpad=8)
    ax.set_title(
        'Regional Budget Allocation Distribution\nFY 2026 General Appropriations Act',
        fontsize=14, fontweight='bold', color=TEXT_DARK, pad=15, loc='left'
    )
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'₱{x:.0f}B'))
    ax.set_xlim(0, reg['TOTAL_B'].max() * 1.22)
    ax.tick_params(axis='y', labelsize=8.5)
    ax.spines['bottom'].set_color('#CCCCCC')
    legend3 = [
        mpatches.Patch(color=ACCENT,    label='NCR (Metro Manila)'),
        mpatches.Patch(color='#0D2137', label='National / Central Office'),
        mpatches.Patch(color='#2E86C1', label='Provincial Regions'),
    ]
    ax.legend(handles=legend3, loc='lower right', frameon=False, fontsize=9)
    plt.tight_layout()
    return fig

st.pyplot(build_chart3(df), use_container_width=True)
st.divider()

# ══════════════════════════════════════════════════════════════════
# CHART 4 — Special Funds
# ══════════════════════════════════════════════════════════════════
st.subheader("💰 Chart 4 — Special Funds & Unprogrammed Allocations")
st.info(
    "**Executive Insight:** The National Tax Allotment (₱1.19B) and Debt Interest Payments "
    "(₱0.95B) together represent ₱2.14B in mandatory fiscal obligations that bypass agency-level "
    "budget control. The Pension and Gratuity Fund (₱0.17B) and BARMM's (₱0.10B) earmarked "
    "allocations further signal that 'flexible' appropriations are in practice largely pre-committed, "
    "narrowing the government's room for discretionary reallocation."
)

@st.cache_data
def build_chart4(_df):
    special = _df[
        _df['UACS_FUNDSUBCAT_DSC'].notna() &
        ~_df['UACS_FUNDSUBCAT_DSC'].isin(EXCL_FUNDS)
    ]
    sp_agg = (
        special.groupby('UACS_FUNDSUBCAT_DSC', observed=True)['AMT']
        .sum().sort_values(ascending=False).head(12).reset_index()
    )
    sp_agg.columns = ['FUND', 'TOTAL']
    sp_agg['TOTAL_B']    = sp_agg['TOTAL'] / 1e9
    sp_agg['FUND_SHORT'] = sp_agg['FUND'].str[:55]
    sp_agg = sp_agg.sort_values('TOTAL_B', ascending=True)

    fig, ax = plt.subplots(figsize=(11, 7))
    fig.patch.set_facecolor(BG_COLOR)
    ax.set_facecolor(PANEL_COLOR)
    ax.barh(sp_agg['FUND_SHORT'], sp_agg['TOTAL_B'],
            color=TEAL_PALETTE[:len(sp_agg)], height=0.65, edgecolor='none')

    for _, row in sp_agg.iterrows():
        ax.text(row['TOTAL_B'] + 0.005, sp_agg.index.get_loc(_) * 1,
                f'₱{row["TOTAL_B"]:.3f}B', va='center', ha='left',
                fontsize=8.5, fontweight='bold', color=TEXT_DARK)

    ax.set_xlabel('Total Allocation (₱ Billions)', fontsize=10, color=TEXT_MID, labelpad=8)
    ax.set_title(
        'Special Funds & Unprogrammed Allocations\nFY 2026 General Appropriations Act',
        fontsize=14, fontweight='bold', color=TEXT_DARK, pad=15, loc='left'
    )
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'₱{x:.2f}B'))
    ax.set_xlim(0, sp_agg['TOTAL_B'].max() * 1.30)
    ax.tick_params(axis='y', labelsize=8.5)
    ax.spines['bottom'].set_color('#CCCCCC')
    fig.text(0.98, 0.02, f'Special Funds Total: ₱{sp_agg["TOTAL"].sum()/1e9:.3f}B',
             ha='right', va='bottom', fontsize=8.5, color=TEXT_MID, style='italic')
    plt.tight_layout()
    return fig, sp_agg

fig4, sp_agg = build_chart4(df)
col_c, col_d = st.columns([1.3, 1])
with col_c:
    st.pyplot(fig4, use_container_width=True)
with col_d:
    st.markdown("#### Top Special Fund Categories")
    tbl4 = sp_agg[['FUND','TOTAL']].copy()
    tbl4.columns = ['Fund / Program', 'Total Amount']
    tbl4['Total (₱B)'] = (tbl4['Total Amount'] / 1e9).round(4)
    tbl4['Share (%)']  = (tbl4['Total Amount'] / tbl4['Total Amount'].sum() * 100).round(1)
    st.dataframe(tbl4[['Fund / Program','Total (₱B)','Share (%)']].reset_index(drop=True),
                 use_container_width=True, hide_index=True)
st.divider()

# ══════════════════════════════════════════════════════════════════
# SECTION 5 — Macro Insights
# ══════════════════════════════════════════════════════════════════
st.subheader("🧠 Section 5 — Inter-Agency Macro Economic Insights")

st.markdown("""
<div style='background:#1A1A2E;border-radius:12px;padding:28px 32px;margin-bottom:12px'>
    <h4 style='color:#C9A84C;margin-bottom:16px;font-size:16px'>
        📌 Fiscal Polarization Analysis — FY 2026 GAA
    </h4>
    <p style='color:#E8ECF0;font-size:14.5px;line-height:1.85;margin-bottom:12px'>
        <strong style='color:#C9A84C'>①</strong>
        The FY 2026 national budget exhibits extreme fiscal polarization:
        <strong style='color:#AED6F1'>Automatic Appropriations (₱2.28B)</strong> and
        <strong style='color:#AED6F1'>DepEd (₱1.02B)</strong> collectively consume
        <strong style='color:#C9A84C'>49.4%</strong> of the entire ₱6.79B appropriation,
        while 37+ departments divide the other half — creating a structurally top-heavy
        budget architecture that compresses operational capacity across the broader public sector.
    </p>
    <p style='color:#E8ECF0;font-size:14.5px;line-height:1.85;margin-bottom:12px'>
        <strong style='color:#C9A84C'>②</strong>
        The dominance of <strong style='color:#AED6F1'>MOOE</strong> as the largest expense
        category signals a recurring structural bottleneck: the government is allocating a
        disproportionate share of discretionary funds to sustaining existing operations rather
        than building long-term productive capital — constraining the fiscal multiplier effect
        that Capital Outlays typically generate through infrastructure and development investment.
    </p>
    <p style='color:#E8ECF0;font-size:14.5px;line-height:1.85;margin-bottom:0'>
        <strong style='color:#C9A84C'>③</strong>
        Geographic concentration data reveals that <strong style='color:#AED6F1'>NCR alone
        absorbs ₱2.63B (38.7%)</strong> while all 17 provincial regions combined receive ~36% —
        a spatial imbalance perpetuating Metro Manila-centric public service delivery, with the
        per-capita shortfall most acute in CARAGA (₱0.11B) and CAR (₱0.09B).
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("#### Fiscal Concentration — Top 5 Departments")
top5 = (
    df.groupby('UACS_DPT_DSC', observed=True)['AMT']
    .sum().sort_values(ascending=False).head(5).reset_index()
)
top5.columns = ['Department', 'Total Amount']
top5['Total (₱B)']       = (top5['Total Amount'] / 1e9).round(3)
top5['Budget Share (%)'] = (top5['Total Amount'] / df['AMT'].sum() * 100).round(1)
top5['Cumulative (%)']   = top5['Budget Share (%)'].cumsum().round(1)
st.dataframe(
    top5[['Department','Total (₱B)','Budget Share (%)','Cumulative (%)']].reset_index(drop=True),
    use_container_width=True, hide_index=True
)

st.divider()

# ── Footer ─────────────────────────────────────────────────────────
st.markdown("""
<p style='text-align:center;color:#9999AA;font-size:12px;margin-top:8px'>
    FY 2026 General Appropriations Act · Data Engineering & Visualization Workshop · KIRO · 2026<br>
    Data Source: Official GAA Expenditure Database · Optimized via Pandas & PyArrow
</p>
""", unsafe_allow_html=True)
