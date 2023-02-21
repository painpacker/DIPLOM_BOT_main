import requests


class ProductService:
    base_url = "http://localhost:8000/api/"
    limit = 5

    def add_product(self, product_data: dict):
        response = requests.post(f"{self.base_url}products/", json=product_data)
        response.raise_for_status()
        return response.json()

    def DisplayProducts(self, page=1):
        query_params = dict(limit=self.limit, offset=(page - 1) * self.limit)
        response = requests.get(f"{self.base_url}products/", params=query_params)
        response.raise_for_status()
        return response.json()

    def get_product(self, user_id: int) -> None:
        response = requests.get(f"{self.base_url}products/{user_id}/")
        response.raise_for_status()
        return response.json()

    def MyProducts(self, account_id, page=1):
        query_params = dict(limit=self.limit, offset=(page - 1) * self.limit)
        response = requests.get(f"{self.base_url}Products/{account_id}/", params=query_params)
        response.raise_for_status()
        return response.json()

    def UpdateProducts(self, user_id: int, user_data: dict) -> dict:
        response = requests.patch(f"{self.base_url}products/{user_id}/", json=user_data)
        response.raise_for_status()
        return response.json()


products_service = ProductService()