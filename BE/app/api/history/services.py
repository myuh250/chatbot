import json
import os
import asyncio
from datetime import datetime
from typing import Dict, Any, List, Optional

# file path để lưu cache
DATA_FILE = os.path.join(os.path.dirname(__file__), '..', '..', 'chat_history.json')

# lock để đảm bảo thread-safe khi ghi file
_lock = asyncio.Lock()

async def _load_history() -> List[Dict[str, Any]]:
    if not os.path.exists(DATA_FILE):
        return []
    async with _lock:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []

async def _save_history(history: List[Dict[str, Any]]):
    async with _lock:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)

async def add_message(user_id: str, role: str, content: str) -> Dict[str, Any]:
    """
    Thêm 1 message mới vào history, trả về message vừa thêm
    role: 'user' hoặc 'agent'
    """
    history = await _load_history()
    msg = {
        "id": len(history) + 1,
        "user_id": user_id,
        "role": role,
        "content": content,
        "timestamp": datetime.utcnow().isoformat() + 'Z'
    }
    history.append(msg)
    await _save_history(history)
    return msg

async def get_history(user_id: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Lấy toàn bộ lịch sử.
    Nếu có user_id thì filter theo user.
    """
    history = await _load_history()
    if user_id:
        history = [m for m in history if m["user_id"] == user_id]
    return history
