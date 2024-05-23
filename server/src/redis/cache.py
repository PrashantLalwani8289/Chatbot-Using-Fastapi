from redis.commands.json.path import Path

class Cache:
    def __init__(self, json_client):
        self.json_client = json_client

    async def get_chat_history(self, token:str):
        data = self.json_client.json().get(str(token), Path.root_path())

        return data