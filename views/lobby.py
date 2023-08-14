from factories.commandfactory import CommandFactory
from services.injector import inject
from views.viewbase import ViewBase


@inject(CommandFactory)
class Lobby(ViewBase):
    def __init__(self, parent, command_factory: CommandFactory, **kwargs) -> None:
        super().__init__(parent, command_factory, **kwargs)
