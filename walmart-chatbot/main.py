import litellm
from colorama import Fore
from dotenv import load_dotenv
from src.agents.agent import Agent
from src.prompts.prompts import SALES_CHATBOT_PROMPT
from src.tools.stripe_payment import GenerateStripePaymentLink
from src.tools.book_meeting import GenerateCalendlyInvitationLink
from src.tools.file_search import GetStoreInfo
from src.tools.product_recommendation import GetProductRecommendation


# Load environment variables from a .env file
load_dotenv()

# set langfuse as a callback, litellm will send the data to langfuse
litellm.success_callback = ["langsmith"]

# litellm.set_verbose = True

# Choose any model with LiteLLM
model = "groq/llama3-70b-8192"
# model = "groq/llama-3.1-70b-versatile"
# model = "gemini/gemini-1.5-pro"

# agent tools
tools_list = [
    GenerateCalendlyInvitationLink,
    GetStoreInfo,
    GetProductRecommendation,
    GenerateStripePaymentLink,
]

# Initiate the sale agent
agent = Agent("Walmart Sales Agent", model, tools_list, system_prompt=SALES_CHATBOT_PROMPT)

# Add initial/introduction chatbot message
agent.messages.append(
    {
        "role": "assistant",
        "content": "Hey, I am your Sales agent from Walmart Team. How can I help you?",
    }
)

print(
    Fore.BLUE
    + "Enter discussion with Walmart Sales Agent! Type 'exit' to end the conversation."
)
print(Fore.BLUE + f"Sales Bot: {agent.messages[-1]['content']}")
while True:
    user_input = input(Fore.YELLOW + "You: ")
    if user_input.lower() == "exit":
        print(Fore.BLUE + "Walmart Sales Agent: Goodbye!")
        break
    response = agent.invoke(user_input)
    print(Fore.BLUE + f"Walmart Sales Agent: {response}")
