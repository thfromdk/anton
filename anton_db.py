import sqlite3

def init_db():
    conn = sqlite3.connect("anton.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            digital_score REAL,
            financial_activity REAL,
            engagement REAL,
            income_weight REAL,
            employment_score REAL,
            anton_score REAL,
            risk_band TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def log_score(data):
    conn = sqlite3.connect("anton.db")
    c = conn.cursor()
    c.execute('''
        INSERT INTO scores (
            digital_score, financial_activity, engagement,
            income_weight, employment_score,
            anton_score, risk_band
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        data["digital_score"],
        data["financial_activity"],
        data["engagement"],
        data["income_weight"],
        data["employment_score"],
        data["anton_score"],
        data["risk_band"]
    ))
    conn.commit()
    conn.close()


