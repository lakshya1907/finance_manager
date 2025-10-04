import pandas as pd
from datetime import datetime

CATEGORIES = ["food", "travel", "shopping", "salary", "bills", "entertainment", "other"]

def add_transaction(expenses, amount, category, note, date_str=None):
    """Add a transaction to expenses list."""
    if category not in CATEGORIES:
        category = "other"
    if not date_str:
        date_str = datetime.today().strftime("%Y-%m-%d")
    transaction = {
        "amount": float(amount),
        "category": category,
        "note": note,
        "date": date_str
    }
    expenses.append(transaction)
    return transaction

def get_summary(expenses):
    """Return total income, expense, net savings."""
    total_income = sum(e['amount'] for e in expenses if e['amount'] > 0)
    total_expense = sum(abs(e['amount']) for e in expenses if e['amount'] < 0)
    net_savings = total_income - total_expense
    return {"income": total_income, "expense": total_expense, "net": net_savings}
