import logging


def get_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """
    Create and return a logger with the specified name and logging level.

    :param name: Name of the logger.
    :param level: Logging level (default is INFO).
    :return: Configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)

    # Create formatter and add it to the handler
    formatter = logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s")
    console_handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(console_handler)

    return logger
