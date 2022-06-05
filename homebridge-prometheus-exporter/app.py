import os
import sys
import logging

from flask import Flask
from flask_apscheduler import APScheduler
from prometheus_client import Gauge
from prometheus_flask_exporter import PrometheusMetrics

from homebridge import HomeBridge


class Config:
    SCHEDULER_API_ENABLED = True
    USERNAME = os.environ.get("HOMEBRIDGE_USERNAME", "")
    PASSWORD = os.environ.get("HOMEBRIDGE_PASSWORD", "")
    URL = os.environ.get("HOMEBRIDGE_URL", "")


if Config.USERNAME == "":
    print("HOMEBRIDGE_USERNAME must be set!")
    sys.exit(1)

if Config.PASSWORD == "":
    print("HOMEBRIDGE_PASSWORD must be set!")
    sys.exit(1)

if Config.URL == "":
    print("HOMEBRIDGE_URL must be set!")
    sys.exit(1)

homebridge = HomeBridge(Config.URL, Config.USERNAME, Config.PASSWORD)

logger = logging.getLogger(__name__)
app = Flask(__name__)
app.config.from_object(Config())

metrics = PrometheusMetrics(app)
temp_gauge = Gauge(
    "homebridge_temperature_celcius",
    "The temperature reported by the HomeKit TemperatureSensor accessory",
    labelnames=["serviceName", "uniqueId"],
)
humidity_gauge = Gauge(
    "homebridge_relative_humidity_percentage",
    "The relative humidity percentage reported by the HomeKit TemperatureSensor accessory",
    labelnames=["serviceName", "uniqueId"],
)

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()


@scheduler.task("interval", id="fetch_accessories", minutes=30, misfire_grace_time=900)
def fetch_accessories():
    logger.info("Fetching accessories data from %s", Config.URL)
    results = homebridge.get_accessories()

    for result in results:
        result_type = result["type"]
        labels = {
            "serviceName": result["serviceName"],
            "uniqueId": result["uniqueId"],
        }
        if result_type == "TemperatureSensor":
            temperature = result["values"]["CurrentTemperature"]
            temp_gauge.labels(**labels).set(temperature)
        elif result_type == "HumiditySensor":
            humidity = result["values"]["CurrentRelativeHumidity"]
            humidity_gauge.labels(**labels).set(humidity)


fetch_accessories()

if __name__ == "__main__":
    app.run()
