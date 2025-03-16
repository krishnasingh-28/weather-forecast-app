from flask import Flask, request
import requests
import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

# Define API base URL
base_url = "http://api.weatherapi.com"

def get_past_7_days_weather(location: str):
    today = datetime.today().strftime("%Y-%m-%d")
    seven_days_back = (datetime.today() - timedelta(days=7)).strftime("%Y-%m-%d")
    
    params = {
        "key": os.environ.get("OPENWEATHER_API_KEY"),
        "q": location,
        "dt": seven_days_back,
        "end_dt": today
    }
    
    response = requests.get(f"{base_url}/v1/history.json", params=params)
    response.raise_for_status()
    
    return response.json()

def get_df(jsondata):
    features = ['hour', 'day', 'month', 'humidity', 'pressure_mb', 'cloud']
    target = "temp_c"
    data = []

    for forecastday in jsondata.get("forecast", {}).get("forecastday", []):
        for hour in forecastday.get("hour", []):
            dt = datetime.strptime(hour.get('time'), "%Y-%m-%d %H:%M")
            data.append({
                "hour": dt.hour,
                "day": dt.day,
                "month": dt.month,
                "humidity": hour.get("humidity"),
                "pressure_mb": hour.get("pressure_mb"),
                "cloud": hour.get("cloud"),
                "temp_c": hour.get("temp_c")
            })
    
    return pd.DataFrame(data)

def train_model(df):
    X = df[['hour', 'day', 'month', 'humidity', 'pressure_mb', 'cloud']].values
    Y = df['temp_c'].values
    
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    return model

def predict_temperature(location: str, date: str):
    jsondata = get_past_7_days_weather(location)
    df = get_df(jsondata)
    model = train_model(df)
    
    dt = datetime.strptime(date, "%Y-%m-%d")
    prediction_data = []
    for hour in range(24):
        prediction_data.append([hour, dt.day, dt.month, df['humidity'].mean(), df['pressure_mb'].mean(), df['cloud'].mean()])
    
    prediction_data = np.array(prediction_data)
    predictions = model.predict(prediction_data)
    
    avg_temp = np.mean(predictions)
    print(f"Predicted average temperature for {location} on {date}: {avg_temp:.2f}°C")
    
    return avg_temp


### Flask Configuration

app = Flask(__file__)


# Predict Route
@app.route("/api/predict")
def predict():
    # Example usage
    location = request.args.get("location")
    days = int(request.args.get("days"))

    if days > 7:
        return {"detail": "Days greater than 7, we support prediction for only 7 or less than 7 days"}

    result = []
    for i in range(1, days+1):
        date = (datetime.today() + timedelta(days=i)).strftime("%Y-%m-%d")
        response = predict_temperature(location, date)
        result.append(response)
    return result


# Ping Route
@app.route("/api/ping")
def ping_view():
    return "Hello World"


if __name__ == "__main__":
    app.run(port=9001)


## Test on your browser: http://127.0.0.1:9001/api/predict?location=chennai&days=2