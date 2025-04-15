import streamlit as st
import pandas as pd
from anton_model import score_user
import io

REQUIRED_COLUMNS = [
    "digital_score",
    "financial_activity",
    "engagement",
    "income_weight",
    "employment_score"
]

st.set_page_config(page_title="Anton Credit Scoring", layout="centered")
st.title("Anton — Adaptive Credit Scoring")
st.caption("Built for imperfect data. Trusted in the real world.")

st.markdown("---")

# ================================
# SINGLE USER SCORING
# ================================

st.header("📍 Single User Scoring")

with st.form("single_user_form"):
    st.write("Fill out what you know. Leave others blank — Anton adapts.")

    input_dict = {}

    input_dict["digital_score"] = st.slider(
        "Digital Score", 0.0, 3.0, 1.0,
        help="How digitally active is this user? Higher = more mobile/app activity."
    )

    input_dict["financial_activity"] = st.slider(
        "Financial Activity", 0.0, 4.0, 2.0,
        help="Savings, borrowing, utility payments, etc."
    )

    input_dict["engagement"] = st.slider(
        "Engagement", 0.0, 3.0, 1.0,
        help="Remittances, pensions, agriculture transactions."
    )

    input_dict["income_weight"] = st.slider(
        "Income Weight", 0.0, 1.0, 0.5,
        help="Scaled income level (0.25 = low, 1.0 = top)."
    )

    input_dict["employment_score"] = st.slider(
        "Employment Score", 0.0, 1.0, 0.5,
        help="Inferred employment stability (0 = none, 1 = stable)."
    )

    submitted = st.form_submit_button("Score User")

    if submitted:
        score, confidence, explanation = score_user(input_dict)

        risk_band = "Low" if score > 0.7 else "Medium" if score > 0.4 else "High"
        band_color = "🟢" if risk_band == "Low" else "🟡" if risk_band == "Medium" else "🔴"

        st.subheader("🔎 Anton Result")
        st.metric(label="Adjusted Credit Score", value=f"{round(score, 2)}")
        st.write(f"**Risk Band:** {band_color} {risk_band}")
        st.write(f"**Confidence Level:** {confidence}")

        with st.expander("🧠 Explanation"):
            st.markdown("Anton scored this user based on available inputs. Here's why:")
            for line in explanation:
                st.markdown(f"- {line}")

st.markdown("---")

# ================================
# BATCH SCORING
# ================================

st.header("📁 Batch Scoring (CSV Upload)")

with st.expander("What should the file look like?"):
    st.markdown("You need a CSV with **these 5 columns** — or as many as you can provide:")
    st.code(", ".join(REQUIRED_COLUMNS), language="csv")

    sample_data = pd.DataFrame([{
        "digital_score": 2,
        "financial_activity": 3,
        "engagement": 1,
        "income_weight": 0.75,
        "employment_score": 0.9
    }])
    csv_bytes = sample_data.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download Sample CSV", data=csv_bytes, file_name="sample_input.csv")

uploaded_file = st.file_uploader("Upload your CSV here", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)

        df["anton_score"] = None
        df["confidence"] = None
        df["risk_band"] = None
        df["explanation"] = None

        for idx, row in df.iterrows():
            row_dict = {key: row[key] if key in df.columns else None for key in REQUIRED_COLUMNS}
            score, confidence, explanation = score_user(row_dict)
            df.at[idx, "anton_score"] = round(score, 2)
            df.at[idx, "confidence"] = confidence
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
