from fastapi import FastAPI
from pydantic import BaseModel
import mlflow
import pandas as pd
import logging
import os

logging.basicConfig(
    filename="salary1_api.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    force=True
)

MODEL_URI = os.getenv("MODEL_URI", "models:/Salary Prediction model/3")
model = None

app = FastAPI(
    title="Salary Prediction API",
    version="1.0",
    description="Salary Prediction using MLflow Registered Model"
)

class Employee(BaseModel):
    Age: int
    Gender: str
    Education_Level: str
    Job_Title: str
    Years_of_Experience: float

@app.on_event("startup")
def load_model():
    global model
    try:
        print("Loading Registered Model...")
        logging.info("Loading Registered Model...")
        model = mlflow.pyfunc.load_model(MODEL_URI)
        print("Model Loaded Successfully!")
        logging.info("Model Loaded Successfully!")
    except Exception as e:
        model = None
        logging.error(f"Model loading failed: {e}")
        print(f"Model loading failed: {e}")

@app.get("/health")
def health():
    return {
        "status": "Running",
        "model_loaded": model is not None
    }

@app.post("/predict")
def predict(employee: Employee):
    try:
        if model is None:
            return {"Error": "Model not loaded"}

        input_df = pd.DataFrame([{
            "Age": employee.Age,
            "Gender": employee.Gender,
            "Education Level": employee.Education_Level,
            "Job Title": employee.Job_Title,
            "Years of Experience": employee.Years_of_Experience
        }])

        prediction = model.predict(input_df)

        return {
            "Predicted Salary": round(float(prediction[0]), 2)
        }

    except Exception as e:
        logging.error(str(e))
        return {"Error": str(e)}
