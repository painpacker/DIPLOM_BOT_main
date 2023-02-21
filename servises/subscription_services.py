import requests


class SubscriptionService:
    base_url = "http://localhost:8000/api/"

    def update_user(self, account_id: int, user_data: dict) -> dict:
        response = requests.patch(f"{self.base_url}user/{account_id}", json=user_data)
        response.raise_for_status()
        return response.json()

    def get_users(self):
        response = requests.get(f"{self.base_url}users/")
        response.raise_for_status()
        return response.json()

    def check_subscription(self, account_id: int):
        response = requests.get(f"{self.base_url}user/{account_id}/subscription/")
        response.raise_for_status()
        return response.json()




subscription_service = SubscriptionService()