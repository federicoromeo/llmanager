import sys
import json

from openai import OpenAI

from llm import LLM, LLMConfig
from logging_config import logger


class OpenaiLLM(LLM):
    """
    Class for handling OpenAI LLM interactions.
    """

    def __init__(self, config: LLMConfig):
        super().__init__(config)
        self.name = "OpenAI"
        self.client = OpenAI()
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
        for chunk in response:
            delta = chunk.choices[0].delta.content
            if delta:
                answer += delta
                yield delta
        
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

        # Query the model.
        try:
            response = self.client.chat.completions.create(
                model = self.config.model,
                messages = self.messages,
                response_format = {"type": "json_object" if self.config.json_mode else "text"},
                max_tokens = self.config.max_tokens,
                temperature = self.config.temperature,
                seed = self.config.seed,
                n = 1, #self.config.n
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

    def list_models(self):
        logger.info(f"Available models for {self.name} LLM:")
        models = [model.id for model in self.client.models.list().data if str(model.id).startswith("gpt")]
        logger.info(models)
        