import datetime
import os
import random
import requests
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


CITY = "Round Rock, TX"
CITY_COORDINATES_DICT = {
    "Round Rock, TX": "30.57208203598085,-97.6556805597923"
}

ENDPOINT = "https://api.weather.gov"

city_endpoint_cache = {}

def get_grid_endpoint_by_coordinates(coordinates: str) -> str:
    r = requests.get(f"{ENDPOINT}/points/{CITY_COORDINATES_DICT[CITY]}")
    r.raise_for_status()
    return r.json()["properties"]["forecast"]


def get_weather_forecast_for_city(city: str) -> str:
    if city not in city_endpoint_cache:
        city_endpoint_cache[city] = get_grid_endpoint_by_coordinates(CITY_COORDINATES_DICT[city])
    r = requests.get(city_endpoint_cache[city])
    r.raise_for_status()
    t = r.json()
    short_forecast = t["properties"]["periods"][0]["shortForecast"]
    return short_forecast


def forecast_to_castform_form(forecast: str) -> str:
    normal_list = ["cloudy"]
    sunny_list = ["sunny"]
    rainy_list = ["rain", "shower", "storm"]
    snowy_list = ["snow", "ice"]
    forecast = forecast.lower()
    print(forecast)
    if any(keyword in forecast for keyword in normal_list):
        return "normal"

    elif any(keyword in forecast for keyword in sunny_list):
        return "sunny"

    elif any(keyword in forecast for keyword in rainy_list):
        return "rainy"

    elif any(keyword in forecast for keyword in snowy_list):
        return "snowy"

    return "normal"



night = [11 + 12,
         0,
         1,
         2,
         3,
         4,
         5]
twilight = [6,
            7,
            8,
            9,
            7 + 12,
            8 + 12,
            9 + 12,
            10 + 12]
day = [10,
       11,
       12,
       1 + 12,
       2 + 12,
       3 + 12,
       4 + 12,
       5 + 12,
       6 + 12]


def forecast_to_eeveelution(forecast: str) -> str:
    eevee_list = ["cloudy"]
    espeon_list = ["sunny"]
    vaporeon_list = ["rain", "shower"]
    jolten_list = ["storm"]
    glaceon_list = ["snow", "ice"]
    leafeon_list = ["windy"]
    forecast = forecast.lower()
    print(forecast)
    eeveelution = "eevee"
    if any(keyword in forecast for keyword in eevee_list):
        eeveelution = "eevee"

    elif any(keyword in forecast for keyword in espeon_list):
        eeveelution = "espeon"

    elif any(keyword in forecast for keyword in vaporeon_list):
        eeveelution = "vaporeon"

    elif any(keyword in forecast for keyword in glaceon_list):
        eeveelution = "glaceon"
    
    elif any(keyword in forecast for keyword in jolten_list):
        eeveelution = "jolteon"
    
    elif any(keyword in forecast for keyword in leafeon_list):
        eeveelution = "leafeon"

    current_hour = datetime.datetime.now().hour
    print(current_hour)
    if eeveelution != "eevee":
        return eeveelution
    elif current_hour in day:
        return "espeon"
    elif current_hour in night:
        return "umbreon"
    
    return eeveelution
    

forecast = get_weather_forecast_for_city(CITY)
print(f"{CITY}: {forecast}")
castform = forecast_to_castform_form(forecast)
print(castform)


opts = Options()
opts.add_argument("--no-sandbox")
opts.add_experimental_option("excludeSwitches", ['enable-automation'])
driver = webdriver.Chrome(options=opts)


def open_gif(castform: str, type: str) -> None:
    print(castform)
    driver.get(f"file://{os.getcwd()}/assets/{type}/{castform}.gif")
    driver.fullscreen_window()
    elem = driver.find_element(By.TAG_NAME, "img")
    print(elem)
    driver.execute_script("arguments[0].style.removeProperty('background-color');", elem)
    driver.execute_script("document.body.style.zoom='900%'")


while True:
    # open_gif(
    #     forecast_to_castform_form(get_weather_forecast_for_city(CITY)),
    #     "castform"
    #     )
    open_gif(
        forecast_to_eeveelution(get_weather_forecast_for_city(CITY)),
        "eevees"
        )
    elem = driver.find_element(By.TAG_NAME, "img")
    t_end = time.time() + 60 * 30
    while time.time() < t_end:
        driver.execute_script("arguments[0].style.setProperty('transform', 'scaleX(-1)');", elem)
        time.sleep(random.randint(2, 15))
        driver.execute_script("arguments[0].style.setProperty('transform', 'scaleX(1)');", elem)
        time.sleep(random.randint(2, 15))
