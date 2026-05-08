import paho.mqtt.client as mqtt
import time
import requests
import websocket
import json
import threading

class MQTTClient:
    def __init__(self, broker_address="broker.hivemq.com", port=1883, username=None, password=None):
        self.broker_address = broker_address
        self.port = port
        # Вказуємо CallbackAPIVersion для версії paho-mqtt 2.0+
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        if username and password:
            self.client.username_pw_set(username, password)
    def connect(self):
        try:
            self.client.connect(self.broker_address, self.port)
            print(f"Підключено до брокера: {self.broker_address}")
            # Запуск циклу обробки в окремому потоці
            self.client.loop_start()
        except Exception as e:
            print(f"Помилка підключення: {e}")
    def publish(self, topic, message):
        result = self.client.publish(topic, str(message))
        status = result[0]
        if status == 0:
            print(f"Повідомлення '{message}' надіслано в тему '{topic}'")
        else:
            print(f"Не вдалося надіслати повідомлення в тему {topic}")
    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()
        print("Відключено від брокера.")



# Налаштування
TOPIC = "university/project/sensor_data"
API_URL = "https://api.coinbase.com/v2/prices/BTC-USD/spot"

def on_ws_message(ws, message):
    on_ws_message.ws = ws
    print(f"WebSocket отримав: {message}")
def run_websocket():
    ws = websocket.WebSocketApp("wss://echo.websocket.org", on_message=on_ws_message)
    ws.run_forever()
def main():
    # 1. Ініціалізація MQTT
    mqtt_cl = MQTTClient()
    mqtt_cl.connect()
    # 2. Запуск WebSocket у фоновому режимі
    ws_thread = threading.Thread(target=run_websocket, daemon=True)
    ws_thread.start()
    try:
        while True:
            # Крок 1: Отримання даних через REST API
            response = requests.get(API_URL)
            if response.status_code == 200:
                data = response.json()
                price = data['data']['amount']
                payload = json.dumps({
                    "timestamp": time.time(),
                    "symbol": "BTC",
                    "price": price
                })
                # Крок 2: Публікація через MQTT
                mqtt_cl.publish(TOPIC, payload)
                # Крок 3: Передача через WebSocket
                print(f"Дані підготовлені для WS: {payload}")
            time.sleep(7)  # Інтервал опитування 10 секунд
    except KeyboardInterrupt:
        print("\nЗупинка системи...")
    finally:
        mqtt_cl.disconnect()

if __name__ == "__main__":
    main()