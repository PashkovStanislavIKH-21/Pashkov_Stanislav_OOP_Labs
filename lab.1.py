from abc import ABC, abstractmethod


# Завдання 1
class CallReport:
    def get_report_data(self):
        return "Звіт: Абонент А -> Абонент Б, 5 хв."
class ReportSaver:
    def save_to_file(self, data, filename):
        print(f"Збереження даних у файл {filename}: {data}")
class Subscriber:
    def __init__(self, name, phone):
        self.name = name
        self.phone = phone
class SMSMessenger:
    def send_sms(self, phone, message):
        print(f"SMS на {phone}: {message}")
class BillingSystem:
    def calculate_balance(self, subscriber_id):
        return 100.50


print("___Завдання 1___")
report = CallReport()
saver = ReportSaver()
data = report.get_report_data()
saver.save_to_file(data, "report.txt")

sub = Subscriber("Іван", "+38099")
sms = SMSMessenger()
sms.send_sms(sub.phone, "Привіт!")



# Завдання 2
class Tariff(ABC):
    @abstractmethod
    def calculate_cost(self, usage):
        pass
class VoiceTariff(Tariff):
    def calculate_cost(self, usage): return usage * 0.5
class DataTariff(Tariff):
    def calculate_cost(self, usage): return usage * 0.1
class RoamingTariff(Tariff):
    def calculate_cost(self, usage): return usage * 5.0
class BillingProcessor:
    def process(self, tariff: Tariff, usage):
        return tariff.calculate_cost(usage)


print("\n___Завдання 2___")
processor = BillingProcessor()
print(f"Вартість дзвінка (10 хв): {processor.process(VoiceTariff(), 10)}")
print(f"Вартість роумінгу (5 хв): {processor.process(RoamingTariff(), 5)}")



# Завдання 3
class NetworkConnection(ABC):
    @abstractmethod
    def connect(self):
        pass
class LTEConnection(NetworkConnection):
    def connect(self): print("LTE підключено")
class WiFiConnection(NetworkConnection):
    def connect(self): print("WiFi підключено")
class SatelliteConnection(NetworkConnection):
    def connect(self):
        self.align_dish()
        print("Супутник підключено")
    def align_dish(self):
        print("Налаштування антени...")


print("\n___Завдання 3___")
connections = [LTEConnection(), WiFiConnection(), SatelliteConnection()]
for conn in connections:
    conn.connect()  # Всі поводяться як NetworkConnection



# Завдання 4
class Callable(ABC):
    @abstractmethod
    def make_call(self): pass
class SMSCapable(ABC):
    @abstractmethod
    def send_sms(self): pass
class DataTransferable(ABC):
    @abstractmethod
    def transfer_data(self): pass
class IoTDevice(DataTransferable):
    def transfer_data(self):
        print("IoT: Відправка телеметрії...")
class Smartphone(Callable, SMSCapable, DataTransferable):
    def make_call(self): print("Смартфон: Дзвоню...")
    def send_sms(self): print("Смартфон: Пишу SMS...")
    def transfer_data(self): print("Смартфон: Використовую інтернет...")


print("\n___Завдання 4___")
iot = IoTDevice()
phone = Smartphone()
iot.transfer_data()
phone.make_call()



# Завдання 5
class Logger(ABC):
    @abstractmethod
    def log(self, message): pass
class FileLogger(Logger):
    def log(self, message): print(f"Лог у файл: {message}")
class ServerLogger(Logger):
    def log(self, message): print(f"Лог на сервер: {message}")
class ConsoleLogger(Logger):
    def log(self, message): print(f"Лог у консоль: {message}")
class NetworkMonitor:
    def __init__(self, logger: Logger):
        self.logger = logger
    def check_status(self):
        self.logger.log("Мережа працює стабільно")


print("\n___Завдання 5___")
# Міняємо логер без зміни коду NetworkMonitor
monitor_file = NetworkMonitor(FileLogger())
monitor_file.check_status()

monitor_console = NetworkMonitor(ConsoleLogger())
monitor_console.check_status()