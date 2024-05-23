# from datetime import datetime
# from pydantic import BaseModel
# from typing import List, Optional
# import uuid


# class Message(BaseModel):
#     id : uuid.uuid4()
#     msg: str
#     timestamp = str(datetime.now())


# class Chat(BaseModel):
#     token : str
#     messages : List[Message]
#     name: str
#     session_start = str(datetime.now())

# from datetime import datetime
# from pydantic import BaseModel
# from typing import List, Optional
# import uuid


# class Message(BaseModel):
#     id = str(uuid.uuid4())
#     msg: str
#     timestamp = str(datetime.now())


# class Chat(BaseModel):
#     token: str
#     messages: List[Message]
#     name: str
#     session_start = str(datetime.now())

from datetime import datetime
from pydantic import BaseModel, Field
from typing import List
import uuid


class Message(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    msg: str
    timestamp: str = Field(default_factory=lambda: str(datetime.now()))


class Chat(BaseModel):
    token: str
    messages: List[Message]
    name: str
    session_start: str = Field(default_factory=lambda: str(datetime.now()))