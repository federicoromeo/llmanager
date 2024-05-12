import sys
import json
import logging
import argparse
from pydantic import ValidationError

from llm import LLM
from provider import Provider
from llm_config import LLMConfig
from logging_config import logger


logger.setLevel(logging.DEBUG)

def main(args: argparse.Namespace):
    """
    Main function to run the LLM chat loop.

    Args:
        args: The command line arguments
    """

    print()
    print("="*100)
    print()

    provider = Provider[args.provider.upper()]
    
    try:
        config = LLMConfig.from_json(provider, f"llms/configs/{provider.value}_config.json")
    except ValidationError as e:
        error = json.loads(e.json())[0]
        logger.error(f"Error when creating LLMConfig object, {error['msg']}: {error['loc']}")
        sys.exit(1)

    llm = LLM(config)

    if args.list and provider:
        llm.list_models()
        sys.exit(0)

    # Run the chat loop to interact with the model
    llm.chat_loop()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='LLM Manager')
    parser.add_argument(
        '--provider',
        required=True,
        type=str,
        choices=Provider.list_all(),
        help=f"Specify the provider. Available providers: {Provider.list_all()}"
    )
    parser.add_argument(
        '--list',
        required=False,
        default=False,
        action='store_true',
        help='List all available models for the specified provider'
    )
    
    args = parser.parse_args()

    main(args)
    