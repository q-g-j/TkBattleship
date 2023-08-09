from commands.commandbase import CommandBase
from events.eventaggregator import EventAggregator
from models.enums import Event


class StartMultiplayerCommand(CommandBase):
    def __init__(self, event_aggregator: EventAggregator) -> None:
        self.__event_aggregator = event_aggregator

    def execute(self):
        self.__event_aggregator.publish(Event.MULTIPLAYER_CLICKED)
