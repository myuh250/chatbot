# workflow -> prompt của người dùng -> đưa qua llm -> llm trả về các features ở dạng json -> lưu dữ liệu này ở dạng file json
# -> api history sẽ dùng file json để đưa data lên frontend

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.history.routes import router as history_router
# nếu có chatbot routes thì import thêm
# from app.api.chatbot.routes import router as chatbot_router

app = FastAPI(title="AI Agent Chatbot")

# Cấu hình CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(history_router)
# app.include_router(chatbot_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)