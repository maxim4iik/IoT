import json
import logging
from typing import List

import pydantic_core
import requests

from app.entities.processed_agent_data import ProcessedAgentData 
from app.interfaces.store_api_gateway import StoreGateway

class StoreApiAdapter(StoreGateway):
    def __init__(self, api_base_url): 
        self.api_base_url = api_base_url
    def save_data(self, processed_agent_data_batch: List[ProcessedAgentData]):
        url = f"{self.api_base_url}/processed_agent_data"
        # Серіалізація кожного елемента з processed_agent_data_batch до JSON
        data_to_send = [item.json() for item in processed_agent_data_batch]
        # Оскільки requests вимагає рядок для тіла запиту і заголовки для вказівки типу контенту,
        # перетворюємо список JSON рядків назад у JSON формат, який містить цей список
        # та встановлюємо заголовок 'Content-Type' як 'application/json'
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, data=json.dumps(data_to_send), headers=headers)
        
        try:
            response.raise_for_status()
            # Логування успішного збереження даних
            logging.info("Data successfully saved to the store API.")
        except requests.exceptions.HTTPError as err:
            # Логування помилки, якщо відповідь не є успішною
            logging.error(f"Error saving data to the store API: {err}")