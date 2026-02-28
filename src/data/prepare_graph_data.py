import pandas as pd

def prepare(trans_path: str, accounts_path: str, output_path: str):
    print("Loading transactions...")
    trans = pd.read_csv(trans_path)

    # Rename columns for clarity
    trans = trans.rename(columns={
        'Account': 'from_account',
        'Account.1': 'to_account',
        'From Bank': 'from_bank',
        'To Bank': 'to_bank',
        'Amount Paid': 'amount',
        'Payment Currency': 'currency',
        'Payment Format': 'payment_format',
        'Is Laundering': 'is_laundering'
    })

    # Separate laundering and legitimate
    laundering = trans[trans['is_laundering'] == 1]
    legitimate = trans[trans['is_laundering'] == 0]

    print(f"Total transactions     : {len(trans):,}")
    print(f"Laundering transactions: {len(laundering):,}")
    print(f"Legitimate transactions: {len(legitimate):,}")
    print(f"Laundering ratio       : {len(laundering)/len(trans)*100:.3f}%")

    # Sample legitimate transactions — same count as laundering for balance
    legit_sample = legitimate.sample(n=min(len(laundering) * 3, 50000), random_state=42)

    # Combine
    df = pd.concat([laundering, legit_sample], ignore_index=True)
    print(f"\nFinal dataset size: {len(df):,}")
    print(f"  Laundering : {df['is_laundering'].sum():,}")
    print(f"  Legitimate : {(df['is_laundering']==0).sum():,}")

    # Merge account metadata for from_account
    accounts = pd.read_csv(accounts_path)
    accounts = accounts.rename(columns={
        'Account Number': 'account_number',
        'Bank Name': 'bank_name',
        'Entity Name': 'entity_name'
    })

    # Keep only needed columns
    df = df[['from_account', 'to_account', 'from_bank', 'to_bank',
             'amount', 'currency', 'payment_format', 'is_laundering', 'Timestamp']]

    df.to_csv(output_path, index=False)
    print(f"\nSaved prepared data to {output_path}")

if __name__ == "__main__":
    prepare(
        trans_path="data/raw/LI-Small_Trans.csv",
        accounts_path="data/raw/LI-Small_Accounts.csv",
        output_path="data/processed/graph_data.csv"
    )