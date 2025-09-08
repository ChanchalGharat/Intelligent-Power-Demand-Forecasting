from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import pickle, json, os
import holidays

app = FastAPI()

# Add the CORS middleware here to allow requests from your frontend
origins = [
    "http://127.0.0.1:5500",  # Your frontend's origin
    "http://localhost:5500",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------
# Load model, training data, and metadata
MODEL_FILE = "prophet_model_v2.pkl"
TRAIN_FILE = "training_data_v2.csv"
META_FILE = "model_meta_v2.json"

try:
    with open(MODEL_FILE, "rb") as f:
        model = pickle.load(f)

    train_prophet = pd.read_csv(TRAIN_FILE)

    with open(META_FILE, "r") as f:
        meta = json.load(f)
except FileNotFoundError as e:
    print(f"Error: Required file not found. Please ensure {e.filename} exists.")
    # You might want to handle this more gracefully, e.g., return a 500 error
    # or a specific message to the frontend.

# -------------------------------
# Forecast Endpoint
# -------------------------------
@app.get("/forecast")
def get_forecast(periods: int = 24):
    """
    Returns forecast for given number of periods (steps ahead).
    If weather_holiday_2017.csv exists, use real data.
    Otherwise, generate dummy regressors.
    """

    # Step 1: Make future dataframe
    future = model.make_future_dataframe(periods=periods, freq=meta["freq"])

    # -------------------------------
    # Option 1: Use real CSV if available
    # -------------------------------
    if os.path.exists("weather_holiday_2017.csv"):
        weather_holiday = pd.read_csv("weather_holiday_2017.csv")

        future = future.merge(
            weather_holiday,
            how="left",
            left_on="ds",
            right_on="Datetime"
        ).drop(columns=["Datetime"])

    else:
        # -------------------------------
        # Option 2: Generate dummy regressors
        # -------------------------------
        last_row = train_prophet.iloc[-1]

        # Fill weather-related regressors with last known values
        for reg in meta["regressors"]:
            if reg in ["is_holiday", "is_weekend"]:
                continue
            future[reg] = last_row[reg]

        # Add holiday flag using Python holidays
        india_holidays = holidays.India(years=[2017])
        future["is_holiday"] = future["ds"].apply(
            lambda d: 1 if d in india_holidays else 0
        )

        # Add weekend flag
        future["is_weekend"] = future["ds"].dt.weekday >= 5

    # Step 2: Forecast
    forecast = model.predict(future)

    # Step 3: Return only requested periods
    forecast = forecast.tail(periods)

    return forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].to_dict(orient="records")


# -------------------------------
# Weather Endpoint (using real data)
# -------------------------------
@app.get("/weather")
def get_weather():
    """
    Returns weather data from the provided CSV file.
    """
    
    if not os.path.exists("weather_holiday_2017.csv"):
        return {"error": "weather_holiday_2017.csv not found."}, 404

    weather_data = pd.read_csv("weather_holiday_2017.csv")
    weather_data.rename(columns={'Datetime': 'time'}, inplace=True)
    

    # Convert relevant columns to numeric format
    weather_data['temperature'] = pd.to_numeric(weather_data['temperature'], errors='coerce')
    weather_data['humidity'] = pd.to_numeric(weather_data['humidity'], errors='coerce')
    weather_data['cloud_cover'] = pd.to_numeric(weather_data['cloud_cover'], errors='coerce')
    
    
    
    # Return all available weather data
    return weather_data[['time', 'temperature', 'humidity', 'cloud_cover']].to_dict(orient='records')


# -------------------------------
# Holidays Endpoint (using real data)
# -------------------------------
@app.get("/holidays")
def get_holidays():
    """
    Returns a list of holidays in India for 2017, including Jharkhand state holidays.
    """
    # Use the same logic as the forecast model to find holidays
    india_holidays = holidays.India(years=[2017], state='JH')
    
    holiday_list = []
    for date, name in sorted(india_holidays.items()):
        is_weekend = date.weekday() >= 5
        holiday_list.append({
            "date": date.strftime("%Y-%m-%d"),
            "holiday_name": name,
            "is_weekend": is_weekend
        })
    
    return holiday_list

# -------------------------------
# Root Endpoint
# -------------------------------
@app.get("/")
def home():
    return {"message": "Power Consumption Forecast API is running!"}
