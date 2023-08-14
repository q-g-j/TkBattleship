from events.eventhandlers.eventhandlerbase import EventHandlerBase
from views.mainview import MainView


class StatusLabelTextSentEventHandler(EventHandlerBase):
    def __init__(
        self,
        main_view: MainView,
    ) -> None:
        self.__main_view = main_view

    def execute(self, text: str) -> None:
        self.__main_view.set_status_label_text(text)
