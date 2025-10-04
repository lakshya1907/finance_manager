import csv
from datetime import datetime

RECURRING_FILE = "data/recurring.csv"

def load_recurring():
    recurring = []
    try:
        with open(RECURRING_FILE, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                recurring.append({
                    "amount": float(row["amount"]),
                    "category": row["category"],
                    "note": row["note"],
                    "day_of_month": int(row["day_of_month"])
                })
    except FileNotFoundError:
        pass
    return recurring

def apply_recurring(expenses, recurring):
    today = datetime.today().day
    added = 0
    for r in recurring:
        if r["day_of_month"] == today:
            transaction = {
                "amount": r["amount"],
                "category": r["category"],
                "note": f"(Auto) {r['note']}",
                "date": datetime.today().strftime("%Y-%m-%d")
            }
            expenses.append(transaction)
            added += 1
    return added
