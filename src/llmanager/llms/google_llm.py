import sys

from google.ai import generativelanguage as glm
import google.generativeai as genai

from llm import LLM, LLMConfig
from logging_config import logger


#https://ai.google.dev/gemini-api/docs/get-started/python?hl=en

class GoogleLLM(LLM):
    """
    Class for handling Google LLM interactions.
    """

    def __init__(self, config: LLMConfig):
        super().__init__(config)
        self.name = "Google"
        genai.configure() # api_key defaults to os.getenv('GOOGLE_API_KEY')
        self.client = genai.GenerativeModel(self.config.model)
        self.messages = []
        #self.thread = self.client.start_chat(history=self.messages)

    def load_api_key(self):
        super().load_api_key()

    def chat_loop(self):
        print(f"Welcome to the {self.name} LLM chat loop!")
        return super().chat_loop()

    def add_message_to_thread(self, message:str, role:str):
        self.messages.append({"role": role, "parts": [message]})

    def add_system_prompt(self, prompt:str):
        self.add_message_to_thread(prompt, role="system")

    def log_usage(self, response: glm.GenerateContentResponse):
        logger.info(self.client.count_tokens(response.candidates[0].content.parts[0].text))

    def stream_response(self, response: glm.GenerateContentResponse):

        answer = ""

        for chunk in response:
            if chunk:
                yield chunk.text
                answer += chunk.text

        yield "\n"
        self.add_message_to_thread(answer, role="model")


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
            response = self.client.generate_content(
                self.messages,
                stream=self.config.stream,
                generation_config=genai.GenerationConfig(
                    max_output_tokens=self.config.max_tokens,
                    temperature=self.config.temperature,
                    top_p=self.config.top_p,
                    candidate_count=1 #self.config.n
                )
            )
            response.resolve()

        except Exception as e:
            logger.error(f"Error in {self.name}LLM.chat: {e}")
            sys.exit(1)


        if self.config.stream:
            return self.stream_response(response)

        else:

            # Log the token usage of the model.
            self.log_usage(response)

            # Get the response from the model.
            answer = response.candidates[0].content.parts[0].text

            self.add_message_to_thread(answer, role="model")

            return answer
