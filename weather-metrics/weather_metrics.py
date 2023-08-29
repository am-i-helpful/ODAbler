# Import Meteostat library and dependencies
from datetime import datetime, timezone
import time
from bs4 import BeautifulSoup
import requests
import json
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS


def generate_weather_data():
    # hint taken from https://www.makeuseof.com/python-live-weather-data/
    try:
        with open('../influxdb-config.json') as config_file:
            data = json.load(config_file)
            city_name = data['location'] + " weather"
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
        }
        url = f'https://www.google.com/search?q={city_name}&oq={city_name}&aqs=chrome.0.35i39l2j0l4j46j69i60.6128j1j7&sourceid=chrome&ie=UTF-8&hl=en'
        res = requests.get(
            url,
            headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        location = data['location']
        time = soup.select('#wob_dts')[0].getText().strip()
        info = soup.select('#wob_dc')[0].getText().strip()
        temperature = soup.select('#wob_tm')[0].getText().strip()
        humidity = soup.select('#wob_hm')[0].getText().strip()
        # print("Location: " + location)
        # print("Temperature: " + temperature + "°C")
        # print("Time: " + time)
        # print("Weather Description: " + info)
        # print("Humidity: "+humidity)
        write_weather_info_to_database(location, temperature, humidity)
    except Exception as e:
           # print("There was some problem getting the weather data!")
           print(e)


# source - https://docs.influxdata.com/influxdb/cloud/api-guide/client-libraries/python/
def write_weather_info_to_database(location, temperature, humidity):
    measurement = "weather"
    with open('../influxdb-config.json') as config_file:
        data = json.load(config_file)
        bucket = data['bucket']
        org = data['org']
        token = data['token']
        url = data['url']
    client = influxdb_client.InfluxDBClient(
        url=url,
        token=token,
        org=org
    )
    # Write script
    write_api = client.write_api(write_options=SYNCHRONOUS)
    p1 = influxdb_client.Point(measurement).tag("location", location).field("temperature", value=temperature) # value_b=weather_description)
    p2 = influxdb_client.Point(measurement).tag("location", location).field("humidity", value=humidity)
    write_api.write(bucket=bucket, org=org, record=[p1,p2])


if __name__ == '__main__':
    for i in range(10):
        generate_weather_data()
        time.sleep(1)