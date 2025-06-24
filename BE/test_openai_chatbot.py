#!/usr/bin/env python3
"""
Test script for OpenAI Chatbot
Usage: python test_openai_chatbot.py
"""

import os
import json
from dotenv import load_dotenv
from app.api.chatbot.services import ChatbotService

# Load environment variables
load_dotenv()

def test_chatbot():
    """Test the chatbot with sample messages"""
    
    # Check if API key is set
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "your_openai_api_key_here":
        print("❌ Please set your OPENAI_API_KEY in .env file")
        print("Example: OPENAI_API_KEY=sk-your-actual-api-key")
        return
    
    try:
        # Initialize chatbot service
        chatbot = ChatbotService()
        print("✅ Chatbot service initialized successfully")
        
        # Test messages
        test_messages = [
            "Chào bạn, tôi muốn đặt bánh. Tên tôi là Nguyễn Văn An, số điện thoại 0901234567. Tôi muốn đặt 1 bánh kem sinh nhật chocolate và 6 bánh cupcake vanilla. Giao đến 123 Đường Lê Lợi, Quận 1, TP.HCM lúc 14:30. Ghi chú: Giao trước 15h, sinh nhật con.",
            
            "Tôi là Trần Thị Bình, số 0123456789. Đặt 2 bánh tiramisu và 1 bánh cheesecake. Địa chỉ: 456 Nguyễn Huệ, Quận 3, TP.HCM. Giao lúc 16:00.",
            
            "Đặt bánh cho tôi: 3 bánh mousse chocolate, 2 bánh red velvet. Tên: Lê Văn Cường, điện thoại: 0987654321. Giao 18:30 tại 789 Võ Văn Tần, Quận 5, TP.HCM. Cần giao gấp cho sinh nhật."
        ]
        
        print("\n🧪 Testing chatbot with sample messages...")
        
        for i, message in enumerate(test_messages, 1):
            print(f"\n--- Test {i} ---")
            print(f"Input: {message[:100]}...")
            
            # Analyze message
            result = chatbot.analyze_message(message)
            
            if 'error' in result:
                print(f"❌ Error: {result['error']}")
            else:
                print("✅ Analysis successful!")
                print("Extracted data:")
                print(json.dumps(result, ensure_ascii=False, indent=2))
                
                # Save to file
                save_success = chatbot.save_order_info(result)
                if save_success:
                    print("✅ Data saved to order_info.json")
                else:
                    print("❌ Failed to save data")
        
        # Show all orders
        print("\n📋 All orders in database:")
        orders = chatbot.get_all_orders()
        print(json.dumps(orders, ensure_ascii=False, indent=2))
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    test_chatbot() 