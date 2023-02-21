import json
import random
import requests


class AdvertisementService:
    limit = 5
    show_list = list()
    base_url = "http://localhost:8000/api/"


    def add_advertisement(self, advertisement_data: dict):
        response = requests.post(f"{self.base_url}advertisement/", json=advertisement_data)
        response.raise_for_status()
        return response.json()

    def display_advertisement(self, account_id, page=1):
        query_params = dict(limit=self.limit, offset=(page - 1) * self.limit)
        response = requests.get(f"{self.base_url}Advertisement/{account_id}/", params=query_params)
        response.raise_for_status()
        return response.json()

    def get_random_advertisement(self):
        response = requests.get(f"{self.base_url}advertisement/")
        response.raise_for_status()
        results = response.json()['results']
        return random.choice(results)

    def advertisement_info(self, user_id):
        response = requests.get(f"{self.base_url}advertisement/{user_id}")
        response.raise_for_status()
        return response.json()

    def update_advertisement(self, user_id: int, user_data: dict) -> dict:
        response = requests.patch(f"{self.base_url}advertisement/{user_id}/", json=user_data)
        response.raise_for_status()
        return response.json()







advertisements_service = AdvertisementService()