import streamlit as st
import pandas as pd
from anton_model import score_user

REQUIRED_COLUMNS = [
    "digital_score",
    "financial_activity",
    "engagement",
    "income_weight",
    "employment_score"
]

st.set_page_config(page_title="Anton Credit Scoring", layout="centered")

st.title("Anton — Alternative Credit Scoring Demo")
st.caption("Helping the financially invisible be seen.")

st.markdown("---")

# SINGLE USER SCORING
st.header("📍 Single User Scoring")

with st.form("single_user_form"):
    digital_score = st.slider("Digital Score", 0.0, 3.0, 1.0)
    financial_activity = st.slider("Financial Activity", 0.0, 4.0, 2.0)
    engagement = st.slider("Engagement Score", 0.0, 3.0, 1.0)
    income_weight = st.slider("Income Weight", 0.0, 1.0, 0.5)
    employment_score = st.slider("Employment Score", 0.0, 1.0, 0.5)

    submitted = st.form_submit_button("Score User")

    if submitted:
        features = [digital_score, financial_activity, engagement, income_weight, employment_score]
        score, explanation = score_user(features)
        risk_band = "Low" if score > 0.7 else "Medium" if score > 0.4 else "High"

        st.metric(label="Anton Score", value=f"{round(score, 2)}")
        st.write(f"**Risk Band:** {risk_band}")
        st.markdown("**Explanation:**")
        for reason in explanation:
            st.markdown(f"- {reason}")

st.markdown("---")

# BATCH SCORING
st.header("📁 Batch Scoring (CSV Upload)")

uploaded_file = st.file_uploader("Upload a CSV with 5 required columns", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)

        # Column check
        if not all(col in df.columns for col in REQUIRED_COLUMNS):
            st.error(f"❌ CSV must contain these columns: {', '.join(REQUIRED_COLUMNS)}")
        else:
            df["anton_score"] = None
            df["risk_band"] = None
            df["explanation"] = None

            for idx, row in df.iterrows():
                features = [row[col] for col in REQUIRED_COLUMNS]
                score, explanation = score_user(features)
                df.at[idx, "anton_score"] = round(score, 2)
                df.at[idx, "risk_band"] = "Low" if score > 0.7 else "Medium" if score > 0.4 else "High"
                df.at[idx, "explanation"] = "; ".join(explanation)

            st.success("✅ Scoring complete. Preview below:")
            st.dataframe(df)

            st.download_button(
                label="Download Scored CSV",
                data=df.to_csv(index=False).encode('utf-8'),
                file_name="scored_users.csv",
                mime="text/csv"
            )

    except Exception as e:
        st.error(f"Something went wrong while processing the file. Details: {e}")
