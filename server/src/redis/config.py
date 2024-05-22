import os
from dotenv import load_dotenv
from redis import asyncio as aioredis 
from redis import client

load_dotenv()


class Redis():
    def __init__(self):
        self.REDIS_URL = os.environ['REDIS_URL']
        self.REDIS_PASSWORD = os.environ['REDIS_PASSWORD']
        self.REDIS_USER = os.environ['REDIS_USER']
        self.connection_url = os.environ.get('REDIS_URL')
        self.REDIS_HOST = os.environ['REDIS_HOST']
        self.REDIS_PORT = os.environ['REDIS_PORT']

    async def create_connection(self):
        self.connection = aioredis.from_url(self.connection_url, db= 0)

        return self.connection
    
    def create_rejson_connection(self):
        # self.redisJson = client(host = self.REDIS_HOST, port = self.REDIS_PORT,decode_responses=True, username=self.REDIS_USER, password=self.REDIS_PASSWORD)
        # return self.redisJson
        self.redisJson = aioredis.from_url(self.connection_url, db=0)
        return self.redisJson