import sys
import json
import logging
import argparse
from pydantic import ValidationError

from llm_config import LLMConfig
from provider import Provider
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
        logger.debug(f"Verbose mode enabled")
        logger.debug(f"Args: {args}")

    # Dispatch the main function based on the provider

    module_name = f"llms.{provider.value}_llm"
    class_name = f"{provider.value.capitalize()}LLM"
    if verbose:
        logger.debug(f"Using {provider.name} provider")
        logger.debug(f"Module name: {module_name}")
        logger.debug(f"Class name: {class_name}")

    try:
        module = __import__(module_name, fromlist=[module_name])
        if verbose:
            logger.debug(f"Module: {module}")
    except (ModuleNotFoundError, ImportError) as e:
        logger.error(f"Support for {provider.name} has not been implemented yet ({e})")
        sys.exit(1)

    ProviderLLM = getattr(module, class_name, None)
    if verbose:
        logger.debug(f"ProviderLLM: {ProviderLLM}")

    if not ProviderLLM:
        logger.error(f"Support for {provider.name} has not been implemented yet")
        sys.exit(1)

    return ProviderLLM

def main(args: argparse.Namespace):
    """
    Main function to run the LLM chat loop.

    Args:
        args: The command line arguments
    """

    provider = Provider[args.provider.upper()]

    providerLLM = load_provider_llm(args)

    print()
    print("="*100)
    print()
    
    try:
        config = LLMConfig.from_json(provider, f"llms/configs/{provider.value}_config.json")
    except ValidationError as e:
        error = json.loads(e.json())[0]
        logger.error(f"Error when creating LLMConfig object, {error['msg']}: {error['loc']}")
        sys.exit(1)

    llm = providerLLM(config)

    if args.list and provider:
        llm.list_models()
        sys.exit(0)

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
    parser.add_argument(
        "--verbose",
        required=False,
        default=False,
        action="store_true",
        help="Enable verbose logging",
    )
    
    args = parser.parse_args()

    main(args)
    