from commands.commandbase import CommandBase
from events.eventaggregator import EventAggregator
from models.enums import Event


class ChangeThemeCommand(CommandBase):
    def __init__(self, event_aggregator: EventAggregator) -> None:
        self.__event_aggregator = event_aggregator

    def execute(self, theme: str):
        self.__event_aggregator.publish(
            Event.THEME_CHANGE_REQUESTED, theme
        )
