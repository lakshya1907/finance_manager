import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

def predict_expense(expenses, category):
    """
    Predict next expense amount for a given category using simple linear regression.
    
    expenses: list of dicts with keys: amount, category, date
    category: string
    Returns predicted value (float)
    """
    if not expenses:
        return 0

    # Convert to DataFrame
    df = pd.DataFrame(expenses)

    # Ensure 'amount' is numeric
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    df = df.dropna(subset=["amount"])

    # Only negative amounts (expenses)
    df_expense = df[df["amount"] < 0].copy()
    df_expense["amount"] = df_expense["amount"].abs()  # make positive

    # Filter by category
    df_cat = df_expense[df_expense["category"] == category]
    if df_cat.empty:
        return 0

    # Convert date to ordinal
    df_cat["date"] = pd.to_datetime(df_cat["date"], errors="coerce")
    df_cat = df_cat.dropna(subset=["date"])
    if df_cat.empty:
        return 0

    df_cat["day_num"] = df_cat["date"].map(lambda x: x.toordinal())
    X = df_cat[["day_num"]]
    y = df_cat["amount"]

    # Handle small datasets
    if len(df_cat) < 2:
        X_train, y_train = X, y
    else:
        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

    # Train model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Predict next day
    next_day = pd.Timestamp.now().toordinal() + 1
    pred = model.predict(np.array([[next_day]]))
    return max(pred[0], 0)  # avoid negative prediction
