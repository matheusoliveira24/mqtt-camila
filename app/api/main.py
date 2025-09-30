from fastapi import FastAPI
from app.mqtt_client import start_mqtt_client, estados_atualizados

app = FastAPI(title="API IoT Bancada Camila")

# Inicializa MQTT assim que a API começa
@app.on_event("startup")
def startup_event():
    start_mqtt_client()
    print("[MQTT] Cliente MQTT iniciado junto com a API")

# Rota para ver todas as variáveis
@app.get("/estados")
def get_estados():
    return {"estados": estados_atualizados}

# Rota para ver uma variável específica
@app.get("/estados/{variavel}")
def get_estado(variavel: str):
    if variavel in estados_atualizados:
        return {variavel: estados_atualizados[variavel]}
    return {"erro": f"Variável '{variavel}' não encontrada"}
