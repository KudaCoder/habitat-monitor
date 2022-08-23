from datetime import datetime, time
from dotenv import load_dotenv
import requests
import json
import os

load_dotenv()
API_URL = os.environ.get("API_URL", "http://habitat-api:8000/api")


def convert_dt_to_iso(data):
    for k, v in data.items():
        if isinstance(v, datetime) or isinstance(v, time):
            data[k] = v.isoformat()
    return data


def add_reading(temperature=None, humidity=None):
    resp = requests.post(
        f"{API_URL}/reading/",
        json={"temperature": temperature, "humidity": humidity},
    )
    if resp.status_code == 201:
        return resp.json()


def get_reading():
    resp = requests.get(f"{API_URL}/reading/")
    if resp.status_code == 200:
        return resp.json()


def filter_readings(period=None, unit=None, date_from=None, date_to=None):
    data = {}
    if period is not None:
        data.update({"period": period, "unit": unit})
    elif date_from is not None:
        data.update({"date_from": date_from, "date_to": date_to})

    resp = requests.get(f"{API_URL}/readings/", json=data)
    if resp.status_code == 200:
        return resp.json()


def get_config():
    resp = requests.get(f"{API_URL}/config/")
    if resp.status_code == 200:
        return resp.json()


def set_config(data):
    data = convert_dt_to_iso(data)
    resp = requests.post(f"{API_URL}/config/", json=data)
    print(resp.json())
    if resp.status_code == 201:
        return resp.json()


def new_config():
    resp = requests.get(f"{API_URL}/config/new/")
    if resp.status_code == 200:
        return resp.json()
