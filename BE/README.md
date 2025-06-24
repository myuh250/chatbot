# AI Agent Chatbot Backend

## Cấu hình

### 1. Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### 2. Cấu hình Gemini API
1. Đăng ký tài khoản tại https://makersuite.google.com/app/apikey
2. Tạo API key mới
3. Tạo file `.env` trong thư mục BE với nội dung:
```
GEMINI_API_KEY=your_actual_api_key_here
```

## Chạy ứng dụng
```bash
python main.py
```

Server sẽ chạy tại: http://localhost:8000

## API Endpoints

### POST /chatbot/analyze
Phân tích tin nhắn chat và trích xuất thông tin đơn hàng

**Request:**
```json
{
  "message": "Chào bạn, tôi muốn đặt 2 chiếc bánh chocolate và 1 bánh kem vanilla cho Nguyễn Văn A, số điện thoại 0123456789, giao tại 123 Đường ABC, Hà Nội lúc 14:00"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "ten_khach_hang": "Nguyễn Văn A",
    "so_dien_thoai": "0123456789",
    "danh_sach_banh": [
      {
        "ten_banh": "bánh chocolate",
        "so_luong": 2
      },
      {
        "ten_banh": "bánh kem vanilla",
        "so_luong": 1
      }
    ],
    "dia_chi": "123 Đường ABC, Hà Nội",
    "gio_giao": "14:00",
    "ghi_chu": null,
    "timestamp": "2024-01-01T12:00:00",
    "original_message": "..."
  },
  "message": "Message analyzed successfully"
}
```

### GET /chatbot/orders
Lấy tất cả thông tin đơn hàng đã được phân tích

### DELETE /chatbot/orders
Xóa tất cả thông tin đơn hàng (reset)

## Cấu trúc dữ liệu

Thông tin đơn hàng được lưu trong file `app/order_info.json` với cấu trúc:

```json
[
  {
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
]
```

### Các trường thông tin:
- `id`: ID đơn hàng (tự động tạo)
- `ten_khach_hang`: Tên khách hàng
- `so_dien_thoai`: Số điện thoại
- `danh_sach_banh`: Danh sách các loại bánh đã đặt
  - `ten_banh`: Tên bánh
  - `so_luong`: Số lượng (số nguyên)
- `dia_chi`: Địa chỉ giao hàng
- `gio_giao`: Giờ giao hàng
- `ghi_chu`: Ghi chú (nếu có)

## Test

Chạy script test để kiểm tra hệ thống:
```bash
python test_chatbot.py
``` 