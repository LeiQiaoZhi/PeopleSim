from turtle import title


class Logger:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

    DEBUG = 0
    INFO = 1
    IMPORTANT = 2
    TITLE = 3
    WARNING = 4
    ERROR = 5

    LEVEL = 1

    @staticmethod
    def set_level(level: int):
        Logger.LEVEL = level

    ### print methods ###
    @staticmethod
    def debug(text):
        if Logger.LEVEL > Logger.DEBUG:
            return
        print(text)

    @staticmethod
    def info(text):
        if Logger.LEVEL > Logger.INFO:
            return
        print(text)

    @staticmethod
    def important(text, color=None):
        if Logger.LEVEL > Logger.IMPORTANT:
            return
        if color != None:
            text = color + text + Logger.END
        print(Logger.bold(text))

    @staticmethod
    def print_title(text, char='*', length=5, total_length=None, divider: str = ""):
        if Logger.LEVEL > Logger.TITLE:
            return
        print(Logger.title(text, char,
              length, total_length=total_length, divider=divider))

    @staticmethod
    def warn(text):
        if Logger.LEVEL > Logger.WARNING:
            return
        print('Warning: ' + Logger.yellow(text))

    @staticmethod
    def error(text):
        if Logger.LEVEL > Logger.ERROR:
            return
        print('Error: ' + Logger.red(text))

    ### decorator methods ###

    @staticmethod
    def title(text, char='*', length=5, total_length=None, divider=""):
        if total_length != None and len(text) <= total_length:
            length = (total_length - len(text) - 2) // (2*len(char))
        return f"{divider}\n{char * length} {Logger.bold(text)} {char * length}\n{divider}"

    @staticmethod
    def divider(char='=', length=50) -> str:
        return char * (length // len(char))

    @staticmethod
    def bold(text) -> str:
        return f"{Logger.BOLD}{text}{Logger.END}"

    @staticmethod
    def underline(text) -> str:
        return f"{Logger.UNDERLINE}{text}{Logger.END}"

    @staticmethod
    def yellow(text) -> str:
        return f"{Logger.YELLOW}{text}{Logger.END}"

    @staticmethod
    def cyan(text) -> str:
        return f"{Logger.CYAN}{text}{Logger.END}"

    @staticmethod
    def dark_cyan(text) -> str:
        return f"{Logger.CYAN}{text}{Logger.END}"

    @staticmethod
    def purple(text) -> str:
        return f"{Logger.PURPLE}{text}{Logger.END}"

    @staticmethod
    def blue(text) -> str:
        return f"{Logger.BLUE}{text}{Logger.END}"

    @staticmethod
    def red(text) -> str:
        return f"{Logger.RED}{text}{Logger.END}"

    @staticmethod
    def green(text) -> str:
        return f"{Logger.GREEN}{text}{Logger.END}"
