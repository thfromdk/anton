import pandas as pd
from anton_model import score_user

# Load CSV with same columns as Anton expects
df = pd.read_csv("partner_users.csv")

# Empty columns for output
df["anton_score"] = None
df["risk_band"] = None
df["explanation"] = None

for idx, row in df.iterrows():
    features = [
        row["digital_score"],
        row["financial_activity"],
        row["engagement"],
        row["income_weight"],
        row["employment_score"]
    ]

    score, explanation = score_user(features)
    df.at[idx, "anton_score"] = round(score, 2)
    df.at[idx, "risk_band"] = "Low" if score > 0.7 else "Medium" if score > 0.4 else "High"
    df.at[idx, "explanation"] = "; ".join(explanation)

# Export scored users
df.to_csv("scored_users.csv", index=False)
print("✅ Batch scoring complete. Output saved to scored_users.csv")
