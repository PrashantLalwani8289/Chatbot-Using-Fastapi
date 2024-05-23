# from .config import Redis
from redis.commands.json.path import Path

class Cache:
    def __init__(self, json_client):
        self.json_client = json_client


    async def get_chat_history(self, token: str):
        data = await self.json_client.json().get(str(token),Path.root_path())

        return data
    
    async def add_message_to_cache(self, token: str, source : str, message_data:dict ):
        if source == "human":
            message_data['msg'] = "Human: " + (message_data['msg'])
        elif source == "bot":
            message_data['msg'] = "Bot: " + (message_data['msg'])
        await self.json_client.json().arrappend(str(token),Path('.messages'), message_data)