import os
from dotenv import load_dotenv
from abc import ABC, abstractmethod

from llm_config import LLMConfig

load_dotenv()

class LLM(ABC):
    """
    Base class for handling general LLM interactions
    """

    def __init__(self, config: LLMConfig):
        super().__init__()
        self.config = config
        self.api_key_env_name = f"{self.config.provider.name}_API_KEY"
        if not self.api_key_env_name in os.environ:
            raise ValueError(f"{self.api_key_env_name} environment variable should be set in the '.env' file")


    def chat_loop(self):
        """Start the chat loop. 
        
        This is an interactive loop where the user can chat with the model.
        """
        while True:
            message = input("\nUSER: ")
            response = self.chat(message=message)
            print(f"\n{self.config.provider.name}: {response}")


    @abstractmethod
    def chat(self, message: str) -> str:
        """Chat with the model.
        
        This method should be implemented by the child class.
        It should take a message as input and return a response from the model.

        Args:
            message: The message to send to the model.
        """
        pass

    
    @abstractmethod
    def add_message_to_thread(self, message:str, role:str):
        """Add a message to the message thread to handle memory in the conversation.
        
        This method should be implemented by the child class.
        It should take a message and a role as input and add the message to the current thread.
        
        Args:
            message: The message to add to the thread.
            role: The role of the message (e.g. system, user, assistant).
        """

        pass


    @abstractmethod
    def log_usage(self, response):
        """Log the usage of the model.

        This method should be implemented by the child class.
        It should take a response from the model as input and log the token usage of the model.

        Args:
            response: The raw response from the model.
        """
        pass

    
    @abstractmethod
    def add_system_prompt(self, prompt:str):
        """Add a system prompt to the message thread.

        This method should be implemented by the child class.
        It should take a prompt as input and add it to the message thread with the role "system" or similar.

        Args:
            prompt: The prompt to add to the message thread.
        """
        pass