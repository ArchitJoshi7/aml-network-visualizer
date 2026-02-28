import pandas as pd
import networkx as nx
import pickle

def build_graph(data_path: str, output_path: str):
    df = pd.read_csv(data_path)

    print("Building directed graph...")
    G = nx.DiGraph()

    for _, row in df.iterrows():
        src = row['from_account']
        dst = row['to_account']
        is_laundering = row['is_laundering']

        # Add edge with attributes
        if G.has_edge(src, dst):
            G[src][dst]['weight'] += row['amount']
            G[src][dst]['count'] += 1
            if is_laundering:
                G[src][dst]['is_laundering'] = 1
        else:
            G.add_edge(src, dst,
                       weight=row['amount'],
                       count=1,
                       is_laundering=int(is_laundering),
                       currency=row['currency'],
                       payment_format=row['payment_format'])

        # Tag nodes
        for node in [src, dst]:
            if node not in G.nodes:
                G.add_node(node)
            if is_laundering:
                G.nodes[node]['is_laundering'] = 1
            elif 'is_laundering' not in G.nodes[node]:
                G.nodes[node]['is_laundering'] = 0

    # Add bank info
    bank_map = df.set_index('from_account')['from_bank'].to_dict()
    bank_map.update(df.set_index('to_account')['to_bank'].to_dict())
    for node in G.nodes:
        G.nodes[node]['bank'] = bank_map.get(node, 'Unknown')

    print(f"Nodes : {G.number_of_nodes():,}")
    print(f"Edges : {G.number_of_edges():,}")

    # Count suspicious nodes
    suspicious_nodes = [n for n, d in G.nodes(data=True) if d.get('is_laundering') == 1]
    suspicious_edges = [(u, v) for u, v, d in G.edges(data=True) if d.get('is_laundering') == 1]
    print(f"Suspicious nodes: {len(suspicious_nodes):,}")
    print(f"Suspicious edges: {len(suspicious_edges):,}")

    # Save graph
    with open(output_path, 'wb') as f:
        pickle.dump(G, f)
    print(f"\nSaved graph to {output_path}")

    return G

if __name__ == "__main__":
    build_graph(
        data_path="data/processed/graph_data.csv",
        output_path="data/processed/transaction_graph.pkl"
    )