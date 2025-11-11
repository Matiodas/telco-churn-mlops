# ================================================================
# ✅ TEST AUTOMATIZADO PARA LA API FASTAPI DE CHURN (Telco)
# ================================================================

import requests
import json
import time

# URL base (debe coincidir con la de FastAPI)
API_URL = "http://127.0.0.1:8000"

# ================================================================
# 🔹 Datos de ejemplo (coinciden con los usados en entrenamiento)
# ================================================================
sample_clients = [
    {
        "gender": "Female",
        "SeniorCitizen": 0,
        "Partner": "Yes",
        "Dependents": "No",
        "tenure": 5,
        "PhoneService": "Yes",
        "MultipleLines": "No",
        "InternetService": "Fiber optic",
        "OnlineSecurity": "No",
        "OnlineBackup": "No",
        "DeviceProtection": "No",
        "TechSupport": "No",
        "StreamingTV": "Yes",
        "StreamingMovies": "No",
        "Contract": "Month-to-month",
        "PaperlessBilling": "Yes",
        "PaymentMethod": "Electronic check",
        "MonthlyCharges": 75.3,
        "TotalCharges": 350.5
    },
    {
        "gender": "Male",
        "SeniorCitizen": 1,
        "Partner": "No",
        "Dependents": "No",
        "tenure": 40,
        "PhoneService": "Yes",
        "MultipleLines": "Yes",
        "InternetService": "DSL",
        "OnlineSecurity": "Yes",
        "OnlineBackup": "Yes",
        "DeviceProtection": "Yes",
        "TechSupport": "Yes",
        "StreamingTV": "Yes",
        "StreamingMovies": "Yes",
        "Contract": "Two year",
        "PaperlessBilling": "No",
        "PaymentMethod": "Credit card (automatic)",
        "MonthlyCharges": 65.7,
        "TotalCharges": 2600.4
    }
]

# ================================================================
# 🔹 Cliente de pruebas
# ================================================================
class ChurnAPIClient:
    def __init__(self, base_url=API_URL):
        self.base_url = base_url

    def test_health(self):
        """Verifica si la API está viva y funcional."""
        print(f"→ Probar endpoint /health en {self.base_url}/health ...")
        try:
            r = requests.get(f"{self.base_url}/health", timeout=5)
            print("  Código:", r.status_code)
            print("  Respuesta:", r.json())
            return r.status_code == 200
        except Exception as e:
            print(f"   ❌ Error al conectar con la API: {e}")
            return False

    def test_prediction(self, data):
        """Envía datos al endpoint /predict y muestra la respuesta."""
        print(f"→ Enviando datos para predicción...")
        try:
            r = requests.post(
                f"{self.base_url}/predict",
                json=data,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            print("  Código:", r.status_code)
            print("  Respuesta:", json.dumps(r.json(), indent=4, ensure_ascii=False))
            return r.status_code == 200
        except Exception as e:
            print(f"   ❌ Error al hacer la predicción: {e}")
            return False

# ================================================================
# 🔹 Ejecutar todas las pruebas
# ================================================================
def run_tests():
    print("🧪 EJECUTANDO PRUEBAS DE LA API FASTAPI DE CHURN")
    print("=" * 60)

    client = ChurnAPIClient()

    # Verificar disponibilidad
    for _ in range(5):
        if client.test_health():
            print("✅ API disponible y lista.")
            break
        print("⌛ Esperando que la API arranque...")
        time.sleep(2)
    else:
        print("❌ No se pudo conectar con la API.")
        print("   Asegúrate de ejecutarla con:")
        print("   uvicorn app.api_fast:app --reload --port 8000")
        return

    # Probar predicciones
    print("\n2️⃣ Probando predicciones con clientes de ejemplo...\n")
    for i, client_data in enumerate(sample_clients, 1):
        print(f"   Cliente {i}:")
        client.test_prediction(client_data)
        print("-" * 60)

    print("\n🎯 PRUEBAS FINALIZADAS")
    print("=" * 60)
    print("👉 Ejecuta la API con: uvicorn app.api_fast:app --reload --port 8000")
    print("👉 Luego este test con: python tests/test_fast_api.py\n")

# ================================================================
# 🔹 Punto de entrada
# ================================================================
if __name__ == "__main__":
    run_tests()
