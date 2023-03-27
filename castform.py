import requests

CITY = "Round Rock, TX"
CITY_COORDINATES_DICT = {
    "Round Rock, TX": "30.57208203598085,-97.6556805597923"
}

ENDPOINT = "https://api.weather.gov"


def get_grid_endpoint_by_coordinates(coordinates: str) -> str:
    r = requests.get(f"{ENDPOINT}/points/{CITY_COORDINATES_DICT[CITY]}")
    return r.json()["properties"]["forecast"]


def get_weather_forecast(city: str) -> str:
    r = requests.get(get_grid_endpoint_by_coordinates(CITY_COORDINATES_DICT[CITY]))
    t = r.json()
    short_forecast = t["properties"]["periods"][0]["shortForecast"]
    return short_forecast


def forecast_to_castform_form(forecast: str) -> str:
    normal_list = ["cloudy"]
    sunny_list = ["sunny"]
    rainy_list = ["rain", "shower", "storm"]
    snowy_list = ["snow", "ice"]
    forecast = forecast.lower()
    if any(keyword in forecast for keyword in normal_list):
        return "normal"
    
    elif any(keyword in forecast for keyword in sunny_list):
        return "sunny"
    
    elif any(keyword in forecast for keyword in rainy_list):
        return "rainy"

    elif any(keyword in forecast for keyword in snowy_list):
        return "snowy"
    
    return "normal"


print(f"{CITY}: {get_weather_forecast(CITY_COORDINATES_DICT[CITY])}")
print(forecast_to_castform_form(get_weather_forecast(CITY_COORDINATES_DICT[CITY])))
