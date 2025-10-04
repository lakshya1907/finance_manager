import csv
import os
import matplotlib.pyplot as plt
from datetime import datetime

FILENAME = "expenses.csv"
expenses = []

RECURRING_FILE = "recurring.csv"
recurring = []


def add_recurring():
    try:
        amount = float(input("Enter recurring amount (negative for expense, positive for income): "))
    except ValueError:
        print("❌ Invalid amount.")
        return

    print(f"Available categories: {categories}")
    category = input("Enter category: ").strip()
    if category not in categories:
        category = "Other"

    note = input("Enter note: ")
    day = int(input("Enter day of month (1–31): "))

    entry = {"amount": amount, "category": category, "note": note, "day_of_month": day}
    recurring.append(entry)

    with open(RECURRING_FILE, mode="a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["amount", "category", "note", "day_of_month"])
        if file.tell() == 0:
            writer.writeheader()
        writer.writerow(entry)

    print("✅ Recurring transaction added!")


def apply_recurring():
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

            # Also write to main CSV
            with open(FILENAME, mode="a", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=["amount", "category", "note", "date"])
                if file.tell() == 0:
                    writer.writeheader()
                writer.writerow(transaction)
            added += 1

    if added > 0:
        print(f"📅 {added} recurring transaction(s) automatically added for today!")




# Predefined categories
categories = ["food", "travel", "shopping", "salary", "bills", "entertainment", "other"]

# Budget limits per category (example)
budgets = {"food": 1000, "travel": 500, "shopping": 1500, "bills": 2000, "entertainment": 800}

# Load existing expenses
if os.path.exists(FILENAME):
    with open(FILENAME, mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            expenses.append({
                "amount": float(row["amount"]),
                "category": row["category"],
                "note": row["note"],
                "date": row.get("date", datetime.today().strftime("%Y-%m-%d"))
            })

# Load recurring transactions
if os.path.exists(RECURRING_FILE):
    with open(RECURRING_FILE, mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            recurring.append({
                "amount": float(row["amount"]),
                "category": row["category"],
                "note": row["note"],
                "day_of_month": int(row["day_of_month"])
            })

apply_recurring()

# ===== Functions =====
def add_transaction():
    try:
        amount = float(input("Enter amount (negative for expense, positive for income): "))
    except ValueError:
        print("Invalid amount. Try again.")
        return

    print(f"Available categories: {categories}")
    category = input("Enter category: ").strip()
    if category not in categories:
        print("Category not recognized. Using 'other'.")
        category = "other"

    note = input("Enter note: ")
    date_str = input("Enter date (YYYY-MM-DD) or leave blank for today: ").strip()
    if date_str == "":
        date_str = datetime.today().strftime("%Y-%m-%d")

    transaction = {"amount": amount, "category": category, "note": note, "date": date_str}
    expenses.append(transaction)

    # Save to CSV
    with open(FILENAME, mode="a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["amount", "category", "note", "date"])
        if file.tell() == 0:
            writer.writeheader()
        writer.writerow(transaction)

    print("Transaction added & saved!")

def view_transactions():
    if not expenses:
        print("No transactions found!")
        return
    print("\n--- Transactions ---")
    for e in expenses:
        print(f"{e['date']} | {e['amount']} - {e['category']} ({e['note']})")

def show_summary():
    total_income = sum(e['amount'] for e in expenses if e['amount'] > 0)
    total_expense = sum(abs(e['amount']) for e in expenses if e['amount'] < 0)
    net_savings = total_income - total_expense

    print("\n--- Summary ---")
    print(f"Total Income:  {total_income}")
    print(f"Total Expense: {total_expense}")
    print(f"Net Savings:   {net_savings}")

def show_charts():
    category_totals = {}
    for e in expenses:
        if e['amount'] < 0:
            category_totals[e['category']] = category_totals.get(e['category'], 0) + abs(e['amount'])

    if not category_totals:
        print("No expenses to show!")
        return

    # Bar chart
    plt.figure(figsize=(8,5))
    plt.bar(category_totals.keys(), category_totals.values(), color='skyblue')
    plt.title("Expenses by Category")
    plt.xlabel("Category")
    plt.ylabel("Amount")
    plt.show()

    # Pie chart
    plt.figure(figsize=(6,6))
    plt.pie(category_totals.values(), labels=category_totals.keys(), autopct='%1.1f%%', startangle=90)
    plt.title("Expense Distribution")
    plt.show()

def show_monthly_report():
    month_totals = {}
    for e in expenses:
        month = e['date'][:7]  # YYYY-MM
        month_totals[month] = month_totals.get(month, 0) + e['amount']

    if not month_totals:
        print("No transactions to report!")
        return

    print("\n--- Monthly Report ---")
    for month, total in month_totals.items():
        print(f"{month}: Net {total}")

def check_budgets():
    category_totals = {}
    for e in expenses:
        if e['amount'] < 0:
            category_totals[e['category']] = category_totals.get(e['category'], 0) + abs(e['amount'])

    for cat, limit in budgets.items():
        spent = category_totals.get(cat, 0)
        if spent > limit:
            print(f" Alert: You exceeded your budget for {cat} (${spent} > ${limit})")
        else:
            print(f" You are good on your budget for {cat} ")
         



# ===== Main Program =====
while True:
    print("\n1. Add Transaction")
    print("2. View Transactions")
    print("3. Exit")
    print("4. Show Summary")
    print("5. Show Charts")
    print("6. Show Monthly Report")
    print("7. Check Budget Alerts")
    print("8. Add Recurring Transaction")

    choice = input("Enter choice: ")

    if choice == "1":
        add_transaction()
    elif choice == "2":
        view_transactions()
    elif choice == "3":
        print(" All transactions saved. Goodbye!")
        break
    elif choice == "4":
        show_summary()
    elif choice == "5":
        show_charts()
    elif choice == "6":
        show_monthly_report()
    elif choice == "7":
        check_budgets()
    elif choice == "8":
        add_recurring()
    else:
        print("Invalid choice")
