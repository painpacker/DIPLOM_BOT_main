# import requests
#
#
# class MarketService:
#     show_list = list()
#     limit = 5
#     base_url = "http://localhost:8000/api/"
#
#     def display_advertisement(self, account_id, page=0):
#         query_params = dict(limit=self.limit, offset=page)
#         response = requests.get(f"{self.base_url}/", params=query_params)
#         response.raise_for_status()
#         return response.json()
