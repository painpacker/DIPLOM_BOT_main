import requests


class AdvertisementService:
    show_list = list()
    limit = 5
    base_url = "http://localhost:8000/api/"


    def add_advertisement(self, advertisement_data: dict):
        response = requests.post(f"{self.base_url}advertisement/", json=advertisement_data)
        response.raise_for_status()
        return response.json()

    def my_advertisement(self, user_id):
        self.show_list.clear()
        invoice_search_query = requests.get(f"{self.base_url}Advertisement/{user_id}")
        json_data = invoice_search_query.json()
        if not json_data['results']:
            return f"У вас нет рекламы, но вы можете создать её!"
        else:
            for json_list in json_data['results']:
                id = json_list['id']
                name = json_list['name']
                conclusion = str(f"{id}:{name}")
                self.show_list.append(conclusion)
            return '\n'.join(self.show_list)

    # def my_advertisement(self, user_id):
    #     responce = requests.get(f"{self.base_url}Advertisement/{user_id}")
    #     responce.raise_for_status()
    #     return responce.json()



advertisements_service = AdvertisementService()