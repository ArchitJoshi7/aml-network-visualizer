import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import warnings
warnings.filterwarnings('ignore')

def parse_patterns(patterns_path: str):
    patterns = {'FAN-IN': [], 'FAN-OUT': [], 'GATHER-SCATTER': []}
    current_type = None
    current_transactions = []

    with open(patterns_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('BEGIN LAUNDERING ATTEMPT'):
                current_transactions = []
                if 'FAN-IN' in line:
                    current_type = 'FAN-IN'
                elif 'FAN-OUT' in line:
                    current_type = 'FAN-OUT'
                elif 'GATHER-SCATTER' in line:
                    current_type = 'GATHER-SCATTER'
                else:
                    current_type = None
            elif line.startswith('END LAUNDERING ATTEMPT'):
                if current_type and current_transactions:
                    patterns[current_type].append(current_transactions)
                current_type = None
            elif current_type and line:
                parts = line.split(',')
                if len(parts) >= 4:
                    current_transactions.append({
                        'from': parts[2],
                        'to': parts[4] if len(parts) > 4 else parts[3],
                        'amount': float(parts[5]) if len(parts) > 5 else 0
                    })

    return patterns

def build_pattern_graph(transactions):
    G = nx.DiGraph()
    for t in transactions:
        G.add_edge(t['from'][:6], t['to'][:6], weight=t['amount'])
    return G

def plot_typologies(patterns_path: str, output_path: str):
    print("Parsing patterns...")
    patterns = parse_patterns(patterns_path)

    for k, v in patterns.items():
        print(f"{k}: {len(v)} patterns found")

    fig, axes = plt.subplots(1, 3, figsize=(18, 7), facecolor='#0d1117')
    fig.suptitle('Money Laundering Typologies\nHow criminals structure transactions to avoid detection',
                 fontsize=14, fontweight='bold', color='white', y=1.02)

    configs = [
        ('FAN-IN',         '#e74c3c', 'Fan-In\nMultiple sources → single account\n(Aggregation)'),
        ('FAN-OUT',        '#e67e22', 'Fan-Out\nSingle source → multiple accounts\n(Dispersal)'),
        ('GATHER-SCATTER', '#9b59b6', 'Gather-Scatter\nCollect then disperse\n(Layering)'),
    ]

    for ax, (pattern_type, color, title) in zip(axes, configs):
        ax.set_facecolor('#0d1117')

        # Pick first pattern with enough nodes
        sample = None
        for p in patterns.get(pattern_type, []):
            if len(p) >= 2:
                sample = p
                break

        if sample is None:
            ax.text(0.5, 0.5, 'No pattern found', color='white',
                    ha='center', va='center', transform=ax.transAxes)
            ax.set_title(title, color=color, fontsize=11, fontweight='bold', pad=15)
            continue

        G = build_pattern_graph(sample)

        # Layout
        if pattern_type == 'FAN-IN':
            pos = nx.shell_layout(G)
        elif pattern_type == 'FAN-OUT':
            pos = nx.shell_layout(G)
        else:
            pos = nx.spring_layout(G, seed=42, k=2)

        # Node colors — destination node is darker
        all_nodes = list(G.nodes())
        in_degrees = dict(G.in_degree())
        out_degrees = dict(G.out_degree())

        node_colors = []
        node_sizes = []
        for node in all_nodes:
            if in_degrees[node] > out_degrees[node]:
                node_colors.append('#ff6b6b')  # sink node
                node_sizes.append(800)
            elif out_degrees[node] > in_degrees[node]:
                node_colors.append('#ffd93d')  # source node
                node_sizes.append(600)
            else:
                node_colors.append(color)
                node_sizes.append(400)

        nx.draw_networkx_nodes(G, pos, ax=ax, node_color=node_colors,
                               node_size=node_sizes, alpha=0.95)
        nx.draw_networkx_labels(G, pos, ax=ax, font_size=7,
                                font_color='white', font_weight='bold')
        nx.draw_networkx_edges(G, pos, ax=ax, edge_color=color,
                               arrows=True, arrowsize=20,
                               width=2, alpha=0.8,
                               connectionstyle='arc3,rad=0.1')

        ax.set_title(title, color=color, fontsize=11, fontweight='bold', pad=15)
        ax.axis('off')

    # Legend
    legend_elements = [
        mpatches.Patch(color='#ffd93d', label='Source account'),
        mpatches.Patch(color='#ff6b6b', label='Destination account'),
        mpatches.Patch(color='#aaaaaa', label='Intermediary account'),
    ]
    fig.legend(handles=legend_elements, loc='lower center', ncol=3,
               facecolor='#1a1a2e', labelcolor='white', fontsize=10,
               bbox_to_anchor=(0.5, -0.05))

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight',
                facecolor='#0d1117')
    print(f"Saved Chart 2 to {output_path}")
    plt.show()

if __name__ == "__main__":
    plot_typologies(
        patterns_path="data/raw/LI-Small_Patterns.txt",
        output_path="outputs/figures/chart2_typologies.png"
    )