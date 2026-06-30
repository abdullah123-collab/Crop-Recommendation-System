import requests


def get_weather_data(city: str, api_key: str) -> dict:
    """Fetch weather values from OpenWeatherMap and return temperature, humidity, and rainfall."""
    city = city.strip()
    if not city:
        return {"error": "Please enter a city name."}
    if not api_key:
        return {"error": "OpenWeatherMap API key is required."}

    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": api_key, "units": "metric"}

    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        if response.status_code != 200:
            return {"error": data.get("message", "Unable to fetch weather data.")}

        main = data.get("main", {})
        rain = data.get("rain", {}).get("1h", 0.0) or data.get("rain", {}).get("3h", 0.0) or 0.0
        return {
            "temperature": round(main.get("temp", 0.0), 2),
            "humidity": int(main.get("humidity", 0)),
            "rainfall": round(rain, 2),
            "city": data.get("name", city.title()),
        }
    except requests.exceptions.RequestException as exc:
        return {"error": f"Could not fetch weather: {exc}"}
