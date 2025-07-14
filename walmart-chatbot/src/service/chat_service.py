from src.agents.agent import Agent
from src.prompts.prompts import SALES_CHATBOT_PROMPT
from src.tools.stripe_payment import GenerateStripePaymentLink
from src.tools.book_meeting import GenerateCalendlyInvitationLink
from src.tools.file_search import GetStoreInfo
from src.tools.product_recommendation import GetProductRecommendation
import litellm

class ChatService:
    def __init__(self):
        # Initialize LiteLLM settings
        litellm.success_callback = ["langsmith"]
        
        # Choose the model
        self.model = "groq/llama3-70b-8192"
        
        # Initialize tools
        self.tools_list = [
            GenerateCalendlyInvitationLink,
            GetStoreInfo,
            GetProductRecommendation,
            GenerateStripePaymentLink,
        ]
        
        # Initialize the agent
        self.agent = Agent("Walmart Sales Agent", self.model, self.tools_list, system_prompt=SALES_CHATBOT_PROMPT)
        
        # Add initial message
        self.agent.messages.append({
            "role": "assistant",
            "content": "Hey, I am your Sales agent from Walmart Team. How can I help you?"
        })
    
    def get_initial_message(self):
        """Get the initial greeting message."""
        return self.agent.messages[-1]["content"]
    
    async def get_response(self, user_input: str) -> str:
        """
        Get a response from the agent for a given user input.
        
        Args:
            user_input (str): The user's message
            
        Returns:
            str: The agent's response
        """
        try:
            response = await self.agent.get_response(user_input)
            return response
        except Exception as e:
            return f"An error occurred: {str(e)}"
    
    def reset_conversation(self):
        """Reset the conversation to initial state."""
        self.agent.messages = []
        self.agent.messages.append({
            "role": "assistant",
            "content": "Hey, I am your Sales agent from Walmart Team. How can I help you?"
        })