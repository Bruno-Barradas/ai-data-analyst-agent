import os
import sys
import json
from datetime import datetime

import pandas as pd
import streamlit as st

# Adiciona src/ ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from data_loader import load_and_clean, get_summary
from analyzer import (
    descriptive_stats,
    correlation_analysis,
    outlier_detection,
    top_categories,
    time_series_insights,
)
from visualizer import generate_all

# ==============================
# PAGE CONFIG
# ==============================
st.set_page_config(
    page_title="AI Data Analyst Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==============================
# STYLES
# ==============================
st.markdown("""
<style>
    .main-title {
        font-size: 2.4rem;
        font-weight: 800;
        margin-bottom: 0.3rem;
    }
    .subtext {
        font-size: 1rem;
        color: #94a3b8;
        margin-bottom: 1.4rem;
    }
    .kpi-card {
        background: #0f172a;
        color: white;
        padding: 1rem;
        border-radius: 14px;
        text-align: center;
        box-shadow: 0 4px 16px rgba(0,0,0,0.12);
    }
    .section-title {
        font-size: 1.2rem;
        font-weight: 700;
        margin-top: 1.2rem;
        margin-bottom: 0.6rem;
    }
</style>
""", unsafe_allow_html=True)

# ==============================
# HELPERS
# ==============================
def safe_json(data):
    try:
        return json.dumps(data, indent=2, ensure_ascii=False, default=str)
    except Exception:
        return str(data)

def format_summary(summary: dict):
    rows, cols = summary["shape"]
    missing_total = sum(summary["missing_values"].values()) if summary["missing_values"] else 0
    return rows, cols, missing_total

def save_uploaded_file(uploaded_file, output_path="temp_uploaded.csv"):
    with open(output_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return output_path

def render_chart_if_exists(path: str, caption: str):
    if os.path.exists(path):
        st.image(path, caption=caption, use_container_width=True)

# ==============================
# SIDEBAR
# ==============================
with st.sidebar:
    st.markdown("## 🤖 AI Data Analyst Agent")
    st.markdown("Automated EDA, insights and business analysis.")
    st.markdown("---")
    st.markdown("### How to use")
    st.markdown("1. Upload a CSV")
    st.markdown("2. Review the dataset preview")
    st.markdown("3. Explore automated analysis")
    st.markdown("4. Review visual outputs")
    st.markdown("---")
    use_sample = st.checkbox("Use sample dataset from /data", value=True)

# ==============================
# HEADER
# ==============================
st.markdown('<div class="main-title">AI Data Analyst Agent</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtext">Automated EDA, insights & business analysis with AI-style workflow</div>',
    unsafe_allow_html=True
)

# ==============================
# DATA INPUT
# ==============================
sample_candidates = [
    "data/sample_dataset.csv",
    "data/revolut_reviews_clean_with_sentiment.csv",
]

sample_path = None
for candidate in sample_candidates:
    if os.path.exists(candidate):
        sample_path = candidate
        break

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

filepath = None
data_source_label = None

if uploaded_file is not None:
    filepath = save_uploaded_file(uploaded_file)
    data_source_label = f"Uploaded file: {uploaded_file.name}"
elif use_sample and sample_path is not None:
    filepath = sample_path
    data_source_label = f"Sample dataset: {os.path.basename(sample_path)}"

if filepath is None:
    st.info("Upload a CSV or keep the sample dataset option enabled.")
    st.stop()

# ==============================
# LOAD DATA
# ==============================
df = load_and_clean(filepath)
summary = get_summary(df)
rows, cols, missing_total = format_summary(summary)

st.caption(data_source_label)

# ==============================
# KPIS
# ==============================
k1, k2, k3 = st.columns(3)
with k1:
    st.markdown(f'<div class="kpi-card"><h3>{rows:,}</h3><p>Rows</p></div>', unsafe_allow_html=True)
with k2:
    st.markdown(f'<div class="kpi-card"><h3>{cols}</h3><p>Columns</p></div>', unsafe_allow_html=True)
with k3:
    st.markdown(f'<div class="kpi-card"><h3>{missing_total:,}</h3><p>Missing Values</p></div>', unsafe_allow_html=True)

# ==============================
# DATASET PREVIEW
# ==============================
st.markdown('<div class="section-title">Dataset Overview</div>', unsafe_allow_html=True)
st.dataframe(df.head(10), use_container_width=True)

with st.expander("Show dataset structure"):
    st.write("Columns:", df.columns.tolist())
    st.write("Dtypes:")
    st.json(summary["dtypes"])

# ==============================
# ANALYSIS
# ==============================
st.markdown('<div class="section-title">Automated Analysis</div>', unsafe_allow_html=True)

stats = descriptive_stats(df)
correlations = correlation_analysis(df)
outliers = outlier_detection(df)
categories = top_categories(df)
time_insights = time_series_insights(df)

tab1, tab2, tab3, tab4 = st.tabs([
    "Descriptive Stats",
    "Correlations",
    "Outliers",
    "Categories / Time"
])

with tab1:
    st.json(stats)

with tab2:
    if correlations:
        st.json(correlations)
    else:
        st.info("Not enough numeric columns for correlation analysis.")

with tab3:
    if outliers:
        st.json(outliers)
    else:
        st.success("No outliers detected by the current IQR rule.")

with tab4:
    col_a, col_b = st.columns(2)
    with col_a:
        if categories:
            st.subheader("Top Categories")
            st.json(categories)
        else:
            st.info("No categorical columns detected.")
    with col_b:
        if time_insights:
            st.subheader("Time Insights")
            st.json(time_insights)
        else:
            st.info("No time-series insight available.")

# ==============================
# VISUALS
# ==============================
st.markdown('<div class="section-title">Visual Insights</div>', unsafe_allow_html=True)

generated_paths = generate_all(df, output_dir="visuals")

img_cols = st.columns(2)
for i, path in enumerate(generated_paths):
    with img_cols[i % 2]:
        if os.path.exists(path):
            st.image(path, caption=os.path.basename(path), use_container_width=True)

# ==============================
# REPORT SUMMARY
# ==============================
st.markdown('<div class="section-title">Business Summary</div>', unsafe_allow_html=True)

summary_text = {
    "dataset_info": summary,
    "top_correlations": correlations.get("top_correlations", [])[:3] if correlations else [],
    "outliers": outliers,
    "time_trends": time_insights,
}

st.code(safe_json(summary_text), language="json")

# ==============================
# DOWNLOAD
# ==============================
report_content = f"""# AI Data Analyst Agent Report

Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Source: {data_source_label}

## Dataset Summary
{safe_json(summary)}

## Top Correlations
{safe_json(correlations)}

## Outliers
{safe_json(outliers)}

## Categories
{safe_json(categories)}

## Time Insights
{safe_json(time_insights)}
"""

st.download_button(
    label="Download Report (.md)",
    data=report_content,
    file_name="ai_data_analyst_report.md",
    mime="text/markdown",
)

st.success("Analysis complete.")