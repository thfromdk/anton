import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Load your dataset
df = pd.read_csv("micro_world_kenya.csv", sep=";")

# Drop rows with missing values for required fields
df = df.dropna(subset=[
    "mobileowner", "pay_onlne", "pay_cash",
    "saved", "borrowed", "receive_wages", "pay_utilities",
    "receive_transfers", "receive_pension", "receive_agriculture",
    "inc_q", "emp_in"
])

# Feature engineering
df["digital_score"] = df["mobileowner"] + df["pay_onlne"] + df["pay_cash"]
df["financial_activity"] = df["saved"] + df["borrowed"] + df["receive_wages"] + df["pay_utilities"]
df["engagement"] = df[["receive_transfers", "receive_pension", "receive_agriculture"]].sum(axis=1)

# Add income + employment features
df["income_weight"] = df["inc_q"] * 0.25  # Scale 1-4 → 0.25–1.0
df["employment_score"] = df["emp_in"].map({
    1: 1.0,   # Wage employed
    2: 0.8,   # Self-employed
    3: 0.5,   # Out of labor force
    4: 0.2    # Unemployed
}).fillna(0)

# Model features + label
X = df[["digital_score", "financial_activity", "engagement", "income_weight", "employment_score"]]
y = df["borrowed"]

X_train, _, y_train, _ = train_test_split(X, y, test_size=0.2, random_state=42)

# Smarter model: Random Forest
model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
model.fit(X_train, y_train)

# Scoring function
def score_user(input_features):
    proba = model.predict_proba([input_features])[0][1]
    explanation = []

    if input_features[0] > 1:
        explanation.append("High mobile activity")
    if input_features[1] > 2:
        explanation.append("Frequent financial transactions")
    if input_features[3] >= 0.75:
        explanation.append("Upper income tier")
    if input_features[4] >= 0.8:
        explanation.append("Stable employment")

    return round(proba, 2), explanation
