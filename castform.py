import os
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
castform = forecast_to_castform_form(get_weather_forecast(CITY_COORDINATES_DICT[CITY]))
print(castform)


opts = Options()
opts.add_argument("--no-sandbox")
opts.add_experimental_option("excludeSwitches", ['enable-automation'])
driver = webdriver.Chrome(options=opts)


def open_castform_gif(castform: str) -> None:
    driver.get(f"file://{os.getcwd()}/assets/{castform}.gif")
    driver.fullscreen_window()
    elem = driver.find_element(By.TAG_NAME, "img")
    print(elem)
    driver.execute_script("arguments[0].style.removeProperty('background-color');", elem)
    driver.execute_script("document.body.style.zoom='900%'")


while True:
    open_castform_gif(forecast_to_castform_form(
        get_weather_forecast(CITY_COORDINATES_DICT[CITY])))
    time.sleep(15 * 60)
