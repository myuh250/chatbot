# AI Chatbot for Cake Ordering

Hệ thống AI chatbot sử dụng OpenAI API (model gpt-4o-mini) để thu thập thông tin đặt bánh từ người dùng và xuất ra file JSON.

## Tính năng

- Phân tích tin nhắn chat để trích xuất thông tin đơn hàng
- Tự động lưu thông tin vào file `order_info.json`
- API RESTful để tương tác với chatbot
- Hỗ trợ nhiều loại bánh trong một đơn hàng
- Trích xuất thông tin: tên khách hàng, số điện thoại, địa chỉ, giờ giao, ghi chú
- Sử dụng model gpt-4o-mini để tối ưu chi phí

## Cài đặt

### 1. Cài đặt dependencies

```bash
pip install -r requirements.txt
```

### 2. Cấu hình API Key

Tạo file `.env` trong thư mục `BE/` với nội dung:

```env
OPENAI_API_KEY=sk-your-actual-openai-api-key-here
```

### 3. Chạy server

```bash
cd BE
python main.py
```

Server sẽ chạy tại `http://localhost:8000`

## API Endpoints

### POST /chatbot/analyze
Phân tích tin nhắn và trích xuất thông tin đơn hàng

**Request:**
```json
{
    "message": "Chào bạn, tôi muốn đặt bánh. Tên tôi là Nguyễn Văn An, số điện thoại 0901234567..."
}
```

**Response:**
```json
{
    "success": true,
    "data": {
        "id": 1,
        "ten_khach_hang": "Nguyễn Văn An",
        "so_dien_thoai": "0901234567",
        "danh_sach_banh": [
            {
                "ten_banh": "Bánh kem sinh nhật chocolate",
                "so_luong": 1
            }
        ],
        "dia_chi": "123 Đường Lê Lợi, Quận 1, TP.HCM",
        "gio_giao": "14:30",
        "ghi_chu": "Giao trước 15h, sinh nhật con"
    },
    "message": "Message analyzed successfully"
}
```

### GET /chatbot/orders
Lấy tất cả thông tin đơn hàng đã được phân tích

### DELETE /chatbot/orders
Xóa tất cả thông tin đơn hàng (reset)

## Cấu trúc dữ liệu

File `order_info.json` có cấu trúc:

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

## Testing

Chạy test script để kiểm tra hệ thống:

```bash
cd BE
python test_openai_chatbot.py
```

## Swagger Documentation

Truy cập `http://localhost:8000/docs` để xem tài liệu API đầy đủ.

## Lưu ý

- Đảm bảo có API key OpenAI hợp lệ
- File `order_info.json` sẽ được tạo tự động khi có đơn hàng đầu tiên
- Hệ thống hỗ trợ tiếng Việt và có thể xử lý các định dạng tin nhắn khác nhau
- Sử dụng model gpt-4o-mini để tối ưu chi phí (rẻ hơn gpt-4o nhưng hiệu suất tốt hơn gpt-3.5-turbo) 