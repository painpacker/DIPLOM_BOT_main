import requests


class ProductService:
    base_url = "http://localhost:8000/api/"
    limit = 5

    def add_product(self, product_data: dict):
        response = requests.post(f"{self.base_url}products/", json=product_data)
        response.raise_for_status()
        return response.json()

    def display_products(self, page=1):
        query_params = dict(limit=self.limit, offset=(page - 1) * self.limit)
        response = requests.get(f"{self.base_url}product/", params=query_params)
        response.raise_for_status()
        return response.json()


products_service = ProductService()