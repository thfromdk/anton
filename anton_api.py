from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from anton_model import score_user
from anton_db import init_db, log_score


app = FastAPI()
# TEMP: Hardcoded valid keys
VALID_KEYS = {"demo-key-1", "test-partner-key", "anton-dev"}

init_db()

class UserProfile(BaseModel):
    digital_score: float
    financial_activity: float
    engagement: float
    income_weight: float
    employment_score: float

@app.post("/score")
def get_score(
    user: UserProfile,
    x_api_key: str = Header(...)
):
    if x_api_key not in VALID_KEYS:
        raise HTTPException(status_code=403, detail="Invalid API key")

    features = [
        user.digital_score,
        user.financial_activity,
        user.engagement,
        user.income_weight,
        user.employment_score
    ]

    score, explanation = score_user(features)
    risk_band = "Low" if score > 0.7 else "Medium" if score > 0.4 else "High"

    log_score({
        "digital_score": user.digital_score,
        "financial_activity": user.financial_activity,
        "engagement": user.engagement,
        "income_weight": user.income_weight,
        "employment_score": user.employment_score,
        "anton_score": score,
        "risk_band": risk_band
    })

    return {
        "anton_score": score,
        "risk_band": risk_band,
        "explanation": explanation
    }


