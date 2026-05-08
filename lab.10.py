import unittest
from parameterized import parameterized
from unittest.mock import MagicMock


# 1. Тестування виконання арифметичних операцій
class MathTool:
    def add(self, a, b):
        return a + b
    def subtract(self, a, b):
        return a - b
    def multiply(self, a, b):
        return a * b
    def divide(self, a, b):
        if b == 0:
            raise ValueError("Ділення на нуль неможливе")
        return a / b

class TestMathTool(unittest.TestCase):
    def setUp(self):
        self.tool = MathTool()
    def test_add(self):
        self.assertEqual(self.tool.add(10, 5), 15)
    def test_subtract(self):
        self.assertEqual(self.tool.subtract(10, 5), 5)
    def test_multiply(self):
        self.assertEqual(self.tool.multiply(10, 5), 50)
    def test_divide(self):
        self.assertEqual(self.tool.divide(10, 2), 5)
    def test_divide_by_zero(self):
        with self.assertRaises(ValueError):
            self.tool.divide(10, 0)


# 2. Тестування класу LibraryItem
class LibraryItem:
    def __init__(self, title, author, year):
        self.title = title
        self.author = author
        self.year = year
    def details(self):
        return f"{self.title} - {self.author} ({self.year})"

class TestLibraryItem(unittest.TestCase):
    def test_details(self):
        item = LibraryItem("Кобзар", "Тарас Шевченко", 1840)
        expected = "Кобзар - Тарас Шевченко (1840)"
        self.assertEqual(item.details(), expected)
    def test_details_different_data(self):
        item = LibraryItem("1984", "George Orwell", 1949)
        self.assertIn("George Orwell", item.details())
        self.assertTrue(item.details().endswith("(1949)"))


# 3. Тестування взаємодії класів з використанням mock
class NotificationService:
    def send(self, message):
        pass

class UserManager:
    def __init__(self, service):
        self.service = service
    def notify_user(self, message):
        self.service.send(message)

class TestUserManager(unittest.TestCase):
    def test_notify_user_calls_send(self):
        # Створюємо мок-об'єкт
        mock_service = MagicMock(spec=NotificationService)
        manager = UserManager(mock_service)
        test_msg = "Привіт, користувачу!"
        manager.notify_user(test_msg)

        # Перевіряємо, чи був викликаний метод send з правильним аргументом
        mock_service.send.assert_called_once_with(test_msg)


# 4. Параметризовані тести для парності числа
def check_even(number):
    return number % 2 == 0

class TestCheckEven(unittest.TestCase):
    @parameterized.expand([
        ("positive_even", 2, True),
        ("positive_odd", 3, False),
        ("zero", 0, True),
        ("negative_even", -4, True),
        ("negative_odd", -7, False),
        ("large_even", 1000, True),
    ])
    def test_check_even(self, name, number, expected):
        self.assertEqual(check_even(number), expected)

if __name__ == '__main__':
    unittest.main()