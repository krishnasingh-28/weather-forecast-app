import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# Sample Data (Replace with your actual 7-day weather data)
data = {
    "Day": [1, 2, 3, 4, 5, 6, 7],  # Last 7 days
    "Temperature": [5.4, 6.1, 7.3, 6.8, 5.9, 6.5, 7.1]  # Avg temperatures
}

df = pd.DataFrame(data)

# Feature & Target Variables
X = df[["Day"]]  # Independent variable (Day)
y = df["Temperature"]  # Dependent variable (Temperature)

# Train the model
model = LinearRegression()
model.fit(X, y)

# Predict for the next day (Day 8)
future_day = np.array([[8]])
predicted_temp = model.predict(future_day)

print(f"📌 Predicted Temperature for Day 8: {predicted_temp[0]:.2f}°C")

# Plot the results
plt.scatter(df["Day"], df["Temperature"], color="blue", label="Actual Temperature")
plt.plot(df["Day"], model.predict(X), color="red", linestyle="--", label="Model Prediction")
plt.scatter(future_day, predicted_temp, color="green", marker="o", label="Forecasted Temp")
plt.xlabel("Days")
plt.ylabel("Temperature (°C)")
plt.legend()
plt.show()
