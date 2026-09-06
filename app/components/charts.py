"""
Plotly Chart Generators for MatGraph Extractor Dashboard and Analytics.
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from typing import List, Dict, Any

THEME_COLORS = px.colors.qualitative.Prism

def plot_property_frequency(df_properties: pd.DataFrame, top_n: int = 10):
    """Bar chart of the most frequently extracted material properties."""
    counts = df_properties["property_name"].value_counts().reset_index()
    counts.columns = ["Property", "Count"]
    counts = counts.head(top_n)

    fig = px.bar(
        counts,
        x="Count",
        y="Property",
        orientation="h",
        color="Count",
        color_continuous_scale="Viridis",
        title=f"Top {top_n} Most Extracted Material Properties",
        text="Count"
    )
    fig.update_layout(
        yaxis=dict(autorange="reversed"),
        xaxis_title="Number of Extractions",
        yaxis_title="Property Name",
        height=400,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    return fig

def plot_component_frequency(df_compositions: pd.DataFrame, top_n: int = 12):
    """Bar chart of most common chemical elements/oxides."""
    counts = df_compositions["component"].value_counts().reset_index()
    counts.columns = ["Chemical Component", "Occurrences"]
    counts = counts.head(top_n)

    fig = px.bar(
        counts,
        x="Chemical Component",
        y="Occurrences",
        color="Occurrences",
        color_continuous_scale="Plasma",
        title=f"Top {top_n} Discovered Chemical Elements & Oxides",
        text="Occurrences"
    )
    fig.update_layout(
        xaxis_title="Component Formula",
        yaxis_title="Frequency in Tables",
        height=400,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    return fig

def plot_category_distribution(df_properties: pd.DataFrame):
    """Donut chart for property category distribution."""
    counts = df_properties["property_category"].value_counts().reset_index()
    counts.columns = ["Category", "Count"]

    fig = px.pie(
        counts,
        names="Category",
        values="Count",
        hole=0.45,
        color_discrete_sequence=px.colors.qualitative.Safe,
        title="Distribution of Material Property Categories"
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(
        height=380,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    return fig

def plot_per_paper_metrics(per_paper_df: pd.DataFrame):
    """Grouped bar chart for tables, materials, and properties per paper."""
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=per_paper_df["Paper ID"],
        y=per_paper_df["Unique Materials"],
        name="Materials",
        marker_color="#2b5c8f"
    ))
    fig.add_trace(go.Bar(
        x=per_paper_df["Paper ID"],
        y=per_paper_df["Composition Records"],
        name="Compositions",
        marker_color="#00a86b"
    ))
    fig.add_trace(go.Bar(
        x=per_paper_df["Paper ID"],
        y=per_paper_df["Property Records"],
        name="Properties",
        marker_color="#e67e22"
    ))

    fig.update_layout(
        barmode='group',
        title="Extracted Knowledge Entities per Scientific Paper",
        xaxis_title="Scientific Paper",
        yaxis_title="Entity Count",
        xaxis_tickangle=-45,
        height=450,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=20, r=20, t=40, b=100)
    )
    return fig
