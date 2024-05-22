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


    await json_client.json().set(str(token),Path.root_path(), chat_session.model_dump)

    redis_client = await redis.create_connection()
    await redis_client.expire(str(token), 3600)

    return chat_session



@chat.post("/refresh_token")
async def refresh_token(request: Request):
    return None



@chat.websocket("/chat")
async def websocket_endpoint(websocket: WebSocket = WebSocket, token:str = Depends(get_token)):
    await manager.connect(websocket)
    redis_client = await redis.create_connection()
    producer = Producer(redis_client)
    
    try:
        while True:
            data = await websocket.receive_text()
            print(data)
            stream_data = {}
            stream_data[token] = data
            await producer.add_to_stream(stream_data,"message_channel")
            await manager.send_personal_message(f"Testing the websocket", websocket)

    except WebSocketDisconnect:
        manager.disconnect(websocket)