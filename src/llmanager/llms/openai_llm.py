import json
import logging

from openai import OpenAI

from llm import LLM, LLMConfig
from logging_config import logger


class OpenaiLLM(LLM):
    """
    Class for handling OpenAI LLM interactions.
    """

    def __init__(self, config: LLMConfig):
        super().__init__(config)
        self.client = OpenAI()
        self.messages = []


    def chat_loop(self):
        print("Welcome to the OpenAI LLM chat loop!")
        return super().chat_loop()
    

    def add_message_to_thread(self, message:str, role:str):
        self.messages.append({"role": role, "content": message})


    def add_system_prompt(self, prompt:str):
        self.add_message_to_thread(prompt, role="system")


    def log_usage(self, response):
        logger.log(logging.INFO, response.usage)


    def chat(self, message:str) -> str:
        """Function to query the model.

        Args:
            message: the message to send to the model

        Returns:
            The response from the model
        """

        self.add_message_to_thread(message, role="user")

        # Query the model.
        try:
            response = self.client.chat.completions.create(
                model = self.config.model,
                messages = self.messages,
                response_format = {"type": "json_object" if self.config.json_mode else "text"},
                max_tokens = self.config.max_tokens,
                temperature = self.config.temperature,
                seed = self.config.seed,
            )
        except Exception as e:
            logger.log(logging.ERROR, e)

        # Log the token usage of the model.
        self.log_usage(response)

        # Get the response from the model.
        answer = response.choices[0].message.content

        # Add the response to the message list.
        self.add_message_to_thread(answer, role="assistant")

        # Convert the response to JSON
        if self.config.json_mode:
            try:
                answer = json.loads(answer)
            except json.JSONDecodeError:
                pass

        return answer
