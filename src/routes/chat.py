from fastapi import Body, APIRouter
from src.controllers.chat import Chat
from src.schemas.chat import Message

router = APIRouter()

@router.post(
    "/",
)
async def message_to_pandas(message: Message = Body(...)):
    chat_pandas = Chat()
    response = chat_pandas.generate_message()
    return response
