import os
from fastapi import APIRouter, Depends, FastAPI, Path, WebSocket, Request, BackgroundTasks, HTTPException, WebSocketDisconnect
import uuid
from redis.commands.json.path import Path
import json
from datetime import datetime

from ..schema.chat import Chat
from ..socket.connection import ConnnectionManager
from ..socket.utils import get_token
from ..redis.producer import Producer
from .. redis.config import Redis
from ..redis.stream import StreamConsumer
from ..redis.cache import Cache
from ..model.gptj import GPT


# adding the routes to the router
chat = APIRouter()

# creating the connection manager
manager = ConnnectionManager()

# get the redsi class from the confing and initializing it
redis = Redis()



@chat.post("/token")
async def token_generator(name : str, request: Request):
    token = str(uuid.uuid4())
    if name == "":
        raise HTTPException(status_code=400, detail={
            "loc" : "name", "msg" : "Enter a valid name"
        })
    
    json_client = redis.create_rejson_connection()
    
    chat_session = Chat(
        token=token,
        messages=[],
        name=name,
        session_start=str(datetime.now())
    )


    await json_client.json().set(str(token),Path.root_path(), chat_session.model_dump())

    redis_client = await redis.create_connection()
    await redis_client.expire(str(token), 3600)

    return chat_session.model_dump()



@chat.post("/refresh_token")
async def refresh_token(request: Request, token: str):
    json_client = redis.create_rejson_connection()
    cache = Cache(json_client)
    data = await cache.get_chat_history(token)
    if data == None:
        raise HTTPException(status_code=400, detail="Session Expired or does not exist")
    else:
        return data




@chat.websocket("/chat")
async def websocket_endpoint(websocket: WebSocket = WebSocket, token:str = Depends(get_token)):
    await manager.connect(websocket)
    redis_client = await redis.create_connection()
    json_client = await redis.create_rejson_connection()
    producer = Producer(redis_client)

    try:
        while True:
            data = await websocket.receive_text()
            stream_data = {}
            stream_data[token] = data
            await producer.add_to_stream(stream_data,"message_channel")
            response = GPT().query(input=str(data))
            await manager.send_personal_message(response, websocket)
    # await manager.connect(websocket)
    # redis_client = await redis.create_connection()
    # producer = Producer(redis_client)
    # json_client = await redis.create_rejson_connection()
    # consumer = StreamConsumer(redis_client)
    
    # try:
    #     while True:
    #         data = await websocket.receive_text()
    #         # print(data)
    #         stream_data = {}
    #         stream_data[str(token)] = str(data)
    #         await producer.add_to_stream(stream_data,"message_channel")
    #         response = await consumer.consume_stream(stream_channel="response_channel",count = 1, block=0)

    #         print(response)

    #         for stream, messages in response:
    #             for message in messages:
    #                 response_token = [k.decode('utf-8') for k,v in message[1].items()][0]

    #                 if token == response_token:
    #                     response_message = [v.decode('utf-8') for k,v in message[1].items()][0]
    #                     print(message[0].decode('utf-8'))
    #                     print(token)
    #                     print(response_token)

    #                     await manager.send_personal_message(response_message,websocket)
    #                 await consumer.delete_message(stream_channel="response_channel",message_id=message[0].decode('utf-8'))

    except WebSocketDisconnect:
        manager.disconnect(websocket)