import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

def plot_bank_heatmap(data_path: str, output_path: str, top_n: int = 10):
    df = pd.read_csv(data_path)

    # Focus on laundering transactions only
    laund = df[df['is_laundering'] == 1].copy()

    # Clean bank names — they're numeric IDs, label them
    laund['from_bank'] = 'Bank ' + laund['from_bank'].astype(str)
    laund['to_bank'] = 'Bank ' + laund['to_bank'].astype(str)

    # Get top N banks by involvement
    top_from = laund['from_bank'].value_counts().head(top_n).index.tolist()
    top_to = laund['to_bank'].value_counts().head(top_n).index.tolist()
    top_banks = list(set(top_from + top_to))[:top_n]

    # Filter to top banks
    filtered = laund[
        laund['from_bank'].isin(top_banks) &
        laund['to_bank'].isin(top_banks)
    ]

    # Build pivot table
    pivot = filtered.groupby(['from_bank', 'to_bank']).size().unstack(fill_value=0)
    pivot = pivot.reindex(index=top_banks, columns=top_banks, fill_value=0)

    fig, ax = plt.subplots(figsize=(12, 9))

    sns.heatmap(
        pivot,
        ax=ax,
        cmap='Reds',
        linewidths=0.5,
        linecolor='#1a1a2e',
        annot=True,
        fmt='d',
        annot_kws={'size': 9},
        cbar_kws={'label': 'Number of Laundering Transactions'}
    )

    ax.set_title('Bank-to-Bank Laundering Transaction Heatmap\nWhich corridors are most exploited by bad actors?',
                 fontsize=13, fontweight='bold', pad=20)
    ax.set_xlabel('Destination Bank', fontsize=11)
    ax.set_ylabel('Source Bank', fontsize=11)
    ax.tick_params(axis='x', rotation=45)
    ax.tick_params(axis='y', rotation=0)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"Saved Chart 3 to {output_path}")
    plt.show()

if __name__ == "__main__":
    plot_bank_heatmap(
        data_path="data/processed/graph_data.csv",
        output_path="outputs/figures/chart3_bank_heatmap.png"
    )