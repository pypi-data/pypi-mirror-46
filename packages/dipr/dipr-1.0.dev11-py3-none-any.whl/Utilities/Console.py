
import logging


class Console(object):

    __indent_string = []

    @staticmethod
    def configure_logging(level):
        log_level = logging.WARNING

        if level == 1:
            log_level = logging.INFO
        elif level == 2:
            log_level = logging.DEBUG

        logging.basicConfig(format='%(levelname)s: %(message)s', level=log_level)

    @staticmethod
    def push_indent(indent="> "):
        Console.__indent_string.append(indent)

    @staticmethod
    def pop_indent():
        if Console.__indent_string:
            Console.__indent_string = Console.__indent_string[:-1]

    @staticmethod
    def __apply_indent(msg):
        return "".join(Console.__indent_string) + msg

    @staticmethod
    def print(msg=""):
        if msg:
            print(Console.__apply_indent(msg))
        else:
            print()

    @staticmethod
    def debug(msg):
        logging.debug(Console.__apply_indent(msg))

    @staticmethod
    def info(msg):
        logging.info(Console.__apply_indent(msg))

    @staticmethod
    def warning(msg):
        logging.warning(Console.__apply_indent(msg))

    @staticmethod
    def error(msg):
        logging.error(Console.__apply_indent(msg))

    @staticmethod
    def critical(msg):
        logging.critical(Console.__apply_indent(msg))