from events.eventhandlers.eventhandlerbase import EventHandlerBase
from views.mainview import MainView


class StatusLabelEventHandler(EventHandlerBase):
    def __init__(
            self,
            main_view: MainView,
    ) -> None:
        self.__main_view = main_view

    def execute(self, text: str):
        self.__main_view.set_status_label_text(text)
