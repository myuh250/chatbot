import React, { useState, useRef, useEffect } from 'react';
import { Send, Bot, User, Cake, Clock, MapPin } from 'lucide-react';
import './homepage.css';

const Homepage = () => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'bot',
      content: 'Xin chào! Tôi là trợ lý ảo của tiệm bánh. Tôi có thể giúp bạn đặt bánh, tư vấn sản phẩm, và trả lời các câu hỏi về dịch vụ của chúng tôi. Bạn cần hỗ trợ gì hôm nay?',
      timestamp: new Date()
    }
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async () => {
    if (!inputMessage.trim()) return;

    const userMessage = {
      id: messages.length + 1,
      type: 'user',
      content: inputMessage,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsTyping(true);

    // Simulate bot response (replace with actual API call)
    setTimeout(() => {
      const botResponse = generateBotResponse(inputMessage);
      const botMessage = {
        id: messages.length + 2,
        type: 'bot',
        content: botResponse,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, botMessage]);
      setIsTyping(false);
    }, 1500);
  };

  const generateBotResponse = (userInput) => {
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
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const formatTime = (date) => {
    return date.toLocaleTimeString('vi-VN', { 
      hour: '2-digit', 
      minute: '2-digit' 
    });
  };

  const quickActions = [
    { text: 'Đặt bánh sinh nhật', icon: <Cake size={16} /> },
    { text: 'Xem bảng giá', icon: <Clock size={16} /> },
    { text: 'Địa chỉ cửa hàng', icon: <MapPin size={16} /> }
  ];

  return (
    <div className="chatbot-container">
      <div className="chat-header">
        <div className="header-content">
          <div className="bot-avatar">
            <Bot size={24} />
          </div>
          <div className="header-info">
            <h2>Bakery Assistant</h2>
            <p className="status">● Đang hoạt động</p>
          </div>
        </div>
      </div>

      <div className="chat-messages">
        {messages.map((message) => (
          <div key={message.id} className={`message ${message.type}`}>
            <div className="message-avatar">
              {message.type === 'bot' ? <Bot size={20} /> : <User size={20} />}
            </div>
            <div className="message-content">
              <div className="message-bubble">
                {message.content.split('\n').map((line, index) => (
                  <React.Fragment key={index}>
                    {line}
                    {index < message.content.split('\n').length - 1 && <br />}
                  </React.Fragment>
                ))}
              </div>
              <div className="message-time">
                {formatTime(message.timestamp)}
              </div>
            </div>
          </div>
        ))}
        
        {isTyping && (
          <div className="message bot">
            <div className="message-avatar">
              <Bot size={20} />
            </div>
            <div className="message-content">
              <div className="message-bubble typing">
                <div className="typing-dots">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="quick-actions">
        {quickActions.map((action, index) => (
          <button
            key={index}
            className="quick-action-btn"
            onClick={() => setInputMessage(action.text)}
          >
            {action.icon}
            <span>{action.text}</span>
          </button>
        ))}
      </div>

      <div className="chat-input">
        <div className="input-container">
          <textarea
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Nhập tin nhắn của bạn..."
            className="message-input"
            rows="1"
          />
          <button 
            onClick={handleSendMessage}
            className="send-btn"
            disabled={!inputMessage.trim() || isTyping}
          >
            <Send size={20} />
          </button>
        </div>
      </div>
    </div>
  );
};

export default Homepage;
