import requests
import json

# Test the /chatbot/process endpoint
def test_process_endpoint():
    url = "http://localhost:8000/chatbot/process"
    data = {
        "message": "Tôi muốn đặt bánh sinh nhật chocolate cho 10 người"
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ API hoạt động tốt!")
        else:
            print("❌ API có lỗi!")
            
    except Exception as e:
        print(f"Error: {e}")

# Test get all endpoints
def test_list_endpoints():
    url = "http://localhost:8000/docs"
    try:
        response = requests.get("http://localhost:8000/openapi.json")
        if response.status_code == 200:
            openapi_spec = response.json()
            print("Available endpoints:")
            for path, methods in openapi_spec.get("paths", {}).items():
                for method in methods.keys():
                    print(f"  {method.upper()} {path}")
        else:
            print("Cannot get OpenAPI spec")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("=== Testing API Endpoints ===")
    test_list_endpoints()
    print("\n=== Testing Process Endpoint ===")
    test_process_endpoint()
