from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import pandas as pd
import joblib
import os

from backend.database.db import SessionLocal, engine, Base
from backend.database.models import GCIScore, ManipulationFlag

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Gig Cashflow Index (GCI) API")

# --- CORS SETUP ---
# This tells the backend that it is allowed to talk to your React frontend!
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, this would be your website's exact URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/gci/{id}")
def get_gci_score(id: str):
    scores_path = 'data/processed/gci_scores.csv'
    if not os.path.exists(scores_path):
        raise HTTPException(status_code=404, detail="Scores not generated yet.")
        
    df = pd.read_csv(scores_path)
    score = df[df['borrower_id'] == id]
    if score.empty:
        raise HTTPException(status_code=404, detail="Borrower not found.")
        
    return {"borrower_id": id, "gci_score": int(score.iloc[0]['final_gci_score'])}

@app.get("/anomaly/{id}")
def get_anomaly_status(id: str):
    anomaly_path = 'data/processed/anomalies.csv'
    if not os.path.exists(anomaly_path):
        raise HTTPException(status_code=404, detail="Anomaly data not found.")
        
    df = pd.read_csv(anomaly_path)
    anomaly = df[df['borrower_id'] == id]
    if anomaly.empty:
        raise HTTPException(status_code=404, detail="Borrower not found.")
        
    return {
        "borrower_id": id,
        "manipulation_label": anomaly.iloc[0]['manipulation_label'],
        "anomaly_score": float(anomaly.iloc[0]['anomaly_score'])
    }