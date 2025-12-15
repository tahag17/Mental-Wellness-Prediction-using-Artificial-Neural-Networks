# api.py
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os

from predict_service import predict_new_user, load_model_objects

app = FastAPI(title="Mental Wellness Predictor")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request data
class UserData(BaseModel):
    age: int
    screen_time_hours: float
    work_screen_hours: float
    leisure_screen_hours: float
    sleep_hours: float
    sleep_quality_1_5: int
    stress_level_0_10: int
    productivity_0_100: int
    exercise_minutes_per_week: int
    social_hours_per_week: int
    gender: str
    occupation: str
    work_mode: str

@app.on_event("startup")
def startup_event():
    # Load model, scaler, columns.json at startup
    load_model_objects()

@app.post("/predict")
def predict(user: UserData):
    user_dict = user.dict()
    wellness_index = predict_new_user(user_dict)
    return {"mental_wellness_index": wellness_index}
