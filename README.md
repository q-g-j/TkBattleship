# TkBattleship
A simple GUI Battleship game written in Python using tkinter

Copyright 2023 Jann Emken

## Description
The game is a work-in-progress.

### Gameplay
After starting a new game (currently only singleplayer) the player has to place his / her ships:

| Ship       | Length  | Number |
|------------|---------|--------|
| Destroyer  | 2 cells | 2      |
| Submarine  | 3 cells | 2      |
| Cruiser    | 3 cells | 1      |
| Battleship | 4 cells | 1      |
| Carrier    | 5 cells | 1      |

The ships have to be placed with at least 1 cell between them.</br>
There is a button to let the computer place all ships randomly.

Players now take turns in trying to hit and destroy the opponent's ships.</br>
The computer opponent has been improved and should be stronger now.

### Requirements
Python 3 (tested with 3.10)

#### Libraries (install via pip):
- Pillow >= 10.0.0
- appdirs >= 1.4.4

### Technical details

This is a practice project to implement the MVC pattern in a TKinter application while following some OOP related principles. It uses the event aggregator pattern for state change notifications between the models, the views and the controller.

I added a dependency injection service which allows for registering class instances and resolve them via constructor injection.

#### DI usage:
**Controller:**
```py
self.__injector.register("root", self.__root)

event_aggregator = self.__injector.resolve(EventAggregator)
self.__injector.register("event_aggregator", event_aggregator)

command_factory = self.__injector.resolve(CommandFactory)
self.__injector.register("command_factory", command_factory)

# All dependencies are resolved automatically, there is no need to specify them during registration:
main_view = self.__injector.resolve(MainView)
self.__injector.register("main_view", main_view)
```

**Main view:**
```py
@inject("root", "event_aggregator", "command_factory")
class MainView(ViewBase):
    def __init__(
        self,
        root: Tk,
        event_aggregator: EventAggregator,
        command_factory: CommandFactory,
    )
```


The views make use of the command pattern for their button commands similar to the ICommand interface from WPF.

Both the event handlers and the commands have been put in their own modules and are retrieved through factory methods to keep the other components as clean as possible.

A REST API multiplayer mode using Flask is in development. Currently only a simple single player mode is done.
