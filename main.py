import streamlit as st
from core.file_manager import load_csv, save_csv
from core.transactions import add_transaction, get_summary
from core.reports import show_charts, show_monthly_report
from core.budgets import check_budgets
from core.recurring import load_recurring, apply_recurring

# Load data
expenses = load_csv("data/expenses.csv")
recurring = load_recurring()
added = apply_recurring(expenses, recurring)

if added > 0:
    st.info(f"{added} recurring transaction(s) added today!")

st.title("💰 Personal Finance Manager")

menu = st.sidebar.radio("Menu", ["Add Expense", "View Summary", "Charts", "Monthly Report", "Budget Alerts"])

if menu == "Add Expense":
    st.header(" Add New Transaction")
    amount = st.number_input("Amount", step=10.0)
    category = st.selectbox("Category", ["food", "travel", "shopping", "salary", "bills", "entertainment", "other"])
    note = st.text_input("Note")
    date_str = st.date_input("Date")
    if st.button("Add Transaction"):
        add_transaction(expenses, amount, category, note, str(date_str))
        save_csv("data/expenses.csv", expenses, ["amount", "category", "note", "date"])
        st.success(f"Added {category} - {amount}")
        check_budgets(expenses)

elif menu == "View Summary":
    st.header(" Summary")
    summary = get_summary(expenses)
    st.write(summary)

elif menu == "Charts":
    st.header(" Charts")
    show_charts(expenses)

elif menu == "Monthly Report":
    show_monthly_report(expenses)

elif menu == "Budget Alerts":
    check_budgets(expenses)
