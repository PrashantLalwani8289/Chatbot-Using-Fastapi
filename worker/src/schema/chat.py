from datetime import datetime
from pydantic import BaseModel, Field
from typing import List, Optional
import uuid




# class Message(BaseModel):
#     id = str(uuid.uuid4())
#     msg : str
#     timestamp = str(datetime.now())

class Message(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    msg: str
    timestamp: str = Field(default_factory=lambda: str(datetime.now()))