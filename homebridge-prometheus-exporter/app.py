import os
import sys
import logging

from flask import Flask
from flask_apscheduler import APScheduler
from prometheus_client import Gauge
from prometheus_flask_exporter import PrometheusMetrics

from homebridge import HomeBridge

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class Config:
    SCHEDULER_API_ENABLED = True
    HOMEBRIDGE_USERNAME = os.environ.get("HOMEBRIDGE_USERNAME", "")
    HOMEBRIDGE_PASSWORD = os.environ.get("HOMEBRIDGE_PASSWORD", "")
    HOMEBRIDGE_URL = os.environ.get("HOMEBRIDGE_URL", "")
    SCHEDULE_MINUTES = int(os.environ.get("SCHEDULE_MINUTES", "5"))
    SCHEDULE_MISFIRE_GRACE_SECONDS = int(
        os.environ.get("SCHEDULE_MISFIRE_GRACE_SECONDS", "900")
    )


REQUIRED_ENV_VARS = ["HOMEBRIDGE_USERNAME", "HOMEBRIDGE_PASSWORD", "HOMEBRIDGE_URL"]

for item in REQUIRED_ENV_VARS:
    if getattr(Config, item) == "":
        logger.error(f"{item} must be set!")
        sys.exit(1)

homebridge = HomeBridge(
    Config.HOMEBRIDGE_URL, Config.HOMEBRIDGE_USERNAME, Config.HOMEBRIDGE_PASSWORD
)

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


@scheduler.task(
    "interval",
    id="fetch_accessories",
    minutes=Config.SCHEDULE_MINUTES,
    misfire_grace_time=Config.SCHEDULE_MISFIRE_GRACE_SECONDS,
)
def fetch_accessories():
    logger.info("Fetching accessories data from %s", Config.HOMEBRIDGE_URL)
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
