import arcade
import config
from entities.entity import Entity
from weapons.pistol import Pistol


class Player(Entity):
    def __init__(self, x, y):
        super().__init__(":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png",
                         config.SPRITE_SCALING, x, y)
        self.speed = config.PLAYER_SPEED

        # --- Здоровье ---
        self.max_hp = config.PLAYER_MAX_HP
        self.hp = self.max_hp

        # --- Статистика ---
        self.score = 0

        self.weapon = Pistol()

    def update(self, delta_time: float = 1 / 60):
        super().update(delta_time)