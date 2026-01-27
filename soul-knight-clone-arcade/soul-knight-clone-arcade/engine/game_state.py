from enum import Enum

class GameState(Enum):
    MENU = 0
    LOBBY = 1
    PLAYING = 2
    PAUSED = 3
    GAME_OVER = 4
    SKIN_SELECT = 5
    WEAPON_SELECT = 6