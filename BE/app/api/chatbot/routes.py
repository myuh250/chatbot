from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import os
import json
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
    order_id: Optional[int] = None

class MessageResponse(BaseModel):
    success: bool
    data: Dict[str, Any]
    message: str

class ConfirmOrderRequest(BaseModel):
    order_id: int

@router.post("/process", response_model=MessageResponse)
async def process_message(request: MessageRequest):
    """
    Xử lý tin nhắn với logic đầy đủ (kiểm tra thông tin, hỏi thiếu, xác nhận)
    """
    if not chatbot_service:
        raise HTTPException(status_code=500, detail="Chatbot service not initialized. Please check OPENAI_API_KEY.")
    
    try:
        # Process message with full logic
        result = chatbot_service.process_order_logic(request.message, request.order_id)
        
        return MessageResponse(
            success=True,
            data=result,
            message=result.get('message', 'Processed successfully')
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process message: {str(e)}")

@router.post("/confirm", response_model=MessageResponse)
async def confirm_order(request: ConfirmOrderRequest):
    """
    Xác nhận đơn hàng và lưu vào file cuối cùng
    """
    if not chatbot_service:
        raise HTTPException(status_code=500, detail="Chatbot service not initialized. Please check OPENAI_API_KEY.")
    
    try:
        # Get all current orders
        orders = chatbot_service.get_all_orders()
        target_order = None
        
        # Find the order to confirm
        for order in orders:
            if order.get('id') == request.order_id:
                target_order = order
                break
        
        if not target_order:
            raise HTTPException(status_code=404, detail="Order not found")
        
        # Check if order is complete before confirming
        completeness_check = chatbot_service.check_order_completeness(target_order)
        if not completeness_check['is_complete']:
            raise HTTPException(
                status_code=400, 
                detail=f"Cannot confirm incomplete order. Missing: {', '.join(completeness_check['missing_fields'])}"
            )
        
        # Save to final orders
        save_success = chatbot_service.save_final_order(target_order)
        
        if save_success:
            return MessageResponse(
                success=True,
                data=target_order,
                message="🎉 Đơn hàng đã được xác nhận thành công! Chúng tôi sẽ liên hệ với bạn sớm để xác nhận thời gian giao hàng."
            )
        else:
            raise HTTPException(status_code=500, detail="Failed to save confirmed order")
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to confirm order: {str(e)}")

@router.get("/confirmed-orders", response_model=List[Dict[str, Any]])
async def get_confirmed_orders():
    """
    Lấy tất cả đơn hàng đã xác nhận
    """
    if not chatbot_service:
        raise HTTPException(status_code=500, detail="Chatbot service not initialized. Please check OPENAI_API_KEY.")
    
    try:
        confirmed_orders = chatbot_service.get_confirmed_orders()
        return confirmed_orders
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get confirmed orders: {str(e)}")

@router.post("/analyze", response_model=MessageResponse)
async def analyze_message(request: MessageRequest):
    """
    Phân tích tin nhắn chat và trích xuất thông tin đơn hàng
    """
    if not chatbot_service:
        raise HTTPException(status_code=500, detail="Chatbot service not initialized. Please check OPENAI_API_KEY.")
    
    try:
        # Analyze the message
        order_data = chatbot_service.analyze_message(request.message)
        
        # Save to file
        save_success = chatbot_service.save_order_info(order_data)

        if save_success and 'error' not in order_data:
            return MessageResponse(
                success=True,
                data=order_data,
                message="Message analyzed and order saved successfully"
            )
        else:
            return MessageResponse(
                success=False,
                data=order_data,
                message=order_data.get('error', 'Failed to analyze message')
            )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to analyze message: {str(e)}")

@router.get("/orders", response_model=List[Dict[str, Any]])
async def get_all_orders():
    """
    Lấy tất cả thông tin đơn hàng đã được phân tích
    """
    if not chatbot_service:
        raise HTTPException(status_code=500, detail="Chatbot service not initialized. Please check OPENAI_API_KEY.")
    
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
        raise HTTPException(status_code=500, detail="Chatbot service not initialized. Please check OPENAI_API_KEY.")
    
    try:
        # Clear order_info.json
        file_path = os.path.join(os.path.dirname(__file__), '..', '..', 'order_info.json')
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump([], f)
        
        return {"success": True, "message": "All orders cleared"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to clear orders: {str(e)}")
