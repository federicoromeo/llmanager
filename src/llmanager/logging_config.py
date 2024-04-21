import logging

logging.basicConfig(format="LOG.%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
