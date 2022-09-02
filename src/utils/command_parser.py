# TODO: parse user commands, to browse history or simulation
from typing import *

class Command:
    def __init__(self) -> None:
        pass

    def parse(self,text) -> bool:
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

class CommandParser:
    def __init__(self, commands:List[Command]) -> None:
        self.commands =commands

    def parse_command(self,text) -> Command:
        for command in self.commands:
            command.parse(text)