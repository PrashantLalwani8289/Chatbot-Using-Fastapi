from fastapi import FastAPI, Request
import uvicorn
import os
from dotenv import load_dotenv


from src.routes.chat import chat

# loading the environment variables
load_dotenv()

# creating the fastapi app
api = FastAPI()

# adding all the routes to the app router
api.include_router(chat)


@api.get("/test")
async def root():
    return {"msg" : "Api is not Online"}


if __name__ == "__main__":
    if os.environ.get('APP_ENV') == "development":
        uvicorn.run("main:api", host="0.0.0.0", port = 3500, workers = 4, reload=True)
    else:
        pass