from commands.commandbase import CommandBase
from events.eventaggregator import EventAggregator
from models.enums import Event, Side


class CellClickedCommand(CommandBase):
    def __init__(self, event_aggregator: EventAggregator) -> None:
        self.__event_aggregator = event_aggregator

    def execute(self, player_type: Side, row: int, column: int) -> None:
        self.__event_aggregator.publish(Event.CELL_CLICKED, player_type, row, column)
