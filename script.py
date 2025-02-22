import requests
import datetime

# Replace with your API key
API_KEY = "" # API key from weather api . com 
LOCATION = "London"
BASE_URL = "https://api.weatherapi.com/v1/history.json"

# Get the last 7 days
def get_last_7_days_weather():
    today = datetime.date.today()
    
    for i in range(7):
        date = today - datetime.timedelta(days=i)  # Get past date
        formatted_date = date.strftime("%Y-%m-%d")
        
        print(f"\n📅 Fetching data for {formatted_date}...\n")
        
        # API Request
        params = {
            "key": API_KEY,
            "q": LOCATION,
            "dt": formatted_date,
        }

        try:
            response = requests.get(BASE_URL, params=params)
            response.raise_for_status()  # Raises an error for HTTP failures (400, 500, etc.)
            data = response.json()

            # Extract relevant weather details
            if "forecast" in data:
                day_weather = data["forecast"]["forecastday"][0]["day"]
                
                print(f"📍 Location: {LOCATION}")
                print(f"🌡️ Temperature: {day_weather['avgtemp_c']}°C")
                print(f"☀️ Condition: {day_weather['condition']['text']}")
                print(f"💧 Humidity: {day_weather['avghumidity']}%")
                print(f"💨 Wind Speed: {day_weather['maxwind_kph']} kph")
                print("-" * 40)
            else:
                print("⚠️ No weather data found for this date.")
        
        except requests.exceptions.RequestException as e:
            print(f"❌ API Error: {e}")
        except KeyError as ke:
            print(f"❌ Missing key in JSON response: {ke}")

# Run the function
get_last_7_days_weather()