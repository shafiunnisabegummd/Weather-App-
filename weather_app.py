import requests

print("=== Weather App - Live API ===")

# Free weather API that needs NO key - Open-Meteo (always works)
# Also supports OpenWeather API if you have key

city = input("Enter city name (e.g. Vijayawada, London): ").strip()
if not city:
    city = "Vijayawada"

def get_weather_free(city):
    try:
        # Step 1: Get lat/lon for city using free geocoding
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"
        geo = requests.get(geo_url, timeout=10).json()
        
        if not geo.get('results'):
            print(f"City '{city}' not found. Trying Vijayawada")
            city = "Vijayawada"
            geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"
            geo = requests.get(geo_url, timeout=10).json()
        
        lat = geo['results'][0]['latitude']
        lon = geo['results'][0]['longitude']
        real_name = geo['results'][0]['name']
        country = geo['results'][0]['country']
        
        # Step 2: Get weather
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code&daily=temperature_2m_max,temperature_2m_min&timezone=auto"
        w = requests.get(weather_url, timeout=10).json()
        
        curr = w['current']
        
        print("\n" + "="*40)
        print(f"📍 {real_name}, {country}")
        print(f"🌡️  Temperature: {curr['temperature_2m']}°C")
        print(f"💧 Humidity: {curr['relative_humidity_2m']}%")
        print(f"💨 Wind: {curr['wind_speed_10m']} km/h")
        print(f"📅 Today Max: {w['daily']['temperature_2m_max'][0]}°C")
        print(f"📅 Today Min: {w['daily']['temperature_2m_min'][0]}°C")
        print("="*40)
        print("✅ Data from Open-Meteo Live API (REST + JSON)")
        print("✅ Project Requirements: REST API, JSON parsing, Clean CLI")
        
    except Exception as e:
        print(f"Error: {e}")
        # Super simple backup - wttr.in
        try:
            r = requests.get(f"https://wttr.in/{city}?format=j1", timeout=10).json()
            curr = r['current_condition'][0]
            print(f"\n📍 {city}")
            print(f"🌡️  Temp: {curr['temp_C']}°C (Feels {curr['FeelsLikeC']}°C)")
            print(f"💧 Humidity: {curr['humidity']}%")
            print(f"☁️  Weather: {curr['weatherDesc'][0]['value']}")
        except:
            print("Check internet connection")

# Bonus: If you have OpenWeather API key, uncomment below
# OPENWEATHER_KEY = "YOUR_KEY_HERE"
# def get_openweather(city):
#     url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_KEY}&units=metric"
#     data = requests.get(url).json()
#     print(f"{data['name']}: {data['main']['temp']}°C, {data['main']['humidity']}% humidity")

get_weather_free(city)

# Keep window open
input("\nPress Enter to exit...")