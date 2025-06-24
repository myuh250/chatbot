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
        
    def analyze_message(self, message: str, existing_order: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Phân tích tin nhắn chat và trích xuất thông tin đơn hàng
        """
        if existing_order:
            # Build the prompt carefully to avoid f-string syntax issues
            existing_order_json = json.dumps(existing_order, ensure_ascii=False, indent=2)
            
            system_prompt = f"""Bạn là một AI assistant chuyên cập nhật thông tin đơn hàng bánh.

THÔNG TIN ĐƠN HÀNG HIỆN TẠI:
{existing_order_json}

NHIỆM VỤ: Cập nhật đơn hàng bằng cách kết hợp thông tin cũ với thông tin mới từ tin nhắn.

QUY TẮC CẬP NHẬT:
1. **BẮT BUỘC**: GIỮ NGUYÊN tất cả thông tin đã có
2. **CHỈ THAY ĐỔI**: khi tin nhắn mới có thông tin rõ ràng thay thế
3. **DANH SÁCH BÁNH**: Thêm bánh mới vào danh sách cũ (không xóa bánh cũ)
4. **KHÔNG TỰ SÁNG TẠO**: Chỉ sử dụng thông tin từ tin nhắn

HƯỚNG DẪN CỤ THỂ:
- Tên khách hàng: Giữ "{existing_order.get('ten_khach_hang', '')}" trừ khi tin nhắn có tên mới
- Số điện thoại: Giữ "{existing_order.get('so_dien_thoai', '')}" trừ khi tin nhắn có SĐT mới  
- Địa chỉ: Giữ "{existing_order.get('dia_chi', '')}" trừ khi tin nhắn có địa chỉ mới
- Giờ giao: Giữ "{existing_order.get('gio_giao', '')}" trừ khi tin nhắn có giờ mới
- Ghi chú: Giữ "{existing_order.get('ghi_chu', '')}" trừ khi tin nhắn có ghi chú mới

ĐỊNH DẠNG OUTPUT: Chỉ JSON thuần, không text khác.

Trả về JSON với cấu trúc chính xác:
{{
    "id": {existing_order.get('id', 'null')},
    "ten_khach_hang": "...",
    "so_dien_thoai": "...",
    "danh_sach_banh": [...],
    "dia_chi": "...",
    "gio_giao": "...",
    "ghi_chu": "..."
}}"""
        else:
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
        
    def get_orders(self) -> list:
        """
        Lấy tất cả thông tin đơn hàng từ file final
        """
        try:
            file_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data_final.json')
            
            if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
                return []
            
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
                
        except Exception as e:
            print(f"Error reading orders: {str(e)}")
            return []
    
    def check_order_completeness(self, order_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Kiểm tra tính đầy đủ của thông tin đơn hàng
        """
        required_fields = ['ten_khach_hang', 'so_dien_thoai', 'danh_sach_banh', 'dia_chi', 'gio_giao']
        missing_fields = []
        
        for field in required_fields:
            if field == 'danh_sach_banh':
                if not order_data.get(field) or len(order_data[field]) == 0:
                    missing_fields.append(field)
            else:
                if not order_data.get(field) or order_data[field] == "":
                    missing_fields.append(field)
        
        is_complete = len(missing_fields) == 0
        
        return {
            'is_complete': is_complete,
            'missing_fields': missing_fields,
            'order_data': order_data
        }
    
    def generate_missing_info_question(self, missing_fields: List[str]) -> str:
        """
        Tạo câu hỏi yêu cầu thông tin còn thiếu
        """
        field_translations = {
            'ten_khach_hang': 'tên khách hàng',
            'so_dien_thoai': 'số điện thoại',
            'danh_sach_banh': 'danh sách bánh cần đặt',
            'dia_chi': 'địa chỉ giao hàng',
            'gio_giao': 'giờ giao hàng'
        }
        
        missing_text = []
        for field in missing_fields:
            if field in field_translations:
                missing_text.append(field_translations[field])
        
        if len(missing_text) == 1:
            return f"Để hoàn tất đơn hàng, bạn vui lòng cung cấp thêm thông tin: **{missing_text[0]}**."
        else:
            return f"Để hoàn tất đơn hàng, bạn vui lòng cung cấp thêm các thông tin sau:\n" + \
                   "\n".join([f"• {info}" for info in missing_text])
    
    def generate_confirmation_message(self, order_data: Dict[str, Any]) -> str:
        """
        Tạo tin nhắn xác nhận đơn hàng
        """
        banh_list = []
        for banh in order_data.get('danh_sach_banh', []):
            banh_list.append(f"• {banh['ten_banh']} - Số lượng: {banh['so_luong']}")
        
        confirmation_msg = f"""✅ **XÁC NHẬN ĐỚN HÀNG**

📝 **Thông tin khách hàng:**
• Tên: {order_data.get('ten_khach_hang', '')}
• SĐT: {order_data.get('so_dien_thoai', '')}

🎂 **Danh sách bánh:**
{chr(10).join(banh_list)}

📍 **Địa chỉ giao hàng:** {order_data.get('dia_chi', '')}
⏰ **Giờ giao hàng:** {order_data.get('gio_giao', '')}
📌 **Ghi chú:** {order_data.get('ghi_chu', 'Không có ghi chú')}

Bạn có xác nhận đơn hàng này không? Vui lòng trả lời "Xác nhận" để hoàn tất đặt hàng."""
        
        return confirmation_msg
    
    def save_final_order(self, order_data: Dict[str, Any]) -> bool:
        """
        Lưu đơn hàng đã xác nhận vào file data_final.json
        """
        try:
            file_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data_final.json')
            
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
            
            # Add confirmation timestamp
            order_data['confirmed_at'] = datetime.now().isoformat()
            order_data['status'] = 'confirmed'
            
            # Remove temporary fields
            order_to_save = {k: v for k, v in order_data.items() 
                           if k not in ['timestamp', 'original_message']}
            
            # Add new order data
            existing_data.append(order_to_save)
            
            # Save back to file
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(existing_data, f, ensure_ascii=False, indent=2)
            
            return True
            
        except Exception as e:
            print(f"Error saving final order: {str(e)}")
            return False
    
    def get_confirmed_orders(self) -> list:
        """
        Lấy tất cả đơn hàng đã xác nhận từ file data_final.json
        """
        try:
            file_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data_final.json')
            
            if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
                return []
            
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
                
        except Exception as e:
            print(f"Error reading confirmed orders: {str(e)}")
            return []
    
    def update_incomplete_order(self, order_id: int, new_message: str) -> Dict[str, Any]:
        """
        Cập nhật thông tin đơn hàng chưa hoàn chỉnh với thông tin mới
        """
        try:
            # Get current orders
            current_orders = self.get_all_orders()
            target_order = None
            
            # Find the order to update
            for order in current_orders:
                if order.get('id') == order_id:
                    target_order = order
                    break
            
            if not target_order:
                return {'error': 'Order not found'}
            
            # Phân tích thông tin mới với context của đơn hàng cũ
            updated_order = self.analyze_message(new_message, target_order)
            
            if 'error' in updated_order:
                return updated_order
            
            # Keep the same ID
            updated_order['id'] = order_id
            
            # Update the order in the list
            for i, order in enumerate(current_orders):
                if order.get('id') == order_id:
                    current_orders[i] = {k: v for k, v in updated_order.items() 
                                       if k not in ['timestamp', 'original_message']}
                    break
            
            # Save updated orders
            file_path = os.path.join(os.path.dirname(__file__), '..', '..', 'order_info.json')
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(current_orders, f, ensure_ascii=False, indent=2)
            
            return updated_order
            
        except Exception as e:
            return {'error': f'Failed to update order: {str(e)}'}
    
    def merge_order_info(self, old_order: Dict[str, Any], new_order: Dict[str, Any]) -> Dict[str, Any]:
        """
        Merge thông tin đơn hàng cũ và mới một cách thông minh
        """
        merged_order = old_order.copy()
        
        # Merge từng field một cách thông minh
        merge_rules = {
            'ten_khach_hang': lambda old, new: new if new and new.strip() else old,
            'so_dien_thoai': lambda old, new: new if new and new.strip() else old,
            'dia_chi': lambda old, new: new if new and new.strip() else old,
            'gio_giao': lambda old, new: new if new and new.strip() else old,
            'ghi_chu': lambda old, new: new if new and new.strip() else old,
        }
        
        # Merge basic fields
        for field, merge_func in merge_rules.items():
            old_value = old_order.get(field, '')
            new_value = new_order.get(field, '')
            merged_order[field] = merge_func(old_value, new_value)
        
        # Merge danh_sach_banh (phức tạp hơn)
        old_banh_list = old_order.get('danh_sach_banh', [])
        new_banh_list = new_order.get('danh_sach_banh', [])
        
        if new_banh_list and len(new_banh_list) > 0:
            # Nếu có thông tin bánh mới, merge với cũ
            merged_banh = self.merge_banh_list(old_banh_list, new_banh_list)
            merged_order['danh_sach_banh'] = merged_banh
        else:
            # Giữ nguyên danh sách cũ
            merged_order['danh_sach_banh'] = old_banh_list
        
        # Update timestamp
        merged_order['timestamp'] = datetime.now().isoformat()
        merged_order['original_message'] = f"{old_order.get('original_message', '')} {new_order.get('original_message', '')}"
        
        return merged_order
    
    def merge_banh_list(self, old_list: List[Dict], new_list: List[Dict]) -> List[Dict]:
        """
        Merge danh sách bánh cũ và mới
        """
        if not old_list:
            return new_list
        
        if not new_list:
            return old_list
        
        # Tạo dictionary để dễ merge
        merged_dict = {}
        
        # Thêm bánh cũ
        for banh in old_list:
            ten_banh = banh.get('ten_banh', '').lower().strip()
            if ten_banh:
                merged_dict[ten_banh] = {
                    'ten_banh': banh.get('ten_banh', ''),
                    'so_luong': banh.get('so_luong', 0)
                }
        
        # Merge với bánh mới (bánh mới sẽ override bánh cũ nếu trùng tên)
        for banh in new_list:
            ten_banh = banh.get('ten_banh', '').lower().strip()
            if ten_banh:
                if ten_banh in merged_dict:
                    # Cập nhật số lượng nếu bánh đã tồn tại
                    merged_dict[ten_banh]['so_luong'] = banh.get('so_luong', merged_dict[ten_banh]['so_luong'])
                else:
                    # Thêm bánh mới
                    merged_dict[ten_banh] = {
                        'ten_banh': banh.get('ten_banh', ''),
                        'so_luong': banh.get('so_luong', 0)
                    }
        
        return list(merged_dict.values())
    
    def process_order_logic(self, message: str, order_id: Optional[int] = None) -> Dict[str, Any]:
        """
        Xử lý logic chính của đơn hàng
        """
        try:
            # If updating existing order
            if order_id:
                order_data = self.update_incomplete_order(order_id, message)
            else:
                # Analyze new message
                order_data = self.analyze_message(message)
            
            if 'error' in order_data:
                return {
                    'type': 'error',
                    'message': f'❌ Có lỗi xảy ra: {order_data["error"]}',
                    'data': order_data
                }
            
            # Save order info (for tracking)
            if not order_id:  # Only save new orders
                self.save_order_info(order_data)
            else:
                # For existing orders, they are already updated in update_incomplete_order method
                pass
            
            # Check completeness
            completeness_check = self.check_order_completeness(order_data)
            
            if completeness_check['is_complete']:
                # Order is complete, ask for confirmation
                confirmation_msg = self.generate_confirmation_message(order_data)
                return {
                    'type': 'confirmation',
                    'message': confirmation_msg,
                    'data': order_data,
                    'order_id': order_data.get('id')
                }
            else:
                # Order is incomplete, ask for missing info
                missing_info_msg = self.generate_missing_info_question(completeness_check['missing_fields'])
                return {
                    'type': 'missing_info',
                    'message': missing_info_msg,
                    'data': order_data,
                    'missing_fields': completeness_check['missing_fields'],
                    'order_id': order_data.get('id')
                }
                
        except Exception as e:
            return {
                'type': 'error',
                'message': f'❌ Có lỗi xảy ra khi xử lý đơn hàng: {str(e)}',
                'data': {}
            }
    
    def debug_order_info(self, order_data: Dict[str, Any], stage: str = "") -> None:
        """
        Debug method để log thông tin đơn hàng
        """
        try:
            print(f"\n=== DEBUG ORDER INFO {stage} ===")
            print(f"Order ID: {order_data.get('id', 'None')}")
            print(f"Customer: {order_data.get('ten_khach_hang', 'Empty')}")
            print(f"Phone: {order_data.get('so_dien_thoai', 'Empty')}")
            print(f"Address: {order_data.get('dia_chi', 'Empty')}")
            print(f"Time: {order_data.get('gio_giao', 'Empty')}")
            print(f"Cakes: {order_data.get('danh_sach_banh', [])}")
            print(f"Note: {order_data.get('ghi_chu', 'Empty')}")
            print("=" * 40)
        except Exception as e:
            print(f"Debug error: {e}")

    def clear_all_orders(self) -> bool:
        """
        Xóa tất cả đơn hàng (cho testing)
        """
        try:
            file_path = os.path.join(os.path.dirname(__file__), '..', '..', 'order_info.json')
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump([], f)
            return True
        except Exception as e:
            print(f"Error clearing orders: {str(e)}")
            return False
