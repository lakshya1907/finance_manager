import streamlit as st
import pandas as pd

DEFAULT_BUDGETS = {
    "food": 1000,
    "travel": 500,
    "shopping": 1500,
    "bills": 2000,
    "entertainment": 800,
    "other": 500
}

import pandas as pd

def check_budgets(expenses):
    df = pd.DataFrame(expenses)

    # Ensure 'amount' is numeric (convert strings -> floats, non-numeric -> NaN)
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0)

    # Separate only expenses (negative values)
    df_expense = df[df["amount"] < 0]

    if df_expense.empty:
        return "✅ No expenses yet to compare with budgets."

    category_totals = df_expense.groupby("category")["amount"].sum().abs().to_dict()

    results = []
    for category, total in category_totals.items():
        results.append(f"{category}: ₹{total:.2f}")

    return "\n".join(results)
