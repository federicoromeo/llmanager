import json
from enum import Enum
from typing import Optional

import jsonschema
from pydantic import BaseModel


class Provider(Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
        
    def list_all():
        return [provider.value for provider in Provider]


class LLMConfig(BaseModel):

    # Model Parameters

    provider: Provider
    """The provider of the model"""
    
    model: str
    """The model name to be used"""

    # Chat Parameters

    max_tokens: Optional[int] = 3000
    """The maximum number of tokens to generate"""

    temperature: Optional[float] = 1.0
    """Tee temperature to use for generation"""

    top_p: Optional[float] = 1.0
    """The nucleus sampling probability"""

    seed: Optional[int] = None
    """The seed to use for generation"""

    json_mode: bool = False
    """Whether to use JSON mode or not"""

    stream: bool = False
    """Whether to stream the response or not"""

    # Logging Parameters

    verbose: bool = False
    """Whether to print verbose logs"""

    @classmethod
    def from_json(cls, provider: Provider, config_file_path: str):
        """Create an instance of LLMConfig from a JSON file.

        Args:
            provider (Provider): The provider of the model.
            config_file_path (str): The path to the JSON config file.

        Returns:
            LLMConfig: An instance of LLMConfig created from the JSON file.

        Raises:
            jsonschema.exceptions.ValidationError: If the JSON file does not match the schema.
        """
        with open(config_file_path, "r") as config_file:
            config_data = json.load(config_file)
            cls.validate_json(config_data)

        return cls(provider=provider, **config_data)

    @staticmethod
    def validate_json(config_data):
        """Validate the JSON data against the schema.

        Args:
            config_data (dict): The JSON data to validate.

        Raises:
            jsonschema.exceptions.ValidationError: If the JSON data does not match the schema.
        """
        schema = json.loads(json.dumps(LLMConfig.model_json_schema()))

        if 'provider' in schema['required']:
            schema['required'].remove('provider')  # Remove 'provider' from the list of required properties
        schema['additionalProperties'] = False  # Disallow additional properties

        jsonschema.validate(instance=config_data, schema=schema)
    