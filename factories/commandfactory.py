from commands.commandbase import CommandBase
from commands.mainview.cellclicked import CellClickedCommand
from commands.mainview.menubuttonclicked import MenuButtonClickedCommand
from commands.mainview.randomshipsbuttonclicked import RandomShipsButtonClickedCommand
from commands.menuview.changetheme import ChangeThemeCommand
from commands.menuview.quitgame import QuitGameCommand
from commands.menuview.startmultiplayer import StartMultiplayerCommand
from commands.menuview.startsingleplayer import StartSingleplayerCommand
from events.eventaggregator import EventAggregator
from models.enums import Command
from services.injector import inject


@inject(EventAggregator)
class CommandFactory:
    def __init__(self, event_aggregator: EventAggregator) -> None:
        self.__event_aggregator = event_aggregator

    def get_command(self, view_name: str, command: Command) -> CommandBase:
        if view_name == "MainView":
            if command == Command.OPEN_MENU:
                return MenuButtonClickedCommand(self.__event_aggregator)
            if command == Command.PLACE_RANDOM_SHIPS:
                return RandomShipsButtonClickedCommand(self.__event_aggregator)
        elif view_name == "Cell":
            if command == Command.CELL_CLICK:
                return CellClickedCommand(self.__event_aggregator)
        elif view_name == "Menu":
            if command == Command.QUIT_GAME:
                return QuitGameCommand(self.__event_aggregator)
            if command == Command.START_SINGLE_PLAYER:
                return StartSingleplayerCommand(self.__event_aggregator)
            if command == Command.START_MULTIPLAYER:
                return StartMultiplayerCommand(self.__event_aggregator)
            if command == Command.CHANGE_THEME:
                return ChangeThemeCommand(self.__event_aggregator)
