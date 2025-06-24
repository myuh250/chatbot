const API_BASE_URL = 'http://localhost:8000';

// Service để gọi API history
export const historyService = {
  // Thêm message mới
  async addMessage(userId, role, content) {
    try {
      const response = await fetch(`${API_BASE_URL}/history/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_id: userId,
          role: role,
          content: content
        })
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('Error adding message:', error);
      throw error;
    }
  },

  // Lấy lịch sử chat
  async getHistory(userId = null) {
    try {
      const url = userId 
        ? `${API_BASE_URL}/history/?user_id=${userId}`
        : `${API_BASE_URL}/history/`;
      
      const response = await fetch(url);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('Error getting history:', error);
      throw error;
    }
  }
};

// Service cho chatbot
export const chatbotService = {
  // Xử lý tin nhắn với logic đầy đủ (API mới)
  async processMessage(userInput, orderId = null) {
    try {
      const response = await fetch(`${API_BASE_URL}/chatbot/process`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          message: userInput,
          order_id: orderId 
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error processing message:', error);
      throw error;
    }
  },

  // Xác nhận đơn hàng
  async confirmOrder(orderId) {
    try {
      const response = await fetch(`${API_BASE_URL}/chatbot/confirm`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ order_id: orderId }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error confirming order:', error);
      throw error;
    }
  },

  // Lấy đơn hàng đã xác nhận
  async getConfirmedOrders() {
    try {
      const response = await fetch(`${API_BASE_URL}/chatbot/confirmed-orders`);

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error getting confirmed orders:', error);
      throw error;
    }
  },

  // Phân tích và lưu đơn hàng (API cũ - vẫn giữ để tương thích)
  async analyzeAndSaveOrder(userInput) {
    try {
      const response = await fetch(`${API_BASE_URL}/chatbot/analyze`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: userInput }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error analyzing and saving order:', error);
      throw error;
    }
  },

  // Tạo bot response (tạm thời dùng logic cũ, sau này có thể call API chatbot)
  generateResponse(userInput) {
    const input = userInput.toLowerCase();
    
    if (input.includes('đặt bánh') || input.includes('order') || input.includes('mua')) {
      return 'Tuyệt vời! Để đặt bánh, bạn vui lòng cho tôi biết:\n• Loại bánh bạn muốn\n• Số lượng\n• Thời gian nhận hàng\n• Địa chỉ giao hàng (nếu cần)\n\nChúng tôi có bánh sinh nhật, bánh cưới, bánh kem, bánh mì và nhiều loại khác!';
    }
    
    if (input.includes('giá') || input.includes('price') || input.includes('bao nhiêu')) {
      return 'Bảng giá các sản phẩm của chúng tôi:\n• Bánh sinh nhật: 250,000 - 1,500,000 VNĐ\n• Bánh kem nhỏ: 150,000 - 300,000 VNĐ\n• Bánh mì: 15,000 - 25,000 VNĐ\n• Bánh ngọt: 20,000 - 80,000 VNĐ\n\nGiá có thể thay đổi tùy theo kích thước và thiết kế!';
    }
    
    if (input.includes('địa chỉ') || input.includes('address') || input.includes('ở đâu')) {
      return 'Tiệm bánh của chúng tôi tọa lạc tại:\n📍 123 Đường ABC, Quận 1, TP.HCM\n📞 Hotline: 0123-456-789\n🕒 Giờ mở cửa: 7:00 - 22:00 hàng ngày\n\nChúng tôi cũng có dịch vụ giao hàng tận nơi!';
    }
    
    return 'Cảm ơn bạn đã liên hệ! Tôi đã ghi nhận thông tin của bạn. Nhân viên của chúng tôi sẽ liên hệ lại trong thời gian sớm nhất để hỗ trợ bạn tốt hơn. Bạn có thể đặt thêm câu hỏi khác không?';
  }
};