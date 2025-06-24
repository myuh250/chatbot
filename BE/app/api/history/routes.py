from fastapi import APIRouter, HTTPException, status, Query
from pydantic import BaseModel
from typing import List, Optional
from .services import add_message, get_history

router = APIRouter(prefix="/history", tags=["history"])

class MessageIn(BaseModel):
    user_id: str
    role: str  # 'user' hoặc 'agent'
    content: str

class MessageOut(MessageIn):
    id: int
    timestamp: str

@router.post("/", response_model=MessageOut, status_code=status.HTTP_201_CREATED)
async def post_message(msg: MessageIn):
    if msg.role not in ("user", "agent"):
        raise HTTPException(status_code=400, detail="role must be 'user' or 'agent'")
    saved = await add_message(msg.user_id, msg.role, msg.content)
    return saved

@router.get("/", response_model=List[MessageOut])
async def read_history(user_id: Optional[str] = Query(None, description="lọc theo user_id")):
    history = await get_history(user_id)
    return history
