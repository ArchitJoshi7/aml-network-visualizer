import pandas as pd
import networkx as nx
import pickle
from pyvis.network import Network

def build_interactive(graph_path: str, output_path: str, max_nodes: int = 500):
    with open(graph_path, 'rb') as f:
        G = pickle.load(f)

    print(f"Full graph: {G.number_of_nodes():,} nodes, {G.number_of_edges():,} edges")

    # Focus on suspicious subgraph + their neighbors
    suspicious_nodes = [n for n, d in G.nodes(data=True) if d.get('is_laundering') == 1]

    # Get neighbors of suspicious nodes
    neighbors = set()
    for node in suspicious_nodes:
        neighbors.update(G.predecessors(node))
        neighbors.update(G.successors(node))

    # Combine suspicious + neighbors, cap at max_nodes
    all_nodes = list(set(suspicious_nodes) | neighbors)[:max_nodes]
    subgraph = G.subgraph(all_nodes)

    print(f"Subgraph : {subgraph.number_of_nodes():,} nodes, {subgraph.number_of_edges():,} edges")

    # Build pyvis network
    net = Network(
        height="900px",
        width="100%",
        bgcolor="#0d1117",
        font_color="white",
        directed=True
    )

    net.barnes_hut(gravity=-8000, central_gravity=0.3, spring_length=100)

    # Add nodes
    for node, data in subgraph.nodes(data=True):
        is_sus = data.get('is_laundering', 0)
        bank = data.get('bank', 'Unknown')

        color = "#e74c3c" if is_sus else "#3498db"
        size = 20 if is_sus else 8
        border = "#ff0000" if is_sus else "#2980b9"
        label = str(node)[:8]  # truncate long account IDs

        net.add_node(
            str(node),
            label=label,
            title=f"Account: {node}<br>Bank: {bank}<br>Suspicious: {'Yes' if is_sus else 'No'}",
            color={"background": color, "border": border},
            size=size,
            font={"size": 8}
        )

    # Add edges
    for src, dst, data in subgraph.edges(data=True):
        is_sus = data.get('is_laundering', 0)
        amount = data.get('weight', 0)
        count = data.get('count', 1)
        fmt = data.get('payment_format', '')

        color = "#e74c3c" if is_sus else "#2ecc7150"
        width = 3 if is_sus else 1

        net.add_edge(
            str(src), str(dst),
            title=f"Amount: ${amount:,.2f}<br>Transactions: {count}<br>Format: {fmt}",
            color=color,
            width=width,
            arrows="to"
        )

    # Add legend via title
    net.set_options("""
    {
        "nodes": {
            "borderWidth": 2,
            "shadow": true
        },
        "edges": {
            "shadow": true,
            "smooth": {"type": "curvedCW", "roundness": 0.2}
        },
        "interaction": {
            "hover": true,
            "tooltipDelay": 100,
            "zoomView": true,
            "dragView": true
        },
        "physics": {
            "enabled": true,
            "stabilization": {"iterations": 200}
        }
    }
    """)

    net.save_graph(output_path)
    print(f"\nSaved interactive graph to {output_path}")
    print("Open the HTML file in your browser to explore!")

if __name__ == "__main__":
    build_interactive(
        graph_path="data/processed/transaction_graph.pkl",
        output_path="outputs/figures/transaction_network.html"
    )