#!/usr/bin/env python3
"""
Script test cho AI Agent Chatbot
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_analyze_message():
    """Test phân tích tin nhắn"""
    print("=== Test phân tích tin nhắn ===")
    
    test_messages = [
        "Chào bạn, tôi muốn đặt 2 chiếc bánh chocolate cho Nguyễn Văn A, số điện thoại 0123456789, giao tại 123 Đường ABC, Hà Nội lúc 14:00",
        "Đặt bánh kem vanilla 1 cái và 6 cupcake chocolate cho Trần Thị B, SĐT 0987654321, địa chỉ 456 XYZ Street, giao lúc 16:30, ghi chú: không đường",
        "Tôi cần 3 bánh tiramisu và 2 bánh kem sinh nhật, khách hàng Lê Văn C, 0901234567, giao tại 789 DEF Road lúc 18:00, sinh nhật con"
    ]
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n--- Test {i} ---")
        print(f"Tin nhắn: {message}")
        
        try:
            response = requests.post(
                f"{BASE_URL}/chatbot/analyze",
                json={"message": message},
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Thành công!")
                print("Kết quả phân tích:")
                data = result['data']
                
                # Hiển thị thông tin cơ bản
                print(f"  ID: {data.get('id')}")
                print(f"  Tên khách hàng: {data.get('ten_khach_hang')}")
                print(f"  Số điện thoại: {data.get('so_dien_thoai')}")
                print(f"  Địa chỉ: {data.get('dia_chi')}")
                print(f"  Giờ giao: {data.get('gio_giao')}")
                print(f"  Ghi chú: {data.get('ghi_chu')}")
                
                # Hiển thị danh sách bánh
                danh_sach_banh = data.get('danh_sach_banh', [])
                print(f"  Danh sách bánh ({len(danh_sach_banh)} loại):")
                for j, banh in enumerate(danh_sach_banh, 1):
                    print(f"    {j}. {banh.get('ten_banh')} - Số lượng: {banh.get('so_luong')}")
                    
            else:
                print(f"❌ Lỗi: {response.status_code}")
                print(response.text)
                
        except Exception as e:
            print(f"❌ Lỗi kết nối: {str(e)}")

def test_get_orders():
    """Test lấy danh sách đơn hàng"""
    print("\n=== Test lấy danh sách đơn hàng ===")
    
    try:
        response = requests.get(f"{BASE_URL}/chatbot/orders")
        
        if response.status_code == 200:
            orders = response.json()
            print(f"✅ Tìm thấy {len(orders)} đơn hàng")
            
            for i, order in enumerate(orders, 1):
                print(f"\n--- Đơn hàng {i} ---")
                print(f"  ID: {order.get('id')}")
                print(f"  Tên khách hàng: {order.get('ten_khach_hang')}")
                print(f"  Số điện thoại: {order.get('so_dien_thoai')}")
                print(f"  Địa chỉ: {order.get('dia_chi')}")
                print(f"  Giờ giao: {order.get('gio_giao')}")
                print(f"  Ghi chú: {order.get('ghi_chu')}")
                
                # Hiển thị danh sách bánh
                danh_sach_banh = order.get('danh_sach_banh', [])
                print(f"  Danh sách bánh ({len(danh_sach_banh)} loại):")
                for j, banh in enumerate(danh_sach_banh, 1):
                    print(f"    {j}. {banh.get('ten_banh')} - Số lượng: {banh.get('so_luong')}")
        else:
            print(f"❌ Lỗi: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Lỗi kết nối: {str(e)}")

def test_clear_orders():
    """Test xóa đơn hàng"""
    print("\n=== Test xóa đơn hàng ===")
    
    try:
        response = requests.delete(f"{BASE_URL}/chatbot/orders")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Xóa thành công!")
            print(f"Thông báo: {result['message']}")
        else:
            print(f"❌ Lỗi: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Lỗi kết nối: {str(e)}")

def show_sample_json():
    """Hiển thị mẫu cấu trúc JSON mong đợi"""
    print("\n=== Cấu trúc JSON mong đợi ===")
    sample = {
        "id": 1,
        "ten_khach_hang": "Nguyễn Văn An",
        "so_dien_thoai": "0901234567",
        "danh_sach_banh": [
            {
                "ten_banh": "Bánh kem sinh nhật chocolate",
                "so_luong": 1
            },
            {
                "ten_banh": "Bánh cupcake vanilla",
                "so_luong": 6
            }
        ],
        "dia_chi": "123 Đường Lê Lợi, Quận 1, TP.HCM",
        "gio_giao": "14:30",
        "ghi_chu": "Giao trước 15h, sinh nhật con"
    }
    print(json.dumps(sample, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    print("🚀 Bắt đầu test AI Agent Chatbot")
    print("Đảm bảo server đang chạy tại http://localhost:8000")
    print("Đảm bảo đã cấu hình GEMINI_API_KEY trong file .env")
    
    # Hiển thị mẫu cấu trúc JSON
    show_sample_json()
    
    # Test các chức năng
    test_analyze_message()
    test_get_orders()
    
    # Hỏi người dùng có muốn xóa đơn hàng không
    choice = input("\nBạn có muốn xóa tất cả đơn hàng không? (y/n): ")
    if choice.lower() == 'y':
        test_clear_orders()
    
    print("\n✅ Hoàn thành test!") 