# Anton — Alternative Credit Scoring API

**Anton** is an API-first credit scoring engine that uses real-world behavioral data to assess risk for underserved populations.  
It replaces rigid, outdated credit systems with explainable, modular, ML-based scores.

> Built for fintechs, lenders, and developers who need infrastructure—not guesswork.

---

## 🚀 Features

- ✅ Real ML model (RandomForest) trained on open financial inclusion data from the World Bank  
- ✅ Explainable risk scores (0–1) with plain-language reasons  
- ✅ Risk banding: Low / Medium / High  
- ✅ REST API with FastAPI & Swagger UI  
- ✅ API key authentication  
- ✅ SQLite logging of every score request  
- ✅ Batch scoring tool (CSV input → scores output)

---

## 🔧 Setup

### 1. Clone the repo

```bash
git clone https://github.com/thfromdk/anton.git
cd anton
```

### 2. Create and activate virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## ⚙️ Running the API

```bash
uvicorn anton_api:app --reload
```

Then open:

```
http://127.0.0.1:8000/docs
```

You’ll see a Swagger UI to test `/score`.

---

## 📊 Batch Scoring

Use `batch_score.py` to score users in bulk.

### Example input (`partner_users.csv`):

```csv
digital_score,financial_activity,engagement,income_weight,employment_score
2,3,1,0.75,0.8
0,1,2,0.25,0.5
3,4,2,1.0,1.0
```

### Run the script:

```bash
python batch_score.py
```

Output: `scored_users.csv` with Anton scores, risk bands, and explanations.

---

## 🔐 API Key Auth

All requests to `/score` require an API key in the headers:

```
x-api-key: test-partner-key
```

---

## 🗺️ Roadmap

- [ ] Streamlit demo interface  
- [ ] Dockerized deployment  
- [ ] PostgreSQL support  
- [ ] Hosted API for partner testing  
- [ ] First live pilot with micro-lender  

---

## 🧠 Credits

Built with real behavioral data from the World Bank Global Findex Dataset.

Created by [@thfromdk](https://github.com/thfromdk) and a very committed AI.

---
