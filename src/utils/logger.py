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

    @staticmethod
    def title(text, char='*', length=5):
        return f"\n{char * length} {Logger.bold(text)} {char * length}\n"

    @staticmethod
    def print_title(text):
        print(Logger.title(text))

    @staticmethod
    def divider(char='=', length=50) -> str:
        return char * 50

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
    def purple(text) -> str:
        return f"{Logger.PURPLE}{text}{Logger.END}"

    @staticmethod
    def blue(text) -> str:
        return f"{Logger.BLUE}{text}{Logger.END}"

    @staticmethod
    def red(text) -> str:
        return f"{Logger.RED}{text}{Logger.END}"
