# TkBattleship
A simple GUI Battleship game written in Python using tkinter

Copyright 2023 Jann Emken

## Description
The game is a work-in-progress.

### Download
Go to [Releases](https://github.com/q-g-j/TkBattleship/releases)

### Features
- Singleplayer against the computer
- Support for tkinter.ttk themes - with instant switching in the game menu
  (in Windows use one of the "native" themes like "vista" or "winnative" if the UI gets very slow. The other themes should work well in Linux and macOS)

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
This is a practice project to implement the MVC pattern in a TKinter application while following some OOP related principles to get a better understanding of these.

It uses the event aggregator pattern for state change notifications between the models, the views and the controller.</br>
Both the event handlers and the commands have been put in their own modules and are retrieved through factory methods to keep the other components as clean as possible.</br>
The views make use of the command pattern for their button commands similar to the ICommand interface from WPF.

A REST API multiplayer mode using Flask is in development. Currently only a the single player mode is done.

I have added an own dependency injection service which allows for registering classes and resolving them via constructor injection.</br>
Types may be registered as singletons or transients objects while it is also possible to register existing instances. When a type is resolved, the service goes through all its dependencies recursively and determines for each wether it is registered as a singleton or as a transient object.

#### Dependency Injection usage example:
***Controller:***
```python
class GameController:
    def __init__(self, root: ThemedTk) -> None:
        self.__root = root
        self.__injector = DependencyInjector()
        self.__register_services()
    
    def __register_services(self) -> None:
        self.__injector.register_instance(self.__root)
        self.__injector.add_singleton(MainView)
        self.__injector.add_singleton(EventAggregator)
        self.__injector.add_transient(CommandFactory)
        self.__injector.add_transient(SettingsReader)
```

***Main view:***
```python
@inject(ThemedTk, EventAggregator, CommandFactory, SettingsReader)
class MainView(ViewBase):
    def __init__(
        self,
        root: ThemedTk,
        event_aggregator: EventAggregator,
        command_factory: CommandFactory,
        settings_reader: SettingsReader,
    ) -> None:
        super().__init__(root, command_factory, style=StyleDefinitions.MAIN_VIEW_FRAME, padding=20)
        self.__root = root
        self.__event_aggregator = event_aggregator
        self.__command_factory = command_factory
        self.__settings_reader = settings_reader
```
