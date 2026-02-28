import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.sankey import Sankey
import warnings
warnings.filterwarnings('ignore')

def plot_sankey(data_path: str, output_path: str):
    df = pd.read_csv(data_path)

    # Separate laundering vs legitimate
    laund = df[df['is_laundering'] == 1]
    legit = df[df['is_laundering'] == 0]

    # Count by payment format
    laund_counts = laund['payment_format'].value_counts()
    legit_counts = legit['payment_format'].value_counts()

    # Align formats
    all_formats = list(set(laund_counts.index) | set(legit_counts.index))
    laund_counts = laund_counts.reindex(all_formats, fill_value=0)
    legit_counts = legit_counts.reindex(all_formats, fill_value=0)

    # Normalize to percentages
    laund_pct = (laund_counts / laund_counts.sum() * 100).round(1)
    legit_pct = (legit_counts / legit_counts.sum() * 100).round(1)

    # Sort by laundering preference
    sorted_formats = laund_pct.sort_values(ascending=False).index.tolist()

    fig, axes = plt.subplots(1, 2, figsize=(16, 7))
    fig.suptitle('Payment Format Distribution: Laundering vs Legitimate Transactions\n'
                 'How do criminals prefer to move money compared to normal transactions?',
                 fontsize=13, fontweight='bold', y=1.02)

    colors = ['#e74c3c', '#e67e22', '#f1c40f', '#2ecc71', '#3498db', '#9b59b6', '#1abc9c']

    for ax, (pct, title, base_color) in zip(axes, [
        (laund_pct, 'Laundering Transactions', '#e74c3c'),
        (legit_pct, 'Legitimate Transactions', '#3498db')
    ]):
        values = [pct[fmt] for fmt in sorted_formats]
        bar_colors = [base_color if i == 0 else colors[i % len(colors)]
                      for i in range(len(sorted_formats))]

        bars = ax.barh(sorted_formats, values, color=bar_colors,
                       edgecolor='white', linewidth=0.5, height=0.6)

        # Value labels
        for bar, val in zip(bars, values):
            ax.text(val + 0.3, bar.get_y() + bar.get_height() / 2,
                    f'{val:.1f}%', va='center', fontsize=10, fontweight='bold')

        ax.set_xlim(0, max(values) * 1.3)
        ax.set_xlabel('Percentage of Transactions (%)', fontsize=11)
        ax.set_title(title, fontsize=12, fontweight='bold',
                     color=base_color, pad=10)
        ax.grid(axis='x', alpha=0.3)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

    # Highlight key differences
    fig.text(0.5, -0.05,
             '💡 Key Insight: Compare the dominant payment formats between laundering and legitimate transactions\n'
             'Criminals tend to favour specific formats to layer and obscure the origin of funds.',
             ha='center', fontsize=10, style='italic', color='#555555')

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"Saved Chart 4 to {output_path}")
    plt.show()

if __name__ == "__main__":
    plot_sankey(
        data_path="data/processed/graph_data.csv",
        output_path="outputs/figures/chart4_payment_formats.png"
    )