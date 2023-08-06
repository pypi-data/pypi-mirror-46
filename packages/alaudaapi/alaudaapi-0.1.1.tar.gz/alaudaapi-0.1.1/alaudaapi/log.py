import logging
import os

from alaudaapi import settings


class Logging(object):
    @classmethod
    def get_logger(cls):
        level = getattr(logging, settings.LOG_LEVEL, logging.INFO)
        if not os.path.exists(settings.LOG_PATH):
            os.mkdir(settings.LOG_PATH)
        log_path = "{}/{}".format(settings.LOG_PATH, "pytest.log")
        cls.logger = cls.create_logger('api-test', level, log_path)
        return cls.logger

    @classmethod
    def create_logger(cls, name, level, log_path):
        logger = logging.getLogger(name)
        logger.setLevel(level)

        if not logger.handlers:
            formatter = logging.Formatter(
                '%(asctime)s - %(filename)s - [%(levelname)s]'
                + '[%(lineno)d] %(message)s')
            file_handler = logging.FileHandler(log_path)
            file_handler.setLevel(level)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

            formatter = logging.Formatter('>  %(asctime)s - %(name)s - %(module)s - %(funcName)s - %(levelname)s '
                                          '- %(message)s')
            console_handler = logging.StreamHandler()
            console_handler.setLevel(level)
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)

        return logger


class Colored(object):
    RED = '\033[1;31m'  # 高亮红色

    RESET = '\033[0m'  # 终端默认颜色

    def color_str(self, color, s):
        return '{}{}{}'.format(
            getattr(self, color),
            s,
            self.RESET
        )

    def red(self, s):
        return self.color_str('RED', s)


logger = Logging.get_logger()
color = Colored()
