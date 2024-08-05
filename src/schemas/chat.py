
from pydantic import BaseModel, EmailStr

class Message(BaseModel):
   msg: str
