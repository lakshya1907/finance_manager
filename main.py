import streamlit as st
from core.file_manager import load_csv, save_csv
from core.transactions import add_transaction, get_summary
from core.reports import show_charts, show_monthly_report
from core.budgets import check_budgets
from core.recurring import load_recurring, apply_recurring
from datetime import datetime
from core.ml.predict_expense import predict_expense


# Load data
expenses = load_csv("data/expenses.csv")
recurring = load_recurring()
added = apply_recurring(expenses, recurring)

if added > 0:
    st.info(f"{added} recurring transaction(s) added today!")

st.title("💰 Personal Finance Manager")

menu = st.sidebar.radio(
    "📂 Menu",
    ["Add Transaction", "View Summary", "Charts", "Monthly Report", "Budget Alerts","ML Prediction"]
)

# ===========================================
# ✅ 1️⃣ ADD TRANSACTION PAGE (updated UX)
# ===========================================
if menu == "Add Transaction":
    st.header("➕ Add New Transaction")

    with st.form("add_transaction_form", clear_on_submit=True):
        # 🔸 Select transaction type
        transaction_type = st.radio(
            "Select type:",
            ["Income", "Expense"],
            horizontal=True
        )

        # 🔸 Amount input (always positive)
        amount = st.number_input("Enter amount:", min_value=0.0, step=10.0)

        # Convert expense to negative automatically
        if transaction_type == "Expense":
            amount = -amount

        # 🔸 Category selection
        category = st.selectbox(
            "Category",
            ["food", "travel", "shopping", "salary", "bills", "entertainment", "other"]
        )

        # 🔸 Optional note
        note = st.text_input("Note (optional)")

        # 🔸 Date input
        date_str = st.date_input("Date", datetime.today())

        # 🔸 Submit button
        submitted = st.form_submit_button("Add Transaction")

        if submitted:
            add_transaction(expenses, amount, category, note, str(date_str))
            save_csv("data/expenses.csv", expenses, ["amount", "category", "note", "date"])
            st.success(f"✅ Added {transaction_type.lower()} of ₹{abs(amount):,.2f} in {category}!")
            check_budgets(expenses)

# ===========================================
# ✅ 2️⃣ VIEW SUMMARY
# ===========================================
elif menu == "View Summary":
    st.header("📊 Summary")
    summary = get_summary(expenses)
    st.write(summary)

# ===========================================
# ✅ 3️⃣ CHARTS
# ===========================================
elif menu == "Charts":
    st.header("📈 Charts")
    show_charts(expenses)

# ===========================================
# ✅ 4️⃣ MONTHLY REPORT
# ===========================================
elif menu == "Monthly Report":
    show_monthly_report(expenses)

# ===========================================
# ✅ 5️⃣ BUDGET ALERTS
# ===========================================
elif menu == "Budget Alerts":
    check_budgets(expenses)

# ===========================================
# ✅ 5️⃣ ML
# ===========================================

elif menu == "ML Prediction":
    st.header("Expense Prediction")
    category = st.selectbox("Select Category", ["food", "travel", "shopping", "bills", "entertainment", "other"])
    if st.button("Predict"):
        from core.ml.predict_expense import predict_expense
        prediction = predict_expense(expenses, category)
        st.success(f"Predicted next expense in '{category}': ${prediction:.2f}")
