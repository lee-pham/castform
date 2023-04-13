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


# class Forecast:
#     def __init__(self, short_forecast: str, temperature: int, wind_speed: int):
#         self.short_forecast = short_forecast
#         self.temperature = temperature
#         self.wind_speed = wind_speed


class NationalWeatherServiceAPICaller:
    city_endpoint_cache = {}

    @staticmethod
    def get_grid_endpoint_by_coordinates(coordinates: str) -> str:
        r = requests.get(f"https://api.weather.gov/points/{coordinates}")
        r.raise_for_status()
        return r.json()["properties"]["forecast"]

    def get_forecast(self, city: str) -> str:
        if city not in self.city_endpoint_cache:
            self.city_endpoint_cache[city] = self.get_grid_endpoint_by_coordinates(
                CITY_COORDINATES_DICT[city])
        retries = 5
        for attempt in range(retries):
            try:
                r = requests.get(self.city_endpoint_cache[city])
                r.raise_for_status()
                t = r.json()
                print(t)
                short_forecast = t["properties"]["periods"][0]["shortForecast"]
                return short_forecast
            except Exception as e:
                print(e)
                minutes_to_wait = 20
                print(f"Retrying in {minutes_to_wait} minutes")
                time.sleep(minutes_to_wait * 60)

        return "retry limit reached. don't know how you got this far chief"


def forecast_to_castform_form(forecast: str) -> str:
    normal_list = ["cloudy"]
    sunny_list = ["sunny"]
    rainy_list = ["rain", "shower", "storm"]
    snowy_list = ["snow", "ice"]
    forecast = forecast.lower()
    print(forecast)
    if any(keyword in forecast for keyword in normal_list):
        return "normal"

    elif any(keyword in forecast for keyword in rainy_list):
        return "rainy"

    elif any(keyword in forecast for keyword in snowy_list):
        return "snowy"

    elif any(keyword in forecast for keyword in sunny_list):
        return "sunny"

    return "normal"


night = [
    9 + 12,
    10 + 12,
    11 + 12,
    0,
    1,
    2,
    3,
    4,
    5,
    6,
    7
]

twilight = [
    8,
    9,
    10,
    6 + 12,
    7 + 12,
    8 + 12
]

day = [
    11,
    12,
    1 + 12,
    2 + 12,
    3 + 12,
    4 + 12,
    5 + 12
]


def is_golden_hour(sunrise_time, sunset_time) -> bool:
    current_time = datetime.datetime.now().time()
    print(current_time, sunrise_time, sunset_time)
    sunrise_golden_hour_end = datetime.time(
        sunrise_time.hour + 1, sunrise_time.minute)
    sunrise_golden_hour = sunrise_time <= current_time <= sunrise_golden_hour_end

    sunset_golden_hour_begin = datetime.time(
        sunset_time.hour - 1, sunset_time.minute)
    sunset_golden_hour = sunset_golden_hour_begin <= current_time <= sunset_time

    golden_hour = sunrise_golden_hour or sunset_golden_hour
    if golden_hour:
        print("~GOLDEN HOUR~")

    return golden_hour


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
    if any(keyword in forecast for keyword in jolten_list):
        eeveelution = "jolteon"

    elif any(keyword in forecast for keyword in vaporeon_list):
        eeveelution = "vaporeon"

    elif any(keyword in forecast for keyword in glaceon_list):
        eeveelution = "glaceon"

    elif any(keyword in forecast for keyword in leafeon_list):
        eeveelution = "leafeon"

    if is_golden_hour(datetime.time(hour=7, minute=8), datetime.time(hour=7 + 12, minute=55)):
        return "sylveon"

    current_hour = datetime.datetime.now().hour
    print(current_hour)
    if eeveelution != "eevee":
        return eeveelution
    elif current_hour in day:
        return "espeon"
    elif current_hour in night:
        return "umbreon"

    return eeveelution


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
    driver.execute_script(
        "arguments[0].style.removeProperty('background-color');", elem)
    driver.execute_script(
        "arguments[0].style.setProperty('object-fit', 'contain');", elem)
    driver.execute_script(
        "arguments[0].style.setProperty('height', '720px');", elem)
    driver.execute_script(
        "arguments[0].style.setProperty('width', '720px');", elem)


nws_api_caller = NationalWeatherServiceAPICaller()
while True:
    # open_gif(
    #     forecast_to_castform_form(
    #         nws_api_caller.get_forecast(CITY)),
    #     "castform"
    #     )
    open_gif(
        forecast_to_eeveelution(
            nws_api_caller.get_forecast(CITY)),
        "eevees"
    )
    elem = driver.find_element(By.TAG_NAME, "img")
    t_end = time.time() + 60 * 10
    while time.time() < t_end:
        driver.execute_script(
            "arguments[0].style.setProperty('transform', 'scaleX(-1)');", elem)
        time.sleep(random.randint(2, 15))
        driver.execute_script(
            "arguments[0].style.setProperty('transform', 'scaleX(1)');", elem)
        time.sleep(random.randint(2, 15))
