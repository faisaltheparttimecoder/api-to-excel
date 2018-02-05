import logging
from colorlog import ColoredFormatter

# Logger name
log = logging.getLogger("logger")


# Initialize Logging
def init_logging(logging_level):
    """
    Initialize logging.
    """

    # The Log level and format.
    log_level = logging_level
    logformat = "%(log_color)s%(asctime)s [%(levelname)s] > %(message)s"

    # Set the level and color code the log messages.
    logging.root.setLevel(log_level)
    formatter = ColoredFormatter(logformat)
    stream = logging.StreamHandler()
    stream.setLevel(log_level)
    stream.setFormatter(formatter)

    # Assign the format to the logger variable
    log.setLevel(log_level)
    log.addHandler(stream)

    log.info("Setting up the logger is completed")

