# AML Transaction Network Visualizer

A graph-based visual analytics tool for detecting and understanding 
money laundering patterns in financial transaction data.

Built as a portfolio project to demonstrate product thinking at the 
intersection of compliance, fintech, and graph analytics.

---

## The Problem

Anti-money laundering (AML) teams at banks process millions of 
transactions daily. Traditional rule-based systems flag individual 
transactions — but money laundering is a *network problem*. 
Criminals exploit relationships between accounts across multiple 
banks and payment formats to obscure the origin of funds.

This project visualizes those relationships.

---

## Key Findings

- **ACH is the dominant laundering format** — 73.2% of all laundering 
  transactions use ACH, vs 11.4% of legitimate transactions. 
  Wire transfers and Reinvestment show 0% laundering usage — 
  too traceable.

- **Bank 1217 → Bank 20 is the hottest corridor** — 10 laundering 
  transactions between these two banks, more than any other pair 
  in the dataset.

- **Three distinct laundering typologies identified** — Fan-In 
  (aggregation), Fan-Out (dispersal), and Gather-Scatter (layering) 
  patterns are visually distinct and detectable from raw transaction 
  data alone.

- **Laundering ratio: 0.051%** — only 3,565 suspicious transactions 
  out of 6.9M total, matching real-world AML base rates.

---

## Visuals

| Visual | Description |
|---|---|
| Interactive Network | Zoomable graph of 500 accounts — red nodes are suspicious |
| Typology Subgraphs | Fan-In, Fan-Out, Gather-Scatter patterns isolated and labeled |
| Bank Risk Heatmap | Which bank-to-bank corridors are most exploited |
| Payment Format Chart | ACH vs Cheque vs Wire — laundering vs legitimate breakdown |

---

## Dataset

IBM Transactions for Anti-Money Laundering (AML)  
Source: Kaggle — `ealtman2019/ibm-transactions-for-anti-money-laundering-aml`  
File used: `LI-Small` (Low Illicit ratio — realistic simulation)  
License: Public, synthetic data — no real account information

---

## Tech Stack

| Tool | Purpose |
|---|---|
| `networkx` | Graph construction and analysis |
| `pyvis` | Interactive HTML graph visualization |
| `matplotlib` + `seaborn` | Static charts |
| `pandas` | Data processing |
| `Python 3.12` | Runtime |

---

## How to Run

**1. Clone the repo and install dependencies**
```bash
git clone https://github.com/ArchitJoshi7/aml-network-visualizer
cd aml-network-visualizer
pip install -r requirements.txt
```

**2. Download the dataset**
- Go to: https://www.kaggle.com/datasets/ealtman2019/ibm-transactions-for-anti-money-laundering-aml
- Download `LI-Small_Trans.csv`, `LI-Small_Patterns.txt`
- Place all three in `data/raw/`

**3. Run the pipeline**
```bash
python src/data/prepare_graph_data.py
python src/processing/build_graph.py
```

**4. Generate visuals**
```bash
python src/visualization/interactive_graph.py
python src/visualization/chart2_typologies.py
python src/visualization/chart3_bank_heatmap.py
python src/visualization/chart4_payment_formats.py
```

**5. Open the interactive graph**
```bash
start outputs/figures/transaction_network.html
```

---

## Project Structure
```
aml-network-visualizer/
├── data/
│   ├── raw/               # Downloaded Kaggle files
│   └── processed/         # Cleaned graph data
├── src/
│   ├── data/              # Data preparation scripts
│   ├── processing/        # Graph construction
│   └── visualization/     # All chart scripts
├── outputs/figures/       # Generated charts and HTML graph
├── writeup/case_study.md  # PM framing of the project
└── requirements.txt
```

---

## Author

Built by [Your Name] as part of a fintech PM portfolio.  
Targeting product roles at hedge funds and compliance-focused fintech firms.