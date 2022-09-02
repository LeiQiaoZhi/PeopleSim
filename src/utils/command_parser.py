# TODO: parse user commands, to browse history or simulation
import random
from utils.logger import Logger
from typing import *
from utils.history_logger import HistoryLogger


class Command:
    def __init__(self) -> None:
        pass

    def parse(self, text: str) -> bool:
        '''
        whether text is the command
        '''
        return False

    def execute(self) -> bool:
        '''
        return whether to break the loop
        '''
        return True


class ExitCommand(Command):
    def execute(self) -> bool:
        return True

    def parse(self, text: str):
        return text.lower() == "quit"


class ParseFailCommand(Command):
    def execute(self) -> bool:
        Logger.warn("Command not recognized. Type 'help' to show docs.")
        return False

    def parse(self, text) -> bool:
        return True


class HelpCommand(Command):
    def execute(self) -> bool:
        help_msg = (
            f"{Logger.title('Help Docs',char='-',total_length=40)}\n"
            f"{Logger.yellow('quit')}: quit simulation \n"
            f"{Logger.title('End of Help Docs',char='-',total_length=40)}"
        )
        Logger.important(help_msg)
        return False

    def parse(self, text) -> bool:
        return text.lower() == 'help'


class HistoryCommand(Command):
    '''
    history -> list people with number, input number to select
    history random -> random person's history

    '''

    def __init__(self, people, history_logger: HistoryLogger) -> None:
        self.people = people
        self.history_logger = history_logger
        self.second_arg = None
        super().__init__()

    def execute(self) -> bool:
        if self.second_arg == None:
            return False
        if self.second_arg == "":
            # TODO list ppl
            pass
        elif self.second_arg == "random":
            Logger.important("Showing you the history of a random person...")
            random_guy = random.choice(self.people)
            self.history_logger.print_history(random_guy.id)
        return False

    def parse(self, text) -> bool:
        if not text.startswith('history'):
            return False

        second_arg = text.split('history')[1].strip()
        self.second_arg = second_arg

        if second_arg == "" or "random":
            return True
        return False


class CommandParser:
    def __init__(self, commands: List[Command]) -> None:
        '''
        commands: in the order of command to parse
        '''
        self.commands = commands

    @staticmethod
    def get_default_parser(people, history_logger):
        commands = [
            ExitCommand(),
            HelpCommand(),
            HistoryCommand(people, history_logger),
            ParseFailCommand()
        ]
        return CommandParser(commands)

    def parse_command(self, text) -> Command:
        for command in self.commands:
            parse_success = command.parse(text)
            if parse_success:
                to_quit = command.execute()
                if to_quit:
                    quit()
                return
