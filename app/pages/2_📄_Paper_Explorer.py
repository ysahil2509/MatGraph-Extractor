"""
Paper Explorer Page: Browse research papers, view abstracts, DOIs, and extracted table inventories.
"""

import streamlit as st
import os
import sys
import pandas as pd
import json

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.dirname(CURRENT_DIR)
sys.path.insert(0, APP_DIR)

from components.db_utils import get_all_papers, get_tables_for_paper, query_df

st.set_page_config(page_title="Paper Explorer | MatGraph Extractor", page_icon="📄", layout="wide")

st.title("📄 Scientific Paper Explorer")
st.caption("Inspect ingested research documents, metadata, abstracts, and table inventories.")

papers_df = get_all_papers()
if papers_df.empty:
    st.warning("No papers found in database.")
    st.stop()

# Paper Selection
paper_options = papers_df["paper_id"].tolist()
selected_paper_id = st.selectbox("Select a Research Paper:", paper_options, format_func=lambda x: f"{x} — {papers_df[papers_df['paper_id']==x]['title'].values[0][:75]}...")

paper_row = papers_df[papers_df["paper_id"] == selected_paper_id].iloc[0]

# Display Paper Details
col_meta1, col_meta2 = st.columns([2.5, 1])

with col_meta1:
    st.markdown(f"### {paper_row['title']}")
    st.markdown(f"**DOI:** [`{paper_row['doi']}`](https://doi.org/{paper_row['doi']}) | **PII:** `{paper_row['pii']}`")
    st.markdown(f"**Source File:** `{paper_row['source_file']}`")

with col_meta2:
    st.info(f"**Status:** {paper_row['status'].upper()} ✅\n\n**Format:** Elsevier / JATS XML")

st.markdown("#### 📖 Abstract")
st.write(paper_row['abstract'])

st.markdown("---")
st.subheader("📋 Extracted Tables in this Paper")

tables_df = get_tables_for_paper(selected_paper_id)
if tables_df.empty:
    st.info("No tables recorded for this paper.")
else:
    for _, tbl in tables_df.iterrows():
        with st.expander(f"📌 {tbl['table_id']}: {tbl['caption'] or 'Untitled Table'} ({tbl['num_rows']} rows × {tbl['num_cols']} cols)", expanded=True):
            if tbl["footnote"]:
                st.caption(f"**Footnote/Conditions:** {tbl['footnote']}")
            
            # Load cleaned table
            cleaned_rows = json.loads(tbl["cleaned_data_json"])
            df_cleaned = pd.DataFrame(cleaned_rows)
            st.dataframe(df_cleaned, use_container_width=True, hide_index=True)

            # Show download options
            c_d1, c_d2 = st.columns(2)
            with c_d1:
                csv_data = df_cleaned.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label=f"📥 Download {tbl['table_id']} as CSV",
                    data=csv_data,
                    file_name=f"{selected_paper_id}_{tbl['table_id']}.csv",
                    mime="text/csv",
                    key=f"dl_csv_{selected_paper_id}_{tbl['table_id']}"
                )
            with c_d2:
                json_data = json.dumps(cleaned_rows, indent=2)
                st.download_button(
                    label=f"📥 Download {tbl['table_id']} as JSON",
                    data=json_data,
                    file_name=f"{selected_paper_id}_{tbl['table_id']}.json",
                    mime="application/json",
                    key=f"dl_json_{selected_paper_id}_{tbl['table_id']}"
                )
