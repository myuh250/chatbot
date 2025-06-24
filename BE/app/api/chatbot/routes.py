from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from .services import ChatbotService

router = APIRouter(prefix="/chatbot", tags=["chatbot"])

# Initialize chatbot service
try:
    chatbot_service = ChatbotService()
except ValueError as e:
    print(f"Warning: {e}")
    chatbot_service = None

class MessageRequest(BaseModel):
    message: str

class MessageResponse(BaseModel):
    success: bool
    data: Dict[str, Any]
    message: str

@router.post("/analyze", response_model=MessageResponse)
async def analyze_message(request: MessageRequest):
    """
    Phân tích tin nhắn chat và trích xuất thông tin đơn hàng
    """
    if not chatbot_service:
        raise HTTPException(status_code=500, detail="Chatbot service not initialized. Please check GEMINI_API_KEY.")
    
    try:
        # Analyze the message
        order_data = chatbot_service.analyze_message(request.message)
        
        # Save to file
        save_success = chatbot_service.save_order_info(order_data)
        
        return MessageResponse(
            success=True,
            data=order_data,
            message="Message analyzed successfully" if save_success else "Message analyzed but failed to save"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to analyze message: {str(e)}")

@router.get("/orders", response_model=List[Dict[str, Any]])
async def get_all_orders():
    """
    Lấy tất cả thông tin đơn hàng đã được phân tích
    """
    if not chatbot_service:
        raise HTTPException(status_code=500, detail="Chatbot service not initialized. Please check GEMINI_API_KEY.")
    
    try:
        orders = chatbot_service.get_all_orders()
        return orders
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get orders: {str(e)}")

@router.delete("/orders")
async def clear_orders():
    """
    Xóa tất cả thông tin đơn hàng (reset)
    """
    if not chatbot_service:
        raise HTTPException(status_code=500, detail="Chatbot service not initialized. Please check GEMINI_API_KEY.")
    
    try:
        import os
        file_path = os.path.join(os.path.dirname(__file__), '..', '..', 'order_info.json')
        
        if os.path.exists(file_path):
            os.remove(file_path)
        
        return {"success": True, "message": "All orders cleared"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to clear orders: {str(e)}")
