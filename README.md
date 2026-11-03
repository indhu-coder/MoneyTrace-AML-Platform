# MoneyTrace-AML-Platform
Detect.Trace.Investigate

It is a Real-time AML Transaction MOnitoring & Investigation Platform

An enterprise-style Anti-Money Laundering project .

Project type: Banking / FinTech Financial Crime Compliance (FinCrime)

Business Usecase:

To build a platform that consumes payment events, evaluates them against AML scenarios, calculates customer and transaction risk, links related accounts, and creates investigator work items. The platform should preserve the evidence behind every alert and support a documented disposition workflow. The key idea is a layered detection approach: deterministic rules for known typologies, statistical/ML scoring for deviations from a customer's baseline, and graph analytics for relationships across accounts. The final score is a prioritization aid—not a finding of criminal conduct

MONEYTRACE - SYNTHETIC DATA GENERATED
-------------------------------------
Customers     : 100
Accounts      : 150
Transactions  : 1000

Transaction scenario breakdown:
scenario_label
NORMAL                 850
STRUCTURING_PATTERN     60
HIGH_FREQUENCY          40
HIGH_VALUE              30
RAPID_MOVEMENT          20
Name: count, dtype: int64

Files saved in: D:\MoneyTrace\MoneyTrace-AML-Platform\data\synthetic

========== MONEYTRACE DATA INTEGRITY VALIDATION ==========

1. RECORD COUNTS
----------------
Customers: 100
Accounts: 150
Transactions: 1000

2. DUPLICATE ID CHECK
---------------------
Duplicate customer IDs: 0
Duplicate account IDs: 0
Duplicate transaction IDs: 0

3. MISSING VALUE CHECK
----------------------
Customers missing values: 0
Accounts missing values: 0
Transactions missing values: 0

4. ACCOUNT REFERENCE CHECK
--------------------------
Invalid sender accounts: 0
Invalid receiver accounts: 0
Invalid customer references: 0

5. TRANSACTION AMOUNT CHECK
---------------------------
Zero or negative amounts: 0
Same sender and receiver: 0

6. TRANSACTION SCENARIO DISTRIBUTION
------------------------------------
scenario_label
NORMAL                 850
STRUCTURING_PATTERN     60
HIGH_FREQUENCY          40
HIGH_VALUE              30
RAPID_MOVEMENT          20
Name: count, dtype: int64

7. FINAL VALIDATION REPORT
--------------------------
Customer count: PASS
Account count: PASS
Transaction count: PASS
Unique customer IDs: PASS
Unique account IDs: PASS
Unique transaction IDs: PASS
No missing values: PASS
Valid account references: PASS
Valid customer references: PASS
Positive transaction amounts: PASS
Different sender and receiver: PASS

SUCCESS: All validation checks passed!

========== MONEYTRACE MONITORING ==========

Rule 1: 30 high-value transactions detected
Rule 2: 2 accounts flagged for high-frequency activity
Rule 3: 1 accounts flagged for structuring-like activity

ALERT SUMMARY
-------------------------
Total alerts: 33

Alerts by rule:
rule_id
AML_RULE_001    30
AML_RULE_002     2
AML_RULE_003     1
Name: count, dtype: int64

Alerts by severity:
severity
HIGH      30
MEDIUM     3
Name: count, dtype: int64

Alerts saved to: D:\MoneyTrace\MoneyTrace-AML-Platform\data\synthetic\alerts.csv

Monitoring completed successfully.

========== MONEYTRACE ALERT REPORT ==========

TOTAL ALERTS: 33

1. ALERTS BY SEVERITY
severity
HIGH      30
MEDIUM     3
Name: count, dtype: int64

2. ALERTS BY RULE
rule_id
AML_RULE_001    30
AML_RULE_002     2
AML_RULE_003     1
Name: count, dtype: int64

3. TOP ACCOUNTS BY ALERT COUNT
account_id
ACC0107    2
ACC0045    2
ACC0122    2
ACC0077    2
ACC0064    2
ACC0037    1
ACC0085    1
ACC0067    1
ACC0150    1
ACC0147    1
Name: count, dtype: int64

4. ALERT DETAILS
alert_id      rule_id account_id severity                              description
ALT00001 AML_RULE_001    ACC0037     HIGH High-value outgoing transaction detected
ALT00002 AML_RULE_001    ACC0085     HIGH High-value outgoing transaction detected
ALT00003 AML_RULE_001    ACC0067     HIGH High-value outgoing transaction detected
ALT00004 AML_RULE_001    ACC0150     HIGH High-value outgoing transaction detected
ALT00005 AML_RULE_001    ACC0147     HIGH High-value outgoing transaction detected
ALT00006 AML_RULE_001    ACC0107     HIGH High-value outgoing transaction detected
ALT00007 AML_RULE_001    ACC0107     HIGH High-value outgoing transaction detected
ALT00008 AML_RULE_001    ACC0045     HIGH High-value outgoing transaction detected
ALT00009 AML_RULE_001    ACC0045     HIGH High-value outgoing transaction detected
ALT00010 AML_RULE_001    ACC0126     HIGH High-value outgoing transaction detected
