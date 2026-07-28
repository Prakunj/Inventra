import os
import requests

from dotenv import load_dotenv
from utils.config import REGION_CITY

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")


class WeatherService:

    @staticmethod
    def get_weather(region: str):

        city = REGION_CITY.get(region)

        if not city:
            return {"error": "Unknown region"}

        response = requests.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params={
                "q": city,
                "appid": API_KEY,
                "units": "metric",
            },
            timeout=10,
        )


        if response.status_code != 200:
            return {"error": "Unable to fetch weather"}

        data = response.json()

        return {
            "city": city,
            "region": region,
            "temperature": data["main"]["temp"],
            "condition": data["weather"][0]["main"],
            "humidity": data["main"]["humidity"],
        }