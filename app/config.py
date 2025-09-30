import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # MQTT
    MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")
    MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
    MQTT_USERNAME = os.getenv("MQTT_USERNAME") or None
    MQTT_PASSWORD = os.getenv("MQTT_PASSWORD") or None
    MQTT_TOPICS = os.getenv("MQTT_TOPICS", "#")  # comma separated

    # DB
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = int(os.getenv("DB_PORT", "3306"))
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASS = os.getenv("DB_PASS", "admin")
    DB_NAME = os.getenv("DB_NAME", "iot_db")

    # App
    APP_HOST = os.getenv("APP_HOST", "0.0.0.0")
    APP_PORT = int(os.getenv("APP_PORT", "8000"))

settings = Settings()
