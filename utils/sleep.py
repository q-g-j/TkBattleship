from threading import Thread
from time import sleep
from types import FunctionType


def threaded_sleep(function_object, seconds: float) -> None:
    def run(_function_object: FunctionType, sec: float):
        sleep(sec)
        _function_object()

    thread = Thread(target=lambda f=function_object, s=seconds: run(f, s), daemon=True)
    thread.start()
