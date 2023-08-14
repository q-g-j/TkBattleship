# TkBattleship
A simple GUI Battleship game written in Python using tkinter

Copyright 2023 Jann Emken

## Description
The game is a work-in-progress.

### Download
Go to [Releases](https://github.com/q-g-j/TkBattleship/releases)

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

#### External modules (install via pip):
- Pillow >= 10.0.0
- appdirs >= 1.4.4
- pyglet == 1.5.27
- ttkthemes >= 3.2.2

#### External resources:
Fonts:
- [Microsoft Selawik](https://github.com/microsoft/Selawik) (License: OFL-1.1)

### Technical details

This is a practice project to implement the MVC pattern in a TKinter application while following some OOP related principles. It uses the event aggregator pattern for state change notifications between the models, the views and the controller.

I have added a dependency injection service which allows for registering class instances and resolving them via constructor injection.

#### Dependency Injection usage example:
**Controller:**
```py
def __init__(self, root: Tk) -> None:
    self.__root = root
    self.__injector = DependencyInjector()

    self.__injector.register_instance(self.__root)
    self.__injector.add_singleton(EventAggregator)
    self.__injector.add_singleton(CommandFactory)
```

**Main view:**
```py
@inject(Tk, EventAggregator, CommandFactory)
class MainView(ViewBase):
    def __init__(
        self,
        root: Tk,
        event_aggregator: EventAggregator,
        command_factory: CommandFactory,
    ) -> None:
```


The views make use of the command pattern for their button commands similar to the ICommand interface from WPF.

Both the event handlers and the commands have been put in their own modules and are retrieved through factory methods to keep the other components as clean as possible.

A REST API multiplayer mode using Flask is in development. Currently only a simple single player mode is done.
