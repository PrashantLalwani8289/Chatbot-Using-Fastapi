from src.redis.config import Redis
import asyncio
from src.model.gptj import GPT
from src.redis.cache import Cache


redis = Redis()


async def main():
    json_client = await redis.create_rejson_connection()
    await Cache(json_client).add_message_to_cache(token="5ad95daf-e1d7-4399-bb0a-61dea65d6fd9", message_data={
        "id": "1",
        "msg": "Hello",
        "timestamp": "2022-07-16 13:20:01.092109"
    })

    data = await Cache(json_client).get_chat_history(token="5ad95daf-e1d7-4399-bb0a-61dea65d6fd9")
    
    print(data)
    # await redis.json().set("key","$", "value")


if __name__ == "__main__":
    asyncio.run(main())