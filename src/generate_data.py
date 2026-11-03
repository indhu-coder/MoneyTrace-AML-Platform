from pathlib import Path
from datetime import datetime, timedelta
import random

import numpy as np
import pandas as pd
from faker import Faker


# Reproducible synthetic data
random.seed(42)
np.random.seed(42)
Faker.seed(42)

fake = Faker("en_IN")

# Project data folder
BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "data" / "synthetic"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# -----------------------------
# 1. Generate 100 customers
# -----------------------------

customers = []

for i in range(1, 101):
    customers.append({
        "customer_id": f"CUST{i:04d}",
        "customer_name": fake.name(),
        "occupation": fake.job(),
        "risk_category": random.choices(
            ["LOW", "MEDIUM", "HIGH"],
            weights=[70, 25, 5]
        )[0],
        "city": fake.city(),
        "customer_since": fake.date_between(
            start_date="-10y",
            end_date="today"
        )
    })

customers_df = pd.DataFrame(customers)

# -----------------------------
# 2. Generate 150 bank accounts
# -----------------------------

accounts = []
customer_ids = customers_df["customer_id"].tolist()

for i in range(1, 151):
    owner = customer_ids[(i - 1) % len(customer_ids)]

    accounts.append({
        "account_id": f"ACC{i:04d}",
        "customer_id": owner,
        "account_type": random.choice(
            ["SAVINGS", "CURRENT"]
        ),
        "balance": round(random.uniform(5000, 1000000), 2),
        "account_status": "ACTIVE"
    })

accounts_df = pd.DataFrame(accounts)

account_ids = accounts_df["account_id"].tolist()

# -----------------------------
# 3. Generate 1,000 transactions
# -----------------------------

transactions = []

start_date = datetime.now() - timedelta(days=30)


def add_transaction(sender, receiver, amount, timestamp, scenario):
    transactions.append({
        "transaction_id": f"TXN{len(transactions) + 1:06d}",
        "sender_account": sender,
        "receiver_account": receiver,
        "amount": round(float(amount), 2),
        "currency": "INR",
        "transaction_type": "TRANSFER",
        "channel": random.choice(
            ["MOBILE", "INTERNET_BANKING", "BRANCH"]
        ),
        "transaction_timestamp": timestamp,
        "status": "SUCCESS",
        "scenario_label": scenario
    })


def get_receiver(sender):
    receiver = random.choice(account_ids)

    while receiver == sender:
        receiver = random.choice(account_ids)

    return receiver


# A. 850 ordinary transactions
for _ in range(850):
    sender = random.choice(account_ids)
    receiver = get_receiver(sender)

    amount = np.random.uniform(100, 25000)
    timestamp = start_date + timedelta(
        minutes=random.randint(0, 30 * 24 * 60)
    )

    add_transaction(
        sender, receiver, amount, timestamp, "NORMAL"
    )


# B. 30 unusually large transactions
for _ in range(30):
    sender = random.choice(account_ids)
    receiver = get_receiver(sender)

    amount = np.random.uniform(100000, 500000)
    timestamp = start_date + timedelta(
        minutes=random.randint(0, 30 * 24 * 60)
    )

    add_transaction(
        sender, receiver, amount, timestamp, "HIGH_VALUE"
    )


# C. 60 smaller transactions from one account
# These simulate a transaction-splitting pattern.
sender = random.choice(account_ids)

for _ in range(60):
    receiver = get_receiver(sender)

    amount = np.random.uniform(9000, 9999)
    timestamp = start_date + timedelta(
        minutes=random.randint(0, 48 * 60)
    )

    add_transaction(
        sender, receiver, amount, timestamp, "STRUCTURING_PATTERN"
    )


# D. 40 transactions from one account in a short period
# These simulate unusually high transaction frequency.
sender = random.choice(account_ids)

for _ in range(40):
    receiver = get_receiver(sender)

    amount = np.random.uniform(1000, 5000)
    timestamp = start_date + timedelta(
        minutes=random.randint(0, 24 * 60)
    )

    add_transaction(
        sender, receiver, amount, timestamp, "HIGH_FREQUENCY"
    )


# E. 20 transactions moving funds through a chain of accounts
chain_accounts = random.sample(account_ids, 21)

for i in range(20):
    sender = chain_accounts[i]
    receiver = chain_accounts[i + 1]

    amount = np.random.uniform(5000, 30000)
    timestamp = start_date + timedelta(
        minutes=1000 + (i * 10)
    )

    add_transaction(
        sender, receiver, amount, timestamp, "RAPID_MOVEMENT"
    )


transactions_df = pd.DataFrame(transactions)

# Sort transactions by date and time
transactions_df["transaction_timestamp"] = pd.to_datetime(
    transactions_df["transaction_timestamp"]
)

transactions_df = transactions_df.sort_values(
    "transaction_timestamp"
).reset_index(drop=True)

# -----------------------------
# 4. Save all three CSV files
# -----------------------------

customers_df.to_csv(
    OUTPUT_DIR / "customers.csv",
    index=False
)

accounts_df.to_csv(
    OUTPUT_DIR / "accounts.csv",
    index=False
)

transactions_df.to_csv(
    OUTPUT_DIR / "transactions.csv",
    index=False
)

# -----------------------------
# 5. Display generation summary
# -----------------------------

print("\nMONEYTRACE - SYNTHETIC DATA GENERATED")
print("-------------------------------------")
print(f"Customers     : {len(customers_df)}")
print(f"Accounts      : {len(accounts_df)}")
print(f"Transactions  : {len(transactions_df)}")

print("\nTransaction scenario breakdown:")
print(transactions_df["scenario_label"].value_counts())

print(f"\nFiles saved in: {OUTPUT_DIR}")