from src.logger import get_logger

logger = get_logger(__name__)
logger.info("Logging is being done")
logger.error("Error occurred")
logger.warning("Warning issued")