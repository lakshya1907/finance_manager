import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd

def show_charts(expenses):
    df = pd.DataFrame(expenses)
    if df.empty:
        st.info("No expenses to display yet.")
        return

    df["amount"] = df["amount"].astype(float)
    df_expense = df[df["amount"] < 0]
    if df_expense.empty:
        st.info("No expenses to display yet.")
        return

    category_totals = df_expense.groupby("category")["amount"].sum().abs()

    # Bar chart
    fig, ax = plt.subplots()
    ax.bar(category_totals.index, category_totals.values, color="skyblue")
    ax.set_title("Expenses by Category")
    ax.set_ylabel("Amount")
    st.pyplot(fig)

    # Pie chart
    fig2, ax2 = plt.subplots()
    ax2.pie(category_totals.values, labels=category_totals.index, autopct="%1.1f%%", startangle=90)
    ax2.set_title("Expense Distribution")
    st.pyplot(fig2)

def show_monthly_report(expenses):
    df = pd.DataFrame(expenses)
    if df.empty:
        st.info("No transactions to report.")
        return

    df["amount"] = df["amount"].astype(float)
    df["month"] = df["date"].str[:7]
    month_totals = df.groupby("month")["amount"].sum()
    st.write("### Monthly Report")
    st.table(month_totals)
