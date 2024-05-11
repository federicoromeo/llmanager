import sys
import json
import requests

import ollama

from llm import LLM, LLMConfig
from logging_config import logger


# RUN curl -fsSL https://ollama.com/install.sh | sh
class OllamaLLM(LLM):
    """
    Class for handling Ollama LLM interactions.
    """

    def __init__(self, config: LLMConfig):
        super().__init__(config)
        self.name = "Ollama"
        self.client = ollama.Client()
        self.messages = []

    def load_api_key(self):
        pass

    def chat_loop(self):
        print(f"Welcome to the {self.name} LLM chat loop!")
        return super().chat_loop()

    def add_message_to_thread(self, message: str, role: str):
        self.messages.append({"role": role, "content": message})

    def add_system_prompt(self, prompt: str):
        self.add_message_to_thread(prompt, role="system")

    def log_usage(self, response):
        logger.info(f"Usage: {response['eval_count']} tokens")

    def stream_response(self, response):
        
        answer = ""
        for chunk in response:
            delta = chunk['message']['content']
            if delta:
                answer += delta
                yield delta

        self.add_message_to_thread(answer, role="assistant")

    def chat(self, message: str):
        """Function to query the model.

        Args:
            message: the message to send to the model

        Returns:
            The response from the model
        """

        models = [model['name'] for model in ollama.list()['models']]
        if self.config.model not in models:
            logger.info(f"Pulling model {self.config.model}...")
            ollama.pull(self.config.model)
            logger.info("Model pulled successfully.")

        self.add_message_to_thread(message, role="user")

        # Query the model.
        try:
            response = ollama.chat(
                model=self.config.model,
                messages=self.messages,
                format="json" if self.config.json_mode else "",
                stream=self.config.stream,
                options=ollama._types.Options(
                    seed=self.config.seed,
                    temperature=self.config.temperature,
                    top_p=self.config.top_p
                )
            )
        except Exception as e:
            logger.error(f"Error in {self.name}LLM.chat: {e}")
            sys.exit(1)

        if self.config.stream:
            return self.stream_response(response)

        else:
            logger.info(response)
            logger.info(response.keys())

            # Log the token usage of the model.
            self.log_usage(response)

            # Get the response from the model.
            answer = response['message']['content']

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
        logger.info(f"Pulled models for {self.name} LLM:")
        models = [model['name'] for model in ollama.list()['models']]
        logger.info(models)
        logger.info("-"*50)
        logger.info(f"Available models for {self.name} LLM:")
        models = requests.get("https://ollama-models.zwz.workers.dev/").json()['models']
        models_with_tag = [f"{element['name']}:{tag}" for element in models for tag in element['tags']]
        logger.info(models_with_tag)