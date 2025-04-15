from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
from tools import tools

load_dotenv()  # This loads variables from .env into environment

# Make you add the OPENAI_API_KEY to the .env file
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

class AI:
    def __init__(self):
        # Setup model and temperature
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
        
        # Bind the llm to our tools and force tool choice
        self.ai = self.llm.bind_tools(tools, tool_choice="required")
        
        # Setup system prompt
        self.system_prompt = """
        You are a fast food ordering assistant. You can help customers place or cancel orders.
        
        For orders, you can only accept:
        - Burgers
        - Fries  
        - Drinks
        
        You must use the addOrder tool when a customer wants to place an order, specifying the quantity of each item.
        You must use the deleteOrder tool when a customer wants to cancel an order.
        
        Do not engage in any other conversations or tasks besides order management.
        Always use the appropriate tool for every customer interaction.
        """

    def generate_response(self, prompt) -> dict:
        # Setup messages
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": prompt}
        ]
        
        # Invoke the AI with the messages
        result = self.ai.invoke(messages)
        
        # Get tool calls and their args
        output = {}
        
        for tool_call in result.tool_calls:
            tool_name = tool_call['name']
            tool_args = tool_call['args']
            output[tool_name] = tool_args
        
        return output
