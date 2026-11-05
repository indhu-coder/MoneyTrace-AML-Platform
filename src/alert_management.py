from datetime import datetime

from pathlib import Path
import pandas as pd


# ---------------------------------------
# 1. File locations
# ---------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "synthetic"

ALERT_FILE = DATA_DIR / "alerts.csv"
REVIEW_FILE = DATA_DIR / "alert_reviews.csv"

# ---------------------------------------
# 2. Review record structure
# ---------------------------------------

REVIEW_COLUMNS = [
    "alert_id",
    "status",
    "assigned_to",
    "disposition",
    "investigation_notes",
    "updated_at"
]

# ---------------------------------------
# 3. Load alerts and review records
# ---------------------------------------

def load_alert_data():

    if not ALERT_FILE.exists():
        raise FileNotFoundError(
            "alerts.csv not found. Run monitoring.py first."
        )

    alerts = pd.read_csv(ALERT_FILE, dtype={"alert_id": str})

    if REVIEW_FILE.exists():
        reviews = pd.read_csv(
            REVIEW_FILE,
            dtype=str,
            keep_default_na=False
        )
    else:
        reviews = pd.DataFrame(columns=REVIEW_COLUMNS)

    # Add review records for newly generated alerts
    existing_ids = set(reviews["alert_id"])

    new_alerts = alerts[
        ~alerts["alert_id"].isin(existing_ids)
    ]

    if not new_alerts.empty:

        new_reviews = pd.DataFrame({
            "alert_id": new_alerts["alert_id"],
            "status": "NEW",
            "assigned_to": "",
            "disposition": "",
            "investigation_notes": "",
            "updated_at": ""
        })

        reviews = pd.concat(
            [reviews, new_reviews],
            ignore_index=True
        )

        reviews.to_csv(REVIEW_FILE, index=False)

    return alerts, reviews

# ---------------------------------------
# 4. Display alert queue
# ---------------------------------------

def view_alert_queue(alerts, reviews):

    queue = alerts.merge(
        reviews,
        on="alert_id",
        how="left"
    )

    print("\n========== ALERT QUEUE ==========\n")

    if queue.empty:
        print("No alerts available.")
        return

    columns = [
        "alert_id",
        "rule_id",
        "account_id",
        "severity",
        "status",
        "assigned_to"
    ]

    print(queue[columns].to_string(index=False))

    print("\nTotal alerts:", len(queue))

# ---------------------------------------
# 5. View individual alert details
# ---------------------------------------

def view_alert_details(alerts, reviews):

    alert_id = input("\nEnter Alert ID: ").strip()

    matching = alerts[alerts["alert_id"] == alert_id]

    if matching.empty:
        print("Alert not found.")
        return

    alert = matching.iloc[0]
    review = reviews[
        reviews["alert_id"] == alert_id
    ].iloc[0]

    print("\n========== ALERT DETAILS ==========")

    print("Alert ID:", alert["alert_id"])
    print("Rule:", alert["rule_id"])
    print("Account:", alert["account_id"])
    print("Transaction:", alert["triggering_transaction_id"])
    print("Amount:", alert["total_amount"])
    print("Severity:", alert["severity"])
    print("Description:", alert["description"])

    print("\n========== INVESTIGATION ==========")

    print("Status:", review["status"])
    print("Assigned to:", review["assigned_to"])
    print("Disposition:", review["disposition"])
    print("Notes:", review["investigation_notes"])
    print("Last updated:", review["updated_at"])

# ---------------------------------------
# 6. Update an alert
# ---------------------------------------

def update_alert(reviews):

    alert_id = input("\nEnter Alert ID: ").strip()

    matching = reviews.index[
        reviews["alert_id"] == alert_id
    ]

    if len(matching) == 0:
        print("Alert not found.")
        return

    index = matching[0]

    print("\n1. Mark as UNDER_REVIEW")
    print("2. Mark as CLOSED")

    choice = input("Select status: ").strip()

    if choice == "1":

        status = "UNDER_REVIEW"
        disposition = ""

    elif choice == "2":

        status = "CLOSED"

        print("\nSelect disposition:")
        print("1. FALSE_POSITIVE")
        print("2. ESCALATED")
        print("3. SUSPICIOUS_ACTIVITY")
        print("4. INSUFFICIENT_INFORMATION")

        disposition_choice = input(
            "Enter disposition: "
        ).strip()

        dispositions = {
            "1": "FALSE_POSITIVE",
            "2": "ESCALATED",
            "3": "SUSPICIOUS_ACTIVITY",
            "4": "INSUFFICIENT_INFORMATION"
        }

        if disposition_choice not in dispositions:
            print("Invalid disposition.")
            return

        disposition = dispositions[disposition_choice]

    else:
        print("Invalid status.")
        return

    investigator = input(
        "Enter investigator name (blank to keep existing): "
    ).strip()

    note = input("Enter investigation note: ").strip()

    if investigator:
        reviews.loc[index, "assigned_to"] = investigator

    reviews.loc[index, "status"] = status
    reviews.loc[index, "disposition"] = disposition

    if note:
        existing_note = reviews.loc[
            index, "investigation_notes"
        ]

        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        new_note = f"[{timestamp}] {note}"

        if existing_note:
            reviews.loc[index, "investigation_notes"] = (
                existing_note + " | " + new_note
            )
        else:
            reviews.loc[index, "investigation_notes"] = new_note

    reviews.loc[index, "updated_at"] = datetime.now().isoformat(
        timespec="seconds"
    )

    reviews.to_csv(REVIEW_FILE, index=False)

    print("\nAlert updated successfully!")

# ---------------------------------------
# 7. Main application menu
# ---------------------------------------

def main():

    alerts, reviews = load_alert_data()

    print("\n================================")
    print("       MONEYTRACE")
    print("    ALERT MANAGEMENT")
    print("================================")

    while True:

        print("\n1. View alert queue")
        print("2. View alert details")
        print("3. Update alert")
        print("4. Exit")

        choice = input("\nSelect an option: ").strip()

        if choice == "1":
            view_alert_queue(alerts, reviews)

        elif choice == "2":
            view_alert_details(alerts, reviews)

        elif choice == "3":
            update_alert(reviews)

        elif choice == "4":
            print("\nExiting MoneyTrace. Goodbye!")
            break

        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
