import requests
from typing import Optional, Dict, Any


class RestClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
    def _make_request(self, method: str, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Optional[
        Dict[str, Any]]:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        try:
            response = requests.request(method, url, json=data, timeout=10)

            # Перевірка на помилки HTTP (4xx, 5xx)
            response.raise_for_status()

            print(f"[{method}] Success! Status Code: {response.status_code}")
            return response.json()

        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except requests.exceptions.ConnectionError:
            print("Error: Could not connect to the server.")
        except requests.exceptions.Timeout:
            print("Error: The request timed out.")
        except requests.exceptions.RequestException as err:
            print(f"An unexpected error occurred: {err}")

        return None

    def get(self, endpoint: str) -> Optional[Dict[str, Any]]:
        return self._make_request("GET", endpoint)

    def post(self, endpoint: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        return self._make_request("POST", endpoint, data)


if __name__ == "__main__":
    # Ініціалізація клієнта для JSONPlaceholder
    client = RestClient("https://jsonplaceholder.typicode.com")

    print("--- Тестування GET запиту ---")
    # Отримання посту з id=1
    post_data = client.get("posts/1")
    if post_data:
        print(f"Title: {post_data.get('title')}\n")

    print("--- Тестування POST запиту ---")
    # Створення нового посту
    new_post = {
        "title": "Новий пост",
        "body": "Зміст нашого тестового запиту",
        "userId": 1
    }
    created_post = client.post("posts", new_post)
    if created_post:
        print(f"Created ID: {created_post.get('id')}")
        print(f"Response: {created_post}")