from enum import Enum


class GameState(Enum):
    NONE = 0
    RUNNING = 1
    MENU = 2
    ENDED = 3
