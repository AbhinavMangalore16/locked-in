import logging
import logging.config

def setup_logging(log_filename):
    logging.config.fileConfig('LOGS/logging.conf', disable_existing_loggers=False)

    for handler in logging.getLogger().handlers:
        if isinstance(handler, logging.FileHandler):
            handler.close()
            handler.baseFilename = log_filename
            handler.stream = open(log_filename, 'a')