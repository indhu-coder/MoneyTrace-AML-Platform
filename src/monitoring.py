
from pathlib import Path
from collections import deque
import pandas as pd


# ---------------------------------------
# 1. Project paths and configuration
# ---------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "synthetic"

INPUT_FILE = DATA_DIR / "transactions.csv"
OUTPUT_FILE = DATA_DIR / "alerts.csv"

HIGH_VALUE_THRESHOLD = 100000

HIGH_FREQUENCY_COUNT = 5
HIGH_FREQUENCY_WINDOW = pd.Timedelta(hours=24)

STRUCTURING_MIN_AMOUNT = 9000
STRUCTURING_MAX_AMOUNT = 10000
STRUCTURING_COUNT = 5
STRUCTURING_WINDOW = pd.Timedelta(hours=48)


# ---------------------------------------
# 2. Load transaction data
# ---------------------------------------

transactions = pd.read_csv(INPUT_FILE)

transactions["transaction_timestamp"] = pd.to_datetime(
    transactions["transaction_timestamp"]
)

transactions = transactions.sort_values(
    "transaction_timestamp"
).reset_index(drop=True)

alerts = []


# ---------------------------------------
# 3. Common alert creation function
# ---------------------------------------

def create_alert(
    rule_id,
    account_id,
    transaction_id,
    transaction_count,
    total_amount,
    severity,
    description,
    timestamp
):
    alert = {
        "alert_id": f"ALT{len(alerts) + 1:05d}",
        "rule_id": rule_id,
        "account_id": account_id,
        "triggering_transaction_id": transaction_id,
        "transaction_count": transaction_count,
        "total_amount": round(float(total_amount), 2),
        "severity": severity,
        "description": description,
        "created_at": timestamp
    }

    alerts.append(alert)


# ---------------------------------------
# 4. Rule 1: High-value transactions
# ---------------------------------------

def detect_high_value(df):

    flagged = df[df["amount"] >= HIGH_VALUE_THRESHOLD]

    for _, row in flagged.iterrows():

        create_alert(
            rule_id="AML_RULE_001",
            account_id=row["sender_account"],
            transaction_id=row["transaction_id"],
            transaction_count=1,
            total_amount=row["amount"],
            severity="HIGH",
            description="High-value outgoing transaction detected",
            timestamp=row["transaction_timestamp"]
        )

    print(f"Rule 1: {len(flagged)} high-value transactions detected")


# ---------------------------------------
# 5. Rule 2: High-frequency transactions
# ---------------------------------------

def detect_high_frequency(df):

    detected_accounts = set()

    for account_id, group in df.groupby("sender_account"):

        group = group.sort_values("transaction_timestamp")

        window = deque()
        window_amount = 0

        for _, row in group.iterrows():

            current_time = row["transaction_timestamp"]

            window.append(row)
            window_amount += row["amount"]

            # Remove transactions older than 24 hours
            while (
                window
                and current_time - window[0]["transaction_timestamp"]
                > HIGH_FREQUENCY_WINDOW
            ):
                removed = window.popleft()
                window_amount -= removed["amount"]

            # Generate only one alert per account for this rule
            if (
                len(window) >= HIGH_FREQUENCY_COUNT
                and account_id not in detected_accounts
            ):

                create_alert(
                    rule_id="AML_RULE_002",
                    account_id=account_id,
                    transaction_id=row["transaction_id"],
                    transaction_count=len(window),
                    total_amount=window_amount,
                    severity="MEDIUM",
                    description=(
                        "Multiple outgoing transactions within 24 hours"
                    ),
                    timestamp=current_time
                )

                detected_accounts.add(account_id)

    print(
        f"Rule 2: {len(detected_accounts)} accounts "
        "flagged for high-frequency activity"
    )


# ---------------------------------------
# 6. Rule 3: Structuring-like transactions
# ---------------------------------------

def detect_structuring(df):

    # Consider only transactions within the configured amount range
    filtered = df[
        (df["amount"] >= STRUCTURING_MIN_AMOUNT)
        & (df["amount"] < STRUCTURING_MAX_AMOUNT)
    ]

    detected_accounts = set()

    for account_id, group in filtered.groupby("sender_account"):

        group = group.sort_values("transaction_timestamp")

        window = deque()
        window_amount = 0

        for _, row in group.iterrows():

            current_time = row["transaction_timestamp"]

            window.append(row)
            window_amount += row["amount"]

            # Remove transactions older than 48 hours
            while (
                window
                and current_time - window[0]["transaction_timestamp"]
                > STRUCTURING_WINDOW
            ):
                removed = window.popleft()
                window_amount -= removed["amount"]

            # Generate one alert per account for this rule
            if (
                len(window) >= STRUCTURING_COUNT
                and account_id not in detected_accounts
            ):

                create_alert(
                    rule_id="AML_RULE_003",
                    account_id=account_id,
                    transaction_id=row["transaction_id"],
                    transaction_count=len(window),
                    total_amount=window_amount,
                    severity="MEDIUM",
                    description=(
                        "Repeated transfers within the configured "
                        "near-threshold amount range"
                    ),
                    timestamp=current_time
                )

                detected_accounts.add(account_id)

    print(
        f"Rule 3: {len(detected_accounts)} accounts "
        "flagged for structuring-like activity"
    )


# ---------------------------------------
# 7. Execute all monitoring rules
# ---------------------------------------

print("\n========== MONEYTRACE MONITORING ==========\n")

detect_high_value(transactions)

detect_high_frequency(transactions)

detect_structuring(transactions)


# ---------------------------------------
# 8. Save alerts
# ---------------------------------------

alerts_df = pd.DataFrame(alerts)

if not alerts_df.empty:

    alerts_df.to_csv(OUTPUT_FILE, index=False)

    print("\nALERT SUMMARY")
    print("-------------------------")
    print("Total alerts:", len(alerts_df))

    print("\nAlerts by rule:")
    print(alerts_df["rule_id"].value_counts())

    print("\nAlerts by severity:")
    print(alerts_df["severity"].value_counts())

    print(f"\nAlerts saved to: {OUTPUT_FILE}")

else:

    print("\nNo alerts generated.")

    alerts_df.to_csv(OUTPUT_FILE, index=False)


print("\nMonitoring completed successfully.")
