import json
import os
from typing import Dict, Any, Optional, List
import openai
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

class ChatbotService:
    def __init__(self):
        # Configure OpenAI API
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        self.client = openai.OpenAI(api_key=api_key)
        
    def analyze_message(self, message: str) -> Dict[str, Any]:
        """
        Phân tích tin nhắn chat và trích xuất thông tin đơn hàng
        """
        system_prompt = """Bạn là một AI agent chuyên phân tích tin nhắn chat để trích xuất thông tin đơn hàng bánh.

Nhiệm vụ của bạn là phân tích tin nhắn và trả về thông tin dưới dạng JSON với cấu trúc chính xác như sau:

{
    "id": null,
    "ten_khach_hang": "Tên khách hàng",
    "so_dien_thoai": "Số điện thoại",
    "danh_sach_banh": [
        {
            "ten_banh": "Tên bánh",
            "so_luong": số_lượng
        }
    ],
    "dia_chi": "Địa chỉ giao hàng",
    "gio_giao": "Giờ giao hàng (định dạng HH:MM)",
    "ghi_chu": "Ghi chú (nếu có)"
}

Quy tắc quan trọng:
1. Nếu có nhiều loại bánh, tạo nhiều object trong danh_sach_banh
2. so_luong phải là số nguyên dương
3. Nếu thông tin nào không có trong tin nhắn, để null hoặc chuỗi rỗng ""
4. id luôn để null (sẽ được tự động tạo)
5. ten_khach_hang: trích xuất tên người đặt hàng
6. so_dien_thoai: trích xuất số điện thoại (có thể có dấu cách, dấu gạch ngang)
7. danh_sach_banh: trích xuất tên bánh và số lượng
8. dia_chi: trích xuất địa chỉ giao hàng
9. gio_giao: trích xuất giờ giao hàng (định dạng HH:MM)
10. ghi_chu: trích xuất ghi chú đặc biệt

Chỉ trả về JSON hợp lệ, không có text khác."""

        user_prompt = f"Phân tích tin nhắn sau: {message}"

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.1,
                max_tokens=1000
            )
            
            # Parse JSON response
            result_text = response.choices[0].message.content.strip()
            result = json.loads(result_text)
            
            # Add timestamp
            result['timestamp'] = datetime.now().isoformat()
            result['original_message'] = message
            
            return result
            
        except Exception as e:
            return {
                'error': f'Failed to analyze message: {str(e)}',
                'timestamp': datetime.now().isoformat(),
                'original_message': message
            }
    
    def save_order_info(self, order_data: Dict[str, Any]) -> bool:
        """
        Lưu thông tin đơn hàng vào file order_info.json
        """
        try:
            file_path = os.path.join(os.path.dirname(__file__), '..', '..', 'order_info.json')
            
            # Load existing data if file exists
            existing_data = []
            if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                with open(file_path, 'r', encoding='utf-8') as f:
                    existing_data = json.load(f)
            
            # Generate ID for new order
            if not existing_data:
                order_data['id'] = 1
            else:
                max_id = max(order.get('id', 0) for order in existing_data)
                order_data['id'] = max_id + 1
            
            # Remove timestamp and original_message from saved data
            order_to_save = {k: v for k, v in order_data.items() 
                           if k not in ['timestamp', 'original_message']}
            
            # Add new order data
            existing_data.append(order_to_save)
            
            # Save back to file
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(existing_data, f, ensure_ascii=False, indent=2)
            
            return True
            
        except Exception as e:
            print(f"Error saving order info: {str(e)}")
            return False
    
    def get_all_orders(self) -> list:
        """
        Lấy tất cả thông tin đơn hàng từ file
        """
        try:
            file_path = os.path.join(os.path.dirname(__file__), '..', '..', 'order_info.json')
            
            if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
                return []
            
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
                
        except Exception as e:
            print(f"Error reading orders: {str(e)}")
            return []
