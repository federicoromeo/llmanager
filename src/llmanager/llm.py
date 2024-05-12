import os
from dotenv import load_dotenv
from abc import ABC, abstractmethod

from llm_config import LLMConfig
from logging_config import logger

load_dotenv()

class LLM(ABC):
    """
    Base class for handling general LLM interactions
    """
    
    def __new__(cls, config: LLMConfig):
        if cls is LLM:
            # Dynamically import the module and class
            module_name = f"llms.{config.provider.value}_llm"
            class_name = f"{config.provider.value.capitalize()}LLM"
            module = __import__(module_name, fromlist=[module_name])
            ProviderLLM = getattr(module, class_name, None)
            # Check if the class was found in the module
            if ProviderLLM is None:
                raise ValueError(f"LLM '{class_name}' not found in module {__name__}")
            return super(LLM, ProviderLLM).__new__(ProviderLLM)
        return super().__new__(cls)
    
    def __init__(self, config: LLMConfig):
        super().__init__()
        self.config = config
        if type(self) is LLM:
            raise TypeError("Cannot instantiate LLM directly")
        if self.config.verbose:
            logger.debug("Config:")
            for key, value in self.config.model_dump().items():
                logger.debug(f" - {key}: {value}")
        self.load_api_key()
        
    def load_api_key(self):
        """Load the API key from the environment variable.
        
        This method loads the API key from the environment variable.
        """
        self.api_key_env_name = f"{self.config.provider.name}_API_KEY"
        if self.config.verbose:
            logger.debug(f"API Key Environment Variable: {self.api_key_env_name}: {os.getenv(self.api_key_env_name)}")
        if not self.api_key_env_name in os.environ:
            raise ValueError(f"{self.api_key_env_name} environment variable should be set in the '.env' file")

    @abstractmethod
    def stream_response(self, response):
        """Stream the response from the model.
        
        This method takes a response from the model and streams it to the console.
        
        Args:
            response: The response from the model as a generator
        """
        pass

    def chat_loop(self):
        """Start the chat loop. 
        
        This is an interactive loop where the user can chat with the model.
        """
        while True:
            message = input("\nUSER: ")
            response = self.chat(message=message)
            if self.config.stream:
                chunks = iter(response)
                first_chunk = next(chunks)
                print(f"\n{self.config.provider.name}: {first_chunk}", end="")
                for chunk in chunks:
                    print(chunk, end="")
            else:
                print(f"\n{self.config.provider.name}: {response}")

    @abstractmethod
    def chat(self, message: str):
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

    @abstractmethod
    def list_models(self):
        """List the available models for the provider.

        This method should be implemented by the child class.
        It should list the available models for the provider.
        """
        pass