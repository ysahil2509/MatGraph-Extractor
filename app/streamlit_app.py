"""
MatGraph Extractor: AI-Driven Material Knowledge Mining from Scientific Tables
Main Streamlit Application Entry Point.
"""

import streamlit as st
import os
import sys

# Ensure root paths are accessible
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
sys.path.insert(0, CURRENT_DIR)
sys.path.insert(0, os.path.join(CURRENT_DIR, "components"))
sys.path.insert(0, PROJECT_ROOT)

from components.db_utils import get_dashboard_counts, search_knowledge

st.set_page_config(
    page_title="MatGraph Extractor | Materials Knowledge Mining",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for academic / modern dark-mode aesthetic
st.markdown("""
<style>
    .main-title {
        font-size: 2.3rem;
        font-weight: 800;
        color: #1e3d59;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1.1rem;
        color: #555555;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 18px;
        border-radius: 10px;
        border-left: 5px solid #2b5c8f;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .tag-badge {
        background-color: #e3f2fd;
        color: #0d47a1;
        padding: 4px 8px;
        border-radius: 4px;
        font-weight: 600;
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar System Health & Navigation
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/atom--v1.png", width=64)
    st.markdown("### **MatGraph Extractor**")
    st.caption("AI-Driven Material Knowledge Mining from Scientific Tables")
    st.markdown("---")
    
    try:
        counts = get_dashboard_counts()
        st.success("🟢 SQLite Database Connected")
        st.caption(f"**{counts['papers']}** Papers | **{counts['tables']}** Tables | **{counts['materials']}** Materials")
    except Exception as e:
        st.warning("⚠️ Database Needs Initialization")
        st.caption("Run the Processing Pipeline page to initialize.")

    st.markdown("---")
    st.markdown("👨‍🎓 **Project 4 Team**")
    st.caption("• **Sahil** (Lead / Preprocessing / Tables)")
    st.caption("• **Harshdeep** (Composition NLP)")
    st.caption("• **Ayush** (Property & Relation Linking)")
    st.caption("• **Nitin** (Database, Graph & Streamlit UI)")
    st.markdown("---")
    st.caption("B.Tech CSE - 6th Semester Capstone")

# Main Page Header
st.markdown('<div class="main-title">🔬 MatGraph Extractor</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">AI-Driven Material Knowledge Mining and Relation Extraction from Scientific Tables (MatSKRAFT Framework)</div>', unsafe_allow_html=True)

# Quick Overview Cards
try:
    counts = get_dashboard_counts()
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    with c1:
        st.metric("Research Papers", counts["papers"])
    with c2:
        st.metric("Extracted Tables", counts["tables"])
    with c3:
        st.metric("Unique Materials", counts["materials"])
    with c4:
        st.metric("Composition Entries", counts["compositions"])
    with c5:
        st.metric("Property Records", counts["properties"])
    with c6:
        st.metric("Linked Triples", counts["triples"])
except Exception as e:
    st.info("💡 Please execute `scripts/process_papers.py` or go to the **Processing Pipeline** page to extract knowledge.")

st.markdown("---")

# Quick Global Search Feature
st.markdown("### 🔍 Global Material Knowledge Search")
col_s1, col_s2 = st.columns([3, 1])
with col_s1:
    search_term = st.text_input("Search material formula, alloy name, chemical component, or DOI...", placeholder="e.g. Ti-6Al-4V, LiFePO4, BaTiO3, SiO2, Cantor, Hardness, Density")
with col_s2:
    prop_opt = st.selectbox("Filter Property", ["All", "Yield Strength", "Vickers Hardness", "Density", "Dielectric Constant", "Specific Capacity", "Critical Temp Tc", "Thermal Conductivity"])

if search_term or prop_opt != "All":
    p_filter = "" if prop_opt == "All" else prop_opt
    results_df = search_knowledge(keyword=search_term, property_filter=p_filter)
    st.markdown(f"**Found {len(results_df)} matching knowledge records:**")
    if not results_df.empty:
        st.dataframe(
            results_df[["material_name", "composition_summary", "property_name", "value_raw", "unit", "paper_id", "doi"]],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.warning("No records matched your search query.")

st.markdown("---")

# Architecture and Workflow Section
st.markdown("### 🏗️ MatSKRAFT Pipeline Architecture")
c_arch1, c_arch2 = st.columns([1.2, 0.8])

with c_arch1:
    st.markdown("""
    The **MatGraph Extractor** is built upon the peer-reviewed **MatSKRAFT** materials informatics methodology.
    It overcomes the barrier of unstructured tabular literature by transforming scientific XML research papers into an interconnected knowledge base:

    1. **Paper & XML Ingestion**: Parses standard Elsevier/JATS XML documents preserving document hierarchy and metadata.
    2. **MIT Table Extraction**: Traverses XML table nodes, normalizing cell spans (`morerows`, `namest`, `nameend`), headers, captions, and footnotes.
    3. **Domain Preprocessing**: Preserves chemical notation ($SiO_2, Al_2O_3, Ti-6Al-4V$), superscripts, subscripts, and scientific exponents ($10^{-3}$).
    4. **Composition Mining**: Extracts elemental/oxide mass, atomic, and molar fractions ($wt\%, at\%, mol\%$).
    5. **Property & Unit Normalization**: Standardizes mechanical, electrical, thermal, and optical properties with canonical units ($MPa, GPa, g/cm^3, W/m\cdot K$).
    6. **Knowledge Linking & Graph Storage**: Unifies compositions with experimental properties in SQLite and interactive NetworkX knowledge graphs.
    """)

with c_arch2:
    st.info("""
    **🚀 How to Navigate this Platform:**
    
    * **📊 Dashboard**: High-level metrics, summary charts, and top distributions.
    * **📄 Paper Explorer**: Inspect individual XML papers, titles, and abstracts.
    * **📋 Table Explorer**: Compare raw extracted tables with cleaned DataFrames.
    * **🔬 Material Explorer**: Deep-dive into specific materials and alloy chemistries.
    * **🕸️ Knowledge Graph**: Interactive multi-relational graph visualization.
    * **📈 Analytics**: In-depth statistical and quality validation reports.
    * **⚙️ Processing Pipeline**: Ingest new XML papers and trigger live extraction.
    * **👥 Team & Project Info**: Project 4 evaluation deliverables and student division table.
    """)
