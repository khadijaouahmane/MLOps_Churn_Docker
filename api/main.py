"""API REST : SEUL point d'accès au modèle ML. Aucun client ne charge le .pkl."""
import json
import os
import pickle
import time

import pandas as pd
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware

from api.schemas import ChurnInput, ChurnOutput

app = FastAPI(
    title="Telco Churn Prediction API",
    description="Prédiction de churn à partir d'un pipeline sklearn sérialisé.",
    version="1.1.0",
)

# En prod, restreignez avec ALLOWED_ORIGINS="https://mon-front.herokuapp.com"
origins = os.environ.get("ALLOWED_ORIGINS", "*").split(",")
app.add_middleware(CORSMiddleware, allow_origins=origins,
                   allow_methods=["*"], allow_headers=["*"])


@app.middleware("http")
async def add_process_time(request: Request, call_next):
    t0 = time.perf_counter()
    response = await call_next(request)
    response.headers["X-Process-Time-ms"] = f"{(time.perf_counter() - t0) * 1000:.1f}"
    return response


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "model", "pipeline_churn.pkl")
META_PATH = os.path.join(BASE_DIR, "model", "metadata.json")

with open(MODEL_PATH, "rb") as f:
    pipeline = pickle.load(f)

metadata = {}
if os.path.exists(META_PATH):
    with open(META_PATH) as f:
        metadata = json.load(f)


@app.get("/", tags=["Info"])
def home():
    return {"message": "Telco Churn API", "docs": "/docs", "metadata": metadata}


@app.get("/health", tags=["Info"])
def health():
    return {"status": "ok"}


@app.post("/predict", response_model=ChurnOutput, tags=["Prediction"])
def predict(payload: ChurnInput):
    try:
        df = pd.DataFrame([payload.model_dump()])
        pred = int(pipeline.predict(df)[0])
        proba = float(pipeline.predict_proba(df)[0][1])
        return ChurnOutput(
            prediction=pred,
            probability_churn=round(proba, 4),
            label="Churn probable" if pred == 1 else "Client fidèle",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
