import sys
import json
import logging
import argparse
from pydantic import ValidationError

from llm_config import LLMConfig, Provider
from logging_config import logger


logger.setLevel(logging.DEBUG)

def load_provider_llm(args: argparse.Namespace):
    """
    Load the provider specific LLM class and run the
    chat loop.

    Args:
        args: The command line arguments
    """

    # Load the cmd arguments
    verbose = args.verbose
    provider = Provider[args.provider.upper()]

    if verbose:
        logger.log(logging.DEBUG, f"Verbose mode enabled")
        logger.log(logging.DEBUG, f"Args: {args}")

    # Dispatch the main function based on the provider

    module_name = f"llms.{provider.value}_llm"
    class_name = f"{provider.value.capitalize()}LLM"
    if verbose:
        logger.log(logging.DEBUG, f"Using {provider.name} provider")
        logger.log(logging.DEBUG, f"Module name: {module_name}")
        logger.log(logging.DEBUG, f"Class name: {class_name}")

    try:
        module = __import__(module_name, fromlist=[module_name])
        if verbose:
            logger.log(logging.DEBUG, f"Module: {module}")
    except (ModuleNotFoundError, ImportError) as e:
        logger.log(logging.ERROR, f"Support for {provider.name} has not been implemented yet ({e})")
        sys.exit(1)

    ProviderLLM = getattr(module, class_name, None)
    if verbose:
        logger.log(logging.DEBUG, f"ProviderLLM: {ProviderLLM}")

    if not ProviderLLM:
        logger.log(logging.ERROR, f"Support for {provider.name} has not been implemented yet")
        sys.exit(1)

    return ProviderLLM

def main(args: argparse.Namespace):
    """
    Main function to run the LLM chat loop.

    Args:
        args: The command line arguments
    """

    provider = Provider[args.provider.upper()]

    ProviderLLM = load_provider_llm(args)

    print()
    print("="*100)
    print()
    
    try:
        config = LLMConfig.from_json(provider, f"llms/{provider.value}_config.json")
    except ValidationError as e:
        error = json.loads(e.json())[0]
        logger.log(logging.ERROR, f"Error when creating LLMConfig object, {error['msg']}: {error['loc']}")
        sys.exit(1)

    llm = ProviderLLM(config)

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
        "--verbose",
        required=False,
        default=False,
        action="store_true",
        help="Enable verbose logging",
    )
    
    args = parser.parse_args()

    main(args)
    