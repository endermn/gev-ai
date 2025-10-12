import logging


class GevaiLogger():
    '''A simple logger class that wraps around Python's built-in logging module.'''
    logger: logging.Logger
    formatter: logging.Formatter

    def __init__(self, name: str, file: str, level=logging.DEBUG) -> None:
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        self.logger.propagate = False

        if not self.logger.handlers:
            file_handler = logging.FileHandler(file, mode='w')
            self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

            file_handler.setFormatter(self.formatter)
            self.logger.addHandler(file_handler)

    def get_logger(self):
        return self.logger



