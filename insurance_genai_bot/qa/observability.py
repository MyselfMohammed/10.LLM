import logging
import os

def setup_logger(log_file="logs/qa.log"):
    # Make sure the logs directory exists!
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)
    logger = logging.getLogger("qa_logger")
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(log_file)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    if not logger.handlers:
        logger.addHandler(handler)
    return logger


def log_response(logger, user_query, answer, checks):
    logger.info(f"QUERY: {user_query}\nANSWER: {answer}\nCHECKS: {checks}")
