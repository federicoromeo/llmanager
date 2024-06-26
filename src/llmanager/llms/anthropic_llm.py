import sys
import json

from anthropic import Anthropic

from llm import LLM, LLMConfig
from logging_config import logger


class AnthropicLLM(LLM):
    """
    Class for handling Anthropic LLM interactions.
    """

    def __init__(self, config: LLMConfig):
        super().__init__(config)
        self.name = "Anthropic"
        self.client = Anthropic()
        self.messages = []

    def load_api_key(self):
        super().load_api_key()

    def chat_loop(self):
        print(f"Welcome to the {self.name} LLM chat loop!")
        return super().chat_loop()

    def add_message_to_thread(self, message:str, role:str):
        self.messages.append({"role": role, "content": message})

    def add_system_prompt(self, prompt:str):
        self.add_message_to_thread(prompt, role="system")

    def log_usage(self, response):
        logger.info(response.usage)

    def stream_response(self, response):
        
        answer = ""
        for event in response:
            if event.type == 'content_block_delta':
                if event.delta.text:
                    yield event.delta.text
                    answer += event.delta.text

        yield "\n"
        self.add_message_to_thread(answer, role="assistant")

    def chat(self, message:str):
        """Function to query the model.

        Args:
            message: the message to send to the model

        Returns:
            The response from the model
        """
        self.add_message_to_thread(message, role="user")

        if self.config.json_mode:
            self.add_message_to_thread("Here is the JSON requested:\n{", role="assistant")

        # Query the model.
        try:
            response = self.client.messages.create(
                model = self.config.model,
                messages = self.messages,
                max_tokens = self.config.max_tokens,
                temperature = self.config.temperature,
                stream = self.config.stream,
            )
        except Exception as e:
            logger.error(f"Error in {self.name}LLM.chat: {e}")
            sys.exit(1)

        if self.config.stream:
            return self.stream_response(response)

        else:

            # Log the token usage of the model.
            self.log_usage(response)

            # Get the response from the model.
            answer = response.content[0].text

            # Convert the response to JSON
            if self.config.json_mode:
                try:
                    answer = json.loads("{" + answer[:answer.rfind("}") + 1])
                    self.messages[-1]['content'] += str(answer)[1:]
                except json.JSONDecodeError:
                    pass
            # Add the response to the message list.
            else:
                self.add_message_to_thread(answer, role="assistant")

            return answer

    def list_models(self):
        logger.info(f"Available models for {self.name} LLM:")
        models = ["claude-3-opus-20240229", "anthropic.claude-3-sonnet-20240229", "claude-3-haiku-20240307"]
        logger.info(models)