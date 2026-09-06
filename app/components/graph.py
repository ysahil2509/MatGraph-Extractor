"""
Knowledge Graph Construction and Plotly Interactive Graph Visualizer for MatGraph Extractor.
Builds multi-relational graphs: Paper -> Table -> Material -> Composition / Property -> Value.
"""

import networkx as nx
import plotly.graph_objects as go
import pandas as pd
from typing import List, Dict, Any, Optional

ENTITY_COLORS = {
    "paper": "#1f77b4",       # Deep Blue
    "table": "#2ca02c",       # Forest Green
    "material": "#ff7f0e",    # Amber Orange
    "component": "#17becf",   # Cyan / Teal
    "property": "#9467bd",    # Royal Purple
    "value": "#d62728"        # Crimson Red
}

def build_knowledge_graph(
    df_knowledge: pd.DataFrame,
    max_materials: int = 15,
    selected_paper: Optional[str] = None
) -> nx.DiGraph:
    """Constructs a NetworkX directed knowledge graph from linked triples."""
    G = nx.DiGraph()

    filtered = df_knowledge.copy()
    if selected_paper and selected_paper != "All Papers":
        filtered = filtered[filtered["paper_id"] == selected_paper]

    # Limit to top materials to keep the graph readable and responsive
    top_mats = filtered["material_name"].unique()[:max_materials]
    filtered = filtered[filtered["material_name"].isin(top_mats)]

    for _, row in filtered.iterrows():
        p_id = row["paper_id"]
        t_id = f"{p_id}:{row['table_id']}"
        mat = row["material_name"]
        prop = row["property_name"]
        val = f"{row['value_raw']} {row['unit']}".strip()
        comp_summary = row["composition_summary"]

        # Add Nodes with Type Attributes
        G.add_node(p_id, type="paper", label=f"📄 Paper: {p_id}", size=24)
        G.add_node(t_id, type="table", label=f"📋 Table: {row['table_id']}", size=18)
        G.add_node(mat, type="material", label=f"🔬 Material: {mat}<br>Composition: {comp_summary}", size=20)
        G.add_node(prop, type="property", label=f"⚙️ Property: {prop}", size=16)
        
        val_node = f"{mat}_{prop}_{val}"
        G.add_node(val_node, type="value", label=f"📊 Value: {val}", size=14)

        # Add Relational Edges
        G.add_edge(p_id, t_id, relation="contains_table")
        G.add_edge(t_id, mat, relation="reports_material")
        G.add_edge(mat, prop, relation="has_property")
        G.add_edge(prop, val_node, relation="measured_as")

    return G

def plot_interactive_graph(G: nx.DiGraph):
    """Renders NetworkX graph into an interactive Plotly visualization."""
    if len(G.nodes) == 0:
        fig = go.Figure()
        fig.add_annotation(text="No knowledge triples match the current filter criteria.", showarrow=False, font_size=16)
        fig.update_layout(height=500)
        return fig

    # Compute 2D spring layout positions
    pos = nx.spring_layout(G, k=0.55, iterations=60, seed=42)

    # Edge traces
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=1.2, color='#888888'),
        hoverinfo='none',
        mode='lines'
    )

    # Node traces grouped by entity type
    node_traces = []
    for n_type, color in ENTITY_COLORS.items():
        nx_list = []
        ny_list = []
        hover_texts = []
        node_names = []
        sizes = []

        for node in G.nodes():
            if G.nodes[node].get("type") == n_type:
                x, y = pos[node]
                nx_list.append(x)
                ny_list.append(y)
                hover_texts.append(G.nodes[node].get("label", str(node)))
                node_names.append(str(node).split(":")[-1])
                sizes.append(G.nodes[node].get("size", 16))

        if nx_list:
            trace = go.Scatter(
                x=nx_list, y=ny_list,
                mode='markers+text',
                name=n_type.capitalize(),
                text=node_names,
                textposition="top center",
                hovertext=hover_texts,
                hoverinfo='text',
                marker=dict(
                    color=color,
                    size=sizes,
                    line=dict(width=1.5, color='#ffffff')
                )
            )
            node_traces.append(trace)

    fig = go.Figure(
        data=[edge_trace] + node_traces,
        layout=go.Layout(
            title="Interactive Materials Knowledge Graph (Multi-Relational Ontology)",
            showlegend=True,
            hovermode='closest',
            margin=dict(b=20, l=20, r=20, t=40),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            height=650,
            template="plotly_white",
            legend=dict(orientation="h", yanchor="bottom", y=1.01, xanchor="right", x=1)
        )
    )
    return fig
