from src.redis.config import Redis
import asyncio
from src.model.gptj import GPT
from src.redis.cache import Cache
from src.schema.chat import Message

redis = Redis()


async def main():
    json_client = await redis.create_rejson_connection()
    await Cache(json_client).add_message_to_cache(token="36259234-e7e7-4bdd-af1a-aa35536447af", source = "human", message_data={
        "id": "9",
        "msg": "Hello",
        "timestamp": "2022-07-16 13:20:01.092109"
    })

    data = await Cache(json_client).get_chat_history(token="36259234-e7e7-4bdd-af1a-aa35536447af")
    
    print(data)
    # await redis.json().set("key","$", "value")
    message_data = data['messages'][-4:]

    input = ["" + i['msg'] for i in message_data]
    input = " ".join(input)


    # todo
    # res = GPT().query(input=input) # todo
    # msg = Message(msg = res) # todo
    # print(msg)  # todo
    # await Cache(json_client).add_message_to_cache(token="36259234-e7e7-4bdd-af1a-aa35536447af", source="bot", message_data=msg.model_dump)


if __name__ == "__main__":
    asyncio.run(main())