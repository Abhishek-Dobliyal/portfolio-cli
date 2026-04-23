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
        self._stream_handler = logging.StreamHandler()
        self._formatter = logging.Formatter(self.log_format) if self.log_format else None
        self._file_handler = logging.FileHandler(self.log_file) if self.log_file else None
        self._logger = logging.getLogger(self.name)
        self._logger.setLevel(self.level)

        if self._formatter:
            if self._file_handler:
                self._file_handler.setFormatter(self._formatter)
                self._logger.addHandler(self._file_handler)

            self._stream_handler.setFormatter(self._formatter)       

        self._logger.addHandler(self._stream_handler)
        return self._logger

