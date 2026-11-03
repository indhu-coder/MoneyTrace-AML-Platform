
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
ALERT_FILE = BASE_DIR / "data" / "synthetic" / "alerts.csv"

alerts = pd.read_csv(ALERT_FILE)

print("\n========== MONEYTRACE ALERT REPORT ==========\n")

if alerts.empty:
    print("No alerts available.")
else:
    # Total alerts
    print("TOTAL ALERTS:", len(alerts))

    # Alerts by severity
    print("\n1. ALERTS BY SEVERITY")
    print(alerts["severity"].value_counts())

    # Alerts by rule
    print("\n2. ALERTS BY RULE")
    print(alerts["rule_id"].value_counts())

    # Accounts with most alerts
    print("\n3. TOP ACCOUNTS BY ALERT COUNT")
    print(
        alerts["account_id"]
        .value_counts()
        .head(10)
    )

    # Alert details
    print("\n4. ALERT DETAILS")
    print(
        alerts[
            [
                "alert_id",
                "rule_id",
                "account_id",
                "severity",
                "description"
            ]
        ].head(10).to_string(index=False)
    )

print("\n=============================================")
