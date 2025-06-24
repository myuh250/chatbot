import React, { useState, useRef, useEffect } from 'react';
import { Send, Bot, User, Cake, Clock, MapPin } from 'lucide-react';
import { historyService, chatbotService } from '../../services/chatbot';
import './homepage.css';

const Homepage = () => {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [userId] = useState('user_' + Math.random().toString(36).substr(2, 9)); // Tạo user ID ngẫu nhiên
  const messagesEndRef = useRef(null);

  // Load lịch sử chat khi component mount
  useEffect(() => {
    loadChatHistory();
  }, []);

  const loadChatHistory = async () => {
    try {
      const history = await historyService.getHistory(userId);
      
      // Convert API data to component format
      const formattedMessages = history.map(msg => ({
        id: msg.id,
        type: msg.role === 'user' ? 'user' : 'bot',
        content: msg.content,
        timestamp: new Date(msg.timestamp)
      }));
      
      setMessages(formattedMessages);
      
      // Nếu chưa có tin nhắn nào, thêm tin nhắn chào mừng
      if (history.length === 0) {
        const welcomeMessage = 'Xin chào! Tôi là trợ lý ảo của tiệm bánh. Tôi có thể giúp bạn đặt bánh, tư vấn sản phẩm, và trả lời các câu hỏi về dịch vụ của chúng tôi. Bạn cần hỗ trợ gì hôm nay?';
        await historyService.addMessage(userId, 'agent', welcomeMessage);
        loadChatHistory(); // Reload để lấy tin nhắn vừa thêm
      }
    } catch (error) {
      console.error('Error loading chat history:', error);
      // Fallback: hiển thị tin nhắn chào mừng offline
      setMessages([{
        id: 1,
        type: 'bot',
        content: 'Xin chào! Tôi là trợ lý ảo của tiệm bánh. Tôi có thể giúp bạn đặt bánh, tư vấn sản phẩm, và trả lời các câu hỏi về dịch vụ của chúng tôi. Bạn cần hỗ trợ gì hôm nay?',
        timestamp: new Date()
      }]);
    }
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async () => {
    if (!inputMessage.trim()) return;

    try {
      // Lưu tin nhắn user vào API
      const userMessageData = await historyService.addMessage(userId, 'user', inputMessage);
      
      const userMessage = {
        id: userMessageData.id,
        type: 'user',
        content: userMessageData.content,
        timestamp: new Date(userMessageData.timestamp)
      };

      setMessages(prev => [...prev, userMessage]);
      setInputMessage('');
      setIsTyping(true);

      // Generate bot response
      const botResponseContent = chatbotService.generateResponse(inputMessage);
      
      // Simulate typing delay
      setTimeout(async () => {
        try {
          // Lưu response của bot vào API  
          const botMessageData = await historyService.addMessage(userId, 'agent', botResponseContent);
          
          const botMessage = {
            id: botMessageData.id,
            type: 'bot',
            content: botMessageData.content,
            timestamp: new Date(botMessageData.timestamp)
          };
          
          setMessages(prev => [...prev, botMessage]);
          setIsTyping(false);
        } catch (error) {
          console.error('Error saving bot message:', error);
          // Fallback: hiển thị response nhưng không lưu vào API
          const botMessage = {
            id: Date.now(),
            type: 'bot',
            content: botResponseContent,
            timestamp: new Date()
          };
          setMessages(prev => [...prev, botMessage]);
          setIsTyping(false);
        }
      }, 1500);
      
    } catch (error) {
      console.error('Error sending message:', error);
      setIsTyping(false);
      // Có thể thêm thông báo lỗi cho user ở đây
    }
  };

  const formatTime = (date) => {
    return date.toLocaleTimeString('vi-VN', { 
      hour: '2-digit', 
      minute: '2-digit' 
    });
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
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
