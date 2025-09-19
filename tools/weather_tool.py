import requests
from pydantic import BaseModel
from typing import Optional
from config.config import OPENWEATHER_API_KEY


class WeatherOutput(BaseModel):
    temperature: float
    description: str
    humidity: int
    wind_speed: float
    unit: str = " Celsius"
    

def get_weather(location: str) -> Optional[WeatherOutput]:
    if not OPENWEATHER_API_KEY:
        print("Error: OPENWEATHER_API_KEY is not set.")
        return None
    
    base_url = "http//api.openweathermap.org/data/2.5/weather"

    params = {
        "q" : location,
        "appid" : OPENWEATHER_API_KEY,
        "units" : "metric"

    }
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()  

        return WeatherOutput(
            temperature = data["main"]["temp"],
            description = data["weather"][0]["description"],
            humidity = data["main"]["humidity"],
            wind_speed = data["wind"]["speed"]
        )
    
    except requests.expections.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None
    except (KeyError, IndexError) as e:
        print(f"Error parsing weather data: {e}")
        return None

        res = requests.get(base_url, params=params)
        res.raise_for_status()
        data = res.json()

        weather = WeatherOutput(
            temperature = data["main"]["temp"],
            description = data["weather"][0]["description"],
            humidity = data["main"]["humidity"],
            wind_speed = data["wind"]["speed"]
        )
        return weather
