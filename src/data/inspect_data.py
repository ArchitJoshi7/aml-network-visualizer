import pandas as pd

def inspect():
    print("=" * 50)
    print("TRANSACTIONS")
    print("=" * 50)
    trans = pd.read_csv("data/raw/LI-Small_Trans.csv")
    print(f"Shape: {trans.shape}")
    print(f"Columns: {trans.columns.tolist()}")
    print(trans.head(3))

    print("\n" + "=" * 50)
    print("ACCOUNTS")
    print("=" * 50)
    accounts = pd.read_csv("data/raw/LI-Small_Accounts.csv")
    print(f"Shape: {accounts.shape}")
    print(f"Columns: {accounts.columns.tolist()}")
    print(accounts.head(3))

    print("\n" + "=" * 50)
    print("PATTERNS (first 20 lines)")
    print("=" * 50)
    with open("data/raw/LI-Small_Patterns.txt", "r") as f:
        for i, line in enumerate(f):
            if i >= 20:
                break
            print(line.strip())

if __name__ == "__main__":
    inspect()