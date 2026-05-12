import asyncio
import websockets
import json

class WebSocketClient:
    def __init__(self):
        self.connection = None
    async def connect(self, url):
        try:
            # Встановлюємо тайм-аут підключення 10 секунд
            self.connection = await asyncio.wait_for(websockets.connect(url), timeout=10)
            print(f"Підключено до: {url}")
        except asyncio.TimeoutError:
            print("Помилка: Тайм-аут підключення.")
        except Exception as e:
            print(f"Помилка підключення: {e}")
            self.connection = None
    async def send_message(self, message):
        if self.connection:
            try:
                # Якщо надсилаємо словник, конвертуємо в JSON
                data = json.dumps(message) if isinstance(message, dict) else message
                await self.connection.send(data)
                print(f"Надіслано: {data}")
            except Exception as e:
                print(f"Помилка при відправленні: {e}")
        else:
            print("З'єднання відсутнє.")
    async def receive_message(self):
        if self.connection:
            try:
                message = await self.connection.recv()
                return message
            except Exception as e:
                print(f"Помилка при отриманні: {e}")
                return None
        return None
    async def close_connection(self):
        if self.connection:
            await self.connection.close()
            print("З'єднання закрито.")

async def main():
    client = WebSocketClient()
    # Використовуємо стабільний потік даних Binance (ціна BTC/USDT)
    uri = "wss://stream.binance.com:9443/ws/btcusdt@trade"
    await client.connect(uri)

    if client.connection:
        print("Чекаємо на повідомлення від сервера (ринок BTC)...")
        # Отримуємо реальні дані з біржі
        data = await client.receive_message()
        if data:
            # Парсимо JSON для красивого виводу
            js = json.loads(data)
            print(f"Отримана ціна BTC: {js['p']} USD")
        await client.close_connection()

if __name__ == "__main__":
    asyncio.run(main())