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

def check_budgets(expenses, budgets=DEFAULT_BUDGETS):
    df = pd.DataFrame(expenses)
    if df.empty:
        return

    df_expense = df[df["amount"] < 0]
    if df_expense.empty:
        return

    category_totals = df_expense.groupby("category")["amount"].sum().abs()

    for cat, limit in budgets.items():
        spent = category_totals.get(cat, 0)
        if spent > limit:
            st.warning(f"⚠️ Budget exceeded for {cat}: spent {spent} > limit {limit}")
        else:
            st.success(f"✅ Budget OK for {cat}: spent {spent} / limit {limit}")
