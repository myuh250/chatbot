#!/usr/bin/env python3
"""
Script kiểm tra cấu hình Gemini API
"""

import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_gemini_config():
    """Kiểm tra cấu hình Gemini API"""
    print("🔍 Kiểm tra cấu hình Gemini API...")
    
    # Kiểm tra API key
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ GEMINI_API_KEY không tìm thấy trong file .env")
        print("📝 Hãy tạo file .env với nội dung:")
        print("GEMINI_API_KEY=your_actual_api_key_here")
        return False
    
    print(f"✅ API Key tìm thấy: {api_key[:10]}...")
    
    # Cấu hình Gemini
    try:
        genai.configure(api_key=api_key)
        print("✅ Cấu hình Gemini thành công")
    except Exception as e:
        print(f"❌ Lỗi cấu hình Gemini: {str(e)}")
        return False
    
    # Kiểm tra các model có sẵn
    models_to_try = [
        'gemini-1.5-flash',
        'gemini-1.5-pro',
        'gemini-2.0-flash'
    ]
    
    working_model = None
    for model_name in models_to_try:
        try:
            print(f"🔍 Thử model: {model_name}")
            model = genai.GenerativeModel(model_name)
            
            # Test với prompt đơn giản
            response = model.generate_content("Xin chào")
            print(f"✅ Model {model_name} hoạt động tốt!")
            working_model = model_name
            break
            
        except Exception as e:
            print(f"❌ Model {model_name} không hoạt động: {str(e)}")
            continue
    
    if working_model:
        print(f"\n🎉 Model hoạt động: {working_model}")
        print("💡 Cập nhật service để sử dụng model này")
        return True
    else:
        print("\n❌ Không tìm thấy model nào hoạt động")
        print("🔧 Hãy kiểm tra:")
        print("1. API key có đúng không")
        print("2. Tài khoản có quyền truy cập Gemini API không")
        print("3. Kết nối internet có ổn định không")
        return False

def list_available_models():
    """Liệt kê các model có sẵn"""
    print("\n📋 Liệt kê các model có sẵn...")
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        genai.configure(api_key=api_key)
        
        # Lấy danh sách model
        models = genai.list_models()
        print("Các model có sẵn:")
        for model in models:
            if 'generateContent' in model.supported_generation_methods:
                print(f"  - {model.name}")
                
    except Exception as e:
        print(f"❌ Không thể lấy danh sách model: {str(e)}")

if __name__ == "__main__":
    print("🚀 Bắt đầu kiểm tra Gemini API")
    
    if check_gemini_config():
        list_available_models()
    else:
        print("\n❌ Cấu hình không đúng. Vui lòng kiểm tra lại.") 