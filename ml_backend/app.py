from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
import pandas as pd

# Initialize FastAPI app
app = FastAPI()

# Load models
rf_model = joblib.load("rf_return_model.pkl")  # RandomForest model for return prediction
xgb_model = joblib.load("resale_model.pkl")  # XGBoost model for resale prediction

# Pydantic model for input data validation
class ProductData(BaseModel):
    price: float
    delivery_time: int
    low_price: int
    high_density_city: int
    review_score: int
    freight_value: float
    customer_city: str
    customer_state: str
    order_status: str  # 'delivered', 'canceled', etc.

@app.post("/predict-return/")
async def predict_return(data: ProductData):
    # Prepare input data
    features = np.array([[
        data.price,
        data.delivery_time,
        data.low_price,
        data.high_density_city,
        data.review_score,
        data.freight_value
    ]])

    # Predict using return prediction model (RandomForest)
    prediction = rf_model.predict_proba(features)[:, 1]

    return {"prediction": prediction[0]}
    print("Return prediction probability:", prediction[0])

@app.post("/predict-resale/")
async def predict_resale(data: ProductData):
    # Prepare input data
    features = np.array([[
        data.price,
        data.review_score,
        data.freight_value
    ]])

    # Predict using resale prediction model (XGBoost)
    resale_value = xgb_model.predict(features)

    return {"predicted_resale_value": resale_value[0]}


from fastapi.middleware.cors import CORSMiddleware

# Allow frontend requests (IMPORTANT!)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict to localhost:5173 in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load cleaned dataset
cleaned_df = pd.read_csv("cleaned_data.csv")

@app.get("/get-dataset")
async def get_dataset():
    return cleaned_df.to_dict(orient="records")