import requests
import mysql.connector
from dotenv import load_dotenv
import os
import datetime

dotenv_path = os.path.join(os.path.dirname(__file__), ".env", ".env")
load_dotenv(dotenv_path)

db_username = os.getenv("DB_USERNAME")
db_password = os.getenv("DB_PASSWORD")

def get_latlong_by_zipcode(zipcode, api_key):
    url = f"http://api.openweathermap.org/geo/1.0/zip?zip={zipcode}&appid={api_key}&units=imperial"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Error: Received status code {response.status_code}")

    data = response.json()
    return data["lat"], data["lon"]


def get_weather_info(lat, lon, api_key):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=imperial"
    res = requests.get(url)

    if res.status_code != 200:
        raise Exception(f"Error: Received status code {res.status_code}")

    data = res.json()
    return data["dt"], data["name"], data["main"]["temp"], data["main"]["feels_like"]


def insert_into_db(date, city_name, current_temp, feels_like):
    try:
        conn = mysql.connector.connect(
            host="localhost", user=db_username, password=db_password, database="weather"
        )
    except mysql.connector.Error as err:
        print(f"Database conection error: {err}")

    cursor = conn.cursor()

    query = "INSERT INTO weather_info (date, city_name, current_temp, feels_like) VALUES (%s, %s, %s, %s)"
    val = (date, city_name, current_temp, feels_like)

    cursor.execute(query, val)
    conn.commit()


if __name__ == "__main__":
    api_key = os.getenv("API_KEY")
    zip_codes = [78660, 94501, 76040, 75001, 75002]

    for zip_code in zip_codes:
        latitude, longitude = get_latlong_by_zipcode(zip_code, api_key)
        if latitude and longitude:
            timestamp, city_name, current_temp, feels_like = get_weather_info(
                latitude, longitude, api_key
            )
            if timestamp and city_name and current_temp and feels_like:
                formated_date = datetime.datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d")
                insert_into_db(formated_date, city_name, current_temp, feels_like)
            else:
                print(f"Failed to fetch data for {zip_code}")
    print(f"***Weather data added successfully.***")
