from threading import Thread
from time import sleep
from types import FunctionType


def threaded_sleep(function_object, seconds: float) -> None:
    def run(fo: FunctionType, sec: float):
        sleep(sec)
        fo()

    thread = Thread(target=lambda f=function_object, s=seconds: run(f, s))
    thread.start()
