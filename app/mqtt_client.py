import json
import paho.mqtt.client as mqtt
from app.config import settings
from app.db import SessionLocal
from app import crud

# Dicionário global para armazenar o estado atual
estados_atualizados = {}

def categorize_message(topic: str, payload_obj: dict | None) -> str:
    t = topic.lower()
    if "prod" in t or "production" in t or (payload_obj and ("production" in payload_obj or "produto" in payload_obj)):
        return "production"
    if "estoque" in t or "stock" in t or (payload_obj and ("stock" in payload_obj or "estoque" in payload_obj)):
        return "stock"
    env_keys = {"temperature", "temp", "humidity", "umidade", "co2", "press"}
    if payload_obj and any(k in payload_obj for k in env_keys):
        return "environmental"
    return "other"

def extract_numeric(payload_obj: dict | None) -> float | None:
    if not payload_obj:
        return None
    for k in ("value","valor","temperature","temp","humidity","umidade","production","quantidade","qtd"):
        if k in payload_obj:
            try:
                return float(payload_obj[k])
            except Exception:
                continue
    return None

def on_connect(client, userdata, flags, rc):
    print(f"[MQTT] conectado com rc={rc}")
    topics = settings.MQTT_TOPICS.split(",")
    for t in topics:
        t = t.strip()
        if t:
            client.subscribe(t)
            print(f"[MQTT] inscrito em: {t}")

def on_message(client, userdata, msg):
    try:
        raw = msg.payload.decode("utf-8")
    except Exception:
        raw = str(msg.payload)

    payload_obj = None
    try:
        payload_obj = json.loads(raw)
    except Exception:
        payload_obj = None

    # Atualiza o estado atual
    if payload_obj and "variable" in payload_obj and "value" in payload_obj:
        estados_atualizados[payload_obj["variable"]] = payload_obj["value"]
        print(f"[MQTT] Atualizado estados_atualizados: {estados_atualizados}")

    # Persist no banco
    db = SessionLocal()
    try:
        crud.create_message(db, topic=msg.topic, payload=payload_obj, raw=raw,
                            category=categorize_message(msg.topic, payload_obj),
                            numeric_value=extract_numeric(payload_obj))
        print(f"[MQTT] mensagem salva: topic={msg.topic}")
    except Exception as e:
        print(f"[MQTT] erro salvando mensagem: {e}")
    finally:
        db.close()

def start_mqtt_client():
    client = mqtt.Client()
    if settings.MQTT_USERNAME:
        client.username_pw_set(settings.MQTT_USERNAME, settings.MQTT_PASSWORD)
    client.on_connect = on_connect
    client.on_message = on_message
    client.tls_set()  # ativa TLS padrão
    client.connect(settings.MQTT_BROKER, settings.MQTT_PORT)
    client.loop_start()
    return client
