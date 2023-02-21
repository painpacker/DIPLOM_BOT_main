import requests


class UserRegistrationService:
    base_url = "http://localhost:8000/api/"

    def add_user(self, user_data: dict):
        request_to_add_user = requests.post(f"{self.base_url}users/", json=user_data)
        return request_to_add_user.raise_for_status()

    def update_user(self, account_id: int, user_data: dict) -> dict:
        response = requests.put(f"{self.base_url}user/{account_id}", json=user_data)
        response.raise_for_status()
        return response.json()

    def get_user(self, account_id: int):
        response = requests.get(f"{self.base_url}user/{account_id}")
        response.raise_for_status()
        return response.json()

user_service = UserRegistrationService()