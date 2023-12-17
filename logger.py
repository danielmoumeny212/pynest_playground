import logging

class ColoredFormatter(logging.Formatter):
    COLORS = {
        'INFO': '\033[92m',  
        'WARNING': '\033[93m',  
        'ERROR': '\033[91m',    
        'CRITICAL': '\033[95m'  
    }
    RESET = '\033[0m'

    def format(self, record):
        log_message = super(ColoredFormatter, self).format(record)
        colored_levelname = f"{self.COLORS.get(record.levelname, '')}{record.levelname}{self.RESET}"
        return f"{colored_levelname}: {log_message}"

class Logger:
    def __init__(self, name, level=logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self._setup_logger()

    def _setup_logger(self):
        console_handler = logging.StreamHandler()
        console_handler.setLevel(self.logger.level)

        colored_formatter = ColoredFormatter(fmt="%(asctime)s [%(levelname)s]: %(message)s ", datefmt="%Y-%m-%d %H:%M:%S")
        console_handler.setFormatter(colored_formatter)

        self.logger.addHandler(console_handler)

    def set_level(self, level):
        self.logger.setLevel(level)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)

