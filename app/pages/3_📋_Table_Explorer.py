"""
Table Explorer Page: Interactive inspection of Raw vs Cleaned tables, captions, footnotes, and dimensions.
"""

import streamlit as st
import os
import sys
import pandas as pd
import json

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.dirname(CURRENT_DIR)
sys.path.insert(0, APP_DIR)

from components.db_utils import get_all_papers, query_df

st.set_page_config(page_title="Table Explorer | MatGraph Extractor", page_icon="📋", layout="wide")

st.title("📋 Scientific Table Explorer")
st.caption("Deep-dive inspection comparing Raw vs Preprocessed tables, captions, spans, and notes.")

papers_df = get_all_papers()
if papers_df.empty:
    st.warning("No papers available.")
    st.stop()

col_sel1, col_sel2 = st.columns([1, 1])

with col_sel1:
    selected_paper = st.selectbox("Select Paper:", papers_df["paper_id"].tolist())

tables_df = query_df("SELECT * FROM tables WHERE paper_id = ? ORDER BY table_id;", (selected_paper,))
if tables_df.empty:
    st.info("No tables for this paper.")
    st.stop()

with col_sel2:
    table_options = tables_df["table_id"].tolist()
    selected_table_id = st.selectbox("Select Table:", table_options, format_func=lambda x: f"{x} — {tables_df[tables_df['table_id']==x]['caption'].values[0][:50]}...")

tbl = tables_df[tables_df["table_id"] == selected_table_id].iloc[0]

# Display Table Metadata
st.markdown(f"### 📌 {tbl['table_id']}: {tbl['caption'] or 'Untitled'}")
if tbl["footnote"]:
    st.info(f"📝 **Table Footnote / Conditions:** {tbl['footnote']}")

# Metrics
c_m1, c_m2, c_m3 = st.columns(3)
with c_m1:
    st.metric("Total Rows", tbl["num_rows"])
with c_m2:
    st.metric("Total Columns", tbl["num_cols"])
with c_m3:
    st.metric("Paper DOI", tbl["paper_id"])

# Tabs for Cleaned Table, Raw Table, and Extracted Entities
tab1, tab2, tab3 = st.tabs(["✨ Cleaned Table", "🔍 Raw Extracted Table", "🧬 Extracted Knowledge Entities"])

with tab1:
    cleaned_rows = json.loads(tbl["cleaned_data_json"])
    df_cleaned = pd.DataFrame(cleaned_rows)
    st.dataframe(df_cleaned, use_container_width=True, hide_index=True)
    
    # Download Button
    st.download_button(
        label="📥 Download Cleaned CSV",
        data=df_cleaned.to_csv(index=False).encode('utf-8'),
        file_name=f"{selected_paper}_{selected_table_id}_cleaned.csv",
        mime="text/csv"
    )

with tab2:
    raw_rows = json.loads(tbl["raw_data_json"])
    df_raw = pd.DataFrame(raw_rows)
    st.dataframe(df_raw, use_container_width=True, hide_index=True)

with tab3:
    col_e1, col_e2 = st.columns(2)
    with col_e1:
        st.markdown("#### 🧪 Composition Extractions")
        df_comp = query_df("SELECT material_name, component, percentage, unit FROM compositions WHERE paper_id = ? AND table_id = ?;", (selected_paper, selected_table_id))
        if not df_comp.empty:
            st.dataframe(df_comp, use_container_width=True, hide_index=True)
        else:
            st.caption("No composition records directly mapped to this table.")

    with col_e2:
        st.markdown("#### ⚙️ Property Extractions")
        df_prop = query_df("SELECT material_name, property_name, value_raw, unit FROM properties WHERE paper_id = ? AND table_id = ?;", (selected_paper, selected_table_id))
        if not df_prop.empty:
            st.dataframe(df_prop, use_container_width=True, hide_index=True)
        else:
            st.caption("No property measurements directly mapped to this table.")
