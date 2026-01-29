import arcade
import config
from entities.entity import Entity

class Wall(Entity):
    def __init__(self, x, y):
        # Кирпичная стена
        super().__init__(":resources:images/tiles/brickBrown.png", config.TILE_SCALING, x, y)

class Floor(Entity):
    def __init__(self, x, y):
        # Темный пол
        super().__init__(":resources:images/tiles/stoneCenter.png", config.TILE_SCALING, x, y)
        self.color = (50, 60, 80)

class DoorBlocker(Entity):
    def __init__(self, x, y):
        # Дверь/Барьер
        super().__init__(":resources:images/tiles/lockYellow.png", config.TILE_SCALING, x, y)
        # Запоминаем, где должна стоять дверь
        self.initial_x = x
        self.initial_y = y