import pandas as pd
import streamlit as st

def show_analytics_dashboard(expenses):
    if not expenses:
        st.warning("No expense data available yet.")
        return

    df = pd.DataFrame(expenses)
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["amount", "date"])

    # Only expenses (negative values)
    df_exp = df[df["amount"] < 0].copy()
    df_exp["amount"] = df_exp["amount"].abs()

    st.subheader("Spending Insights")

    # 1️⃣ Total & Average Spending
    total_spend = df_exp["amount"].sum()
    avg_monthly = df_exp.groupby(df_exp["date"].dt.to_period("M"))["amount"].sum().mean()

    st.metric("Total Spend", f"₹{total_spend:,.2f}")
    st.metric("Avg Monthly Spend", f"₹{avg_monthly:,.2f}")

    # 2️⃣ Top Categories
    st.subheader("Top Categories")
    category_totals = df_exp.groupby("category")["amount"].sum().sort_values(ascending=False)
    st.bar_chart(category_totals)

    # 3️⃣ Monthly Trend
    st.subheader("Monthly Trend")
    monthly_trend = df_exp.groupby(df_exp["date"].dt.to_period("M"))["amount"].sum()
    st.line_chart(monthly_trend)

    # 4️⃣ Overspending detection
    st.subheader("Overspending Alerts")
    avg_spend = df_exp["amount"].mean()
    high_spend = df_exp[df_exp["amount"] > avg_spend * 1.5]

    if not high_spend.empty:
        st.warning("You have unusually high spends in these categories:")
        st.dataframe(high_spend[["date", "category", "amount", "note"]])
    else:
        st.success("No abnormal spending detected!")

    # 5️⃣ Pie Chart Breakdown
    st.subheader("Category Breakdown")
    st.pyplot(category_totals.plot.pie(y="amount", autopct='%1.1f%%', figsize=(5,5)).figure)
