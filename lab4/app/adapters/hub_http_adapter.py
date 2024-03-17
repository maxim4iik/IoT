import requests
from app.entities.processed_agent_data import ProcessedAgentData

class HubHttpAdapter:
    def __init__(self, api_base_url):
        self.api_base_url = api_base_url

    def save_data(self, processed_data: ProcessedAgentData) -> bool:
        response = requests.post(f"{self.api_base_url}/save", json=processed_data.dict())
        return response.status_code == 200
