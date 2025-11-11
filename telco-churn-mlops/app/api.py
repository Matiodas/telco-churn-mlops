# ===============================================================
# 📦 API FastAPI para predicción de Churn de clientes Telco
# ===============================================================

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import joblib

# ---------------------------------------------------------------
# 1️⃣ Inicializar app y cargar modelo
# ---------------------------------------------------------------
app = FastAPI(title="API de Predicción de Churn 📊")

MODEL_PATH = "app/model.joblib"

try:
    model = joblib.load(MODEL_PATH)
    print(f"✅ Modelo cargado correctamente desde {MODEL_PATH}")
except Exception as e:
    print(f"❌ Error cargando el modelo: {e}")
    raise RuntimeError("No se pudo cargar el modelo entrenado")

# ---------------------------------------------------------------
# 2️⃣ Definir los campos esperados
# ---------------------------------------------------------------
class CustomerData(BaseModel):
    gender: str
    SeniorCitizen: int
    Partner: str
    Dependents: str
    tenure: int
    PhoneService: str
    MultipleLines: str
    InternetService: str
    OnlineSecurity: str
    OnlineBackup: str
    DeviceProtection: str
    TechSupport: str
    StreamingTV: str
    StreamingMovies: str
    Contract: str
    PaperlessBilling: str
    PaymentMethod: str
    MonthlyCharges: float
    TotalCharges: float

# ---------------------------------------------------------------
# 3️⃣ Endpoint principal (bienvenida)
# ---------------------------------------------------------------
@app.get("/")
def home():
    return {
        "message": "API de predicción de churn de clientes Telco 📊",
        "status": "online",
        "model_path": MODEL_PATH
    }

# ---------------------------------------------------------------
# 4️⃣ Health check
# ---------------------------------------------------------------
@app.get("/health")
def health():
    return {"status": "healthy", "model_loaded": True}

# ---------------------------------------------------------------
# 5️⃣ Endpoint de predicción
# ---------------------------------------------------------------
@app.post("/predict")
def predict(customer: CustomerData):
    try:
        # Convertir entrada a DataFrame
        X = pd.DataFrame([customer.dict()])

        # Predicción
        prob = model.predict_proba(X)[0][1]
        pred = int(prob >= 0.5)

        # Interpretación del riesgo
        if prob < 0.3:
            risk = "Bajo"
        elif prob < 0.7:
            risk = "Moderado"
        else:
            risk = "Alto"

        return {
            "Churn": bool(pred),
            "Churn_probability": round(float(prob), 4),
            "Risk_level": risk,
            "interpretation": f"El cliente tiene un riesgo {risk.lower()} de fuga."
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en predicción: {str(e)}")

# ---------------------------------------------------------------
# 6️⃣ Ejecutar servidor local
# ---------------------------------------------------------------
# Ejecuta con:
# uvicorn app.api_fast:app --reload --host 0.0.0.0 --port 8000
