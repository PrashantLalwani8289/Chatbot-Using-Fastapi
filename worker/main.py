import asyncio
import os


from src.redis.config import Redis
from src.model.gptj import GPT
from src.redis.cache import Cache
from src.schema.chat import Message
from src.redis.stream import StreamConsumer
from src.redis.producer import Producer



redis = Redis()


async def main():
    json_client = await redis.create_rejson_connection()
    redis_client = await redis.create_connection()
    consumer = StreamConsumer(redis_client)
    cache = Cache(json_client)
    producer = Producer(redis_client)


    print("Stream Consumer Started")
    print("Stream waiting for new messages")

    while True:
        response = await consumer.consume_stream(stream_channel="message_channel", count=1, block=0)

        if response:
            for stream, messages in response:
                # Get message from stream, and extract token, message data and message id
                for message in messages:
                    message_id = message[0]
                    token = [k.decode('utf-8') for k, v in message[1].items()][0]

                    message = [v.decode('utf-8') for k, v in message[1].items()][0]

                    print(token)

                    msg = Message(msg = message)

                    data = await cache.add_message_to_cache(token=token, source="human", message_data=msg.model_dump())


                    message_data = data['messages'][-4:]

                    input = ["" + i['msg'] for i in message_data]
                    input = " ".join(input)

                    # todo
                    res = GPT().query(input=input) # todo
                    msg = Message(msg = res) # todo
                    stream_data = {}
                    stream_data[str(token)] = str(msg.model_dump())
                    await producer.add_to_stream(stream_data, "response_channel")
                    # print(msg)  # todo
                    await Cache(json_client).add_message_to_cache(token="36259234-e7e7-4bdd-af1a-aa35536447af", source="bot", message_data=msg.model_dump)

                await consumer.delete_message(stream_channel="message_channel", message_id=message_id)



if __name__ == "__main__":
    asyncio.run(main())