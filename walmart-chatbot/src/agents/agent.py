from colorama import Fore, init
from litellm import completion
import json
import re

# Initialize colorama for colored terminal output
init(autoreset=True)

class Agent:
    """
    @title AI Agent Class
    @notice This class defines an AI agent that can uses function calling to interact with tools and generate responses.
    """

    def __init__(self, name, model, tools=None, system_prompt=""):
        """
        @notice Initializes the Agent class.
        @param model The AI model to be used for generating responses.
        @param tools A list of tools that the agent can use.
        @param available_tools A dictionary of available tools and their corresponding functions.
        @param system_prompt system prompt for agent behaviour.
        """
        self.name = name
        self.model = model
        self.messages = []
        self.tools = tools if tools is not None else []
        self.tools_schemas = self.get_openai_tools_schema() if self.tools else None
        self.system_prompt = system_prompt
        if self.system_prompt and not self.messages:
            self.handle_messages_history("system", self.system_prompt)

    async def get_response(self, message):
        if re.search(r"goodbye|bye", message, re.IGNORECASE):
            return "Goodbye! If you have any more questions, feel free to ask later."
        print(Fore.GREEN + f"\nCalling Agent: {self.name}")
        self.handle_messages_history("user", message)
        result = await self.execute()
        return result

    async def execute(self):
        """
        @notice Use LLM to generate a response and handle tool calls if needed.
        @return The final response.
        """
        try:
            # First, call the AI to get a response
            response = completion(
                model=self.model,
                messages=self.messages,
                tools=self.tools_schemas,
                tool_choice="auto"
            )
            
            # Extract the message from the response
            response_message = response.choices[0].message
            
            # Check if the message has tool calls
            tool_calls = getattr(response_message, 'tool_calls', None)
            
            if tool_calls:
                # Handle tool calls
                final_response = await self.run_tools(tool_calls)
                return getattr(final_response, 'content', str(final_response))
            else:
                # Return the direct message content
                return getattr(response_message, 'content', str(response_message))
                
        except Exception as e:
            print(Fore.RED + f"Error in execute: {str(e)}")
            return f"I apologize, but I encountered an error: {str(e)}"

    def call_llm(self):
        """
        @notice Call the LLM to get a response.
        @return The response from the LLM.
        """
        try:
            response = completion(
                model=self.model,
                messages=self.messages,
                tools=self.tools_schemas,
                tool_choice="auto"
            )
            return response.choices[0].message
        except Exception as e:
            print(Fore.RED + f"Error in LLM call: {str(e)}")
            return {"content": f"I apologize, but I encountered an error: {str(e)}"}

    async def run_tools(self, tool_calls):
        """
        @notice Run the tools called by the LLM.
        @param tool_calls The tool calls from the LLM response.
        @return The final response after running the tools.
        """
        # Add the assistant's response with tool calls to the message history
        self.handle_messages_history(
            "assistant",
            None,
            tool_calls=tool_calls,
        )

        # Process each tool call
        for tool_call in tool_calls:
            try:
                # Find the corresponding tool
                tool_name = tool_call.function.name
                tool = next(
                    (t for t in self.tools if t.name == tool_name),
                    None,
                )

                if tool:
                    # Execute the tool
                    args = tool_call.function.arguments
                    if isinstance(args, str):
                        try:
                            args = json.loads(args)
                        except json.JSONDecodeError:
                            pass
                            
                    result = await tool.execute(args)
                    
                    # Add the tool's response to the message history
                    self.handle_messages_history(
                        "tool",
                        str(result),
                        tool_call_id=tool_call.id,
                        name=tool_name,
                    )
                else:
                    print(Fore.RED + f"Tool {tool_name} not found")

            except Exception as e:
                print(Fore.RED + f"Error executing tool {tool_name}: {str(e)}")
                self.handle_messages_history(
                    "tool",
                    str(e),
                    tool_call_id=tool_call.id,
                    name=tool_name,
                )

        # Get the final response from the LLM
        final_response = self.call_llm()
        content = getattr(final_response, 'content', str(final_response))
        self.handle_messages_history("assistant", content)
        
        return final_response

    def handle_messages_history(
        self, role, content=None, tool_calls=None, tool_call_id=None, name=None
    ):
        """
        @notice Handle the message history by adding new messages.
        @param role The role of the message sender.
        @param content The content of the message.
        @param tool_calls Any tool calls in the message.
        @param tool_call_id The ID of the tool call.
        @param name The name of the tool.
        """
        message = {"role": role}

        if content is not None:
            message["content"] = content

        if tool_calls is not None:
            message["tool_calls"] = tool_calls

        if tool_call_id is not None:
            message["tool_call_id"] = tool_call_id

        if name is not None:
            message["name"] = name

        self.messages.append(message)

    def get_openai_tools_schema(self):
        """
        @notice Get the schema of available tools in OpenAI format.
        @return A list of tool schemas.
        """
        if not self.tools:
            return None

        tools_list = []
        for tool in self.tools:
            if hasattr(tool, 'get_schema'):
                tools_list.append(
                    {
                        "type": "function",
                        "function": tool.get_schema(),
                    }
                )
        return tools_list