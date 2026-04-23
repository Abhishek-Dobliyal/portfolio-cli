import logging


class Logger:
    DEFAULT_LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    def __init__(self, name, log_file=None, 
                level=logging.DEBUG,
                log_format=None):
        self.name = name
        self.log_file = log_file
        self.level = level
        self.log_format = log_format if log_format else Logger.DEFAULT_LOG_FORMAT
    
    def get_logger(self):
        """ Instantiates and returns the custom logger """
        logger = logging.getLogger(self.name)
        logger.setLevel(self.level)
        logger.propagate = False

        if logger.handlers:
            return logger

        stream_handler = logging.StreamHandler()
        formatter = logging.Formatter(self.log_format) if self.log_format else None
        file_handler = logging.FileHandler(self.log_file) if self.log_file else None

        if formatter:
            stream_handler.setFormatter(formatter)
            if file_handler:
                file_handler.setFormatter(formatter)

        logger.addHandler(stream_handler)

        if file_handler:
            logger.addHandler(file_handler)

        return logger

