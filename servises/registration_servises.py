import requests


class UserRegistrationService:
    base_url = "http://localhost:8000/api/"

    def add_user(self, user_data: dict):
        response = requests.post(f"{self.base_url}users/", json=user_data)
        response.raise_for_status()
        return response.json()


user_service = UserRegistrationService()