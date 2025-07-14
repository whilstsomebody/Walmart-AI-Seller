from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.service.chat_service import ChatService

app = FastAPI()

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize chat service
chat_service = ChatService()

class ChatMessage(BaseModel):
    message: str

@app.get("/")
async def health_check():
    return {"status": "healthy"}

@app.get("/chat/initial")
async def get_initial_message():
    """Get the initial greeting message."""
    return {"message": chat_service.get_initial_message()}

@app.post("/chat/message")
async def send_message(chat_message: ChatMessage):
    """
    Send a message to the chatbot and get a response.
    """
    try:
        response = await chat_service.get_response(chat_message.message)
        return {"message": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat/reset")
async def reset_chat():
    """Reset the chat conversation."""
    chat_service.reset_conversation()
    return {"message": "Conversation reset successfully"}