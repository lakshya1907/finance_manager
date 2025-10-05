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
    total_income = 0
    total_expense = 0

    for e in expenses:
        try:
            amount = float(e['amount'])
        except (ValueError, TypeError):
            amount = 0

        if amount > 0:
            total_income += amount
        else:
            total_expense += abs(amount)

    balance = total_income - total_expense
    return {"income": total_income, "expense": total_expense, "balance": balance}
