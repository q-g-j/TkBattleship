from commands.commandbase import CommandBase
from events.eventaggregator import EventAggregator
from models.enums import Event, Side
from models.position import Position


class CellClickedCommand(CommandBase):
    def __init__(self, event_aggregator: EventAggregator) -> None:
        self.__event_aggregator = event_aggregator

    def execute(self, player_type: Side, pos: Position) -> None:
        self.__event_aggregator.publish(Event.CELL_CLICKED, player_type, pos)
