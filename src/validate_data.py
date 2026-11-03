
from pathlib import Path
import pandas as pd

# Locate the synthetic data folder
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "synthetic"

# Load the three datasets
customers = pd.read_csv(DATA_DIR / "customers.csv")
accounts = pd.read_csv(DATA_DIR / "accounts.csv")
transactions = pd.read_csv(DATA_DIR / "transactions.csv")

print("\n========== MONEYTRACE DATA VALIDATION ==========\n")

# 1. Check record counts
print("1. RECORD COUNTS")
print("----------------")
print("Customers:", len(customers))
print("Accounts:", len(accounts))
print("Transactions:", len(transactions))

# 2. Check duplicate IDs
print("\n2. DUPLICATE ID CHECK")
print("---------------------")
print("Duplicate customer IDs:", customers["customer_id"].duplicated().sum())
print("Duplicate account IDs:", accounts["account_id"].duplicated().sum())
print("Duplicate transaction IDs:", transactions["transaction_id"].duplicated().sum())

# 3. Check missing values
print("\n3. MISSING VALUE CHECK")
print("----------------------")
print("Customers missing values:", customers.isnull().sum().sum())
print("Accounts missing values:", accounts.isnull().sum().sum())
print("Transactions missing values:", transactions.isnull().sum().sum())

# 4. Check account references
print("\n4. ACCOUNT REFERENCE CHECK")
print("--------------------------")

valid_accounts = set(accounts["account_id"])

invalid_senders = (~transactions["sender_account"].isin(valid_accounts)).sum()
invalid_receivers = (~transactions["receiver_account"].isin(valid_accounts)).sum()

print("Invalid sender accounts:", invalid_senders)
print("Invalid receiver accounts:", invalid_receivers)

# 5. Check customer references in accounts
valid_customers = set(customers["customer_id"])

invalid_customers = (~accounts["customer_id"].isin(valid_customers)).sum()

print("Invalid customer references:", invalid_customers)

# 6. Check transaction amounts
print("\n5. TRANSACTION AMOUNT CHECK")
print("---------------------------")
print("Zero or negative amounts:", (transactions["amount"] <= 0).sum())

# 7. Check sender and receiver
print("Same sender and receiver:", (
    transactions["sender_account"] == transactions["receiver_account"]
).sum())

# 8. Scenario distribution
print("\n6. TRANSACTION SCENARIO DISTRIBUTION")
print("------------------------------------")
print(transactions["scenario_label"].value_counts())

# 9. Final validation result
checks = {
    "Customer count": len(customers) == 100,
    "Account count": len(accounts) == 150,
    "Transaction count": len(transactions) == 1000,
    "Unique customer IDs": customers["customer_id"].is_unique,
    "Unique account IDs": accounts["account_id"].is_unique,
    "Unique transaction IDs": transactions["transaction_id"].is_unique,
    "No missing values": (
        customers.notnull().all().all()
        and accounts.notnull().all().all()
        and transactions.notnull().all().all()
    ),
    "Valid account references": invalid_senders == 0 and invalid_receivers == 0,
    "Valid customer references": invalid_customers == 0,
    "Positive transaction amounts": (transactions["amount"] > 0).all(),
    "Different sender and receiver": (
        transactions["sender_account"] != transactions["receiver_account"]
    ).all()
}

print("\n7. FINAL VALIDATION REPORT")
print("--------------------------")

for check, result in checks.items():
    print(f"{check}: {'PASS' if result else 'FAIL'}")

if all(checks.values()):
    print("\nSUCCESS: All validation checks passed!")
else:
    print("\nWARNING: Some validation checks failed. Review the results.")
