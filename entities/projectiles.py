import arcade
import math
import config
from entities.entity import Entity


class Projectile(Entity):
    def __init__(self, start_x, start_y, target_x, target_y, damage=10):
        super().__init__(":resources:images/space_shooter/laserBlue01.png",
                         config.SPRITE_SCALING, start_x, start_y)

        self.damage = damage

        # --- Математика стрельбы ---
        x_diff = target_x - start_x
        y_diff = target_y - start_y
        angle = math.atan2(y_diff, x_diff)

        self.angle = math.degrees(angle)

        self.change_x = math.cos(angle) * config.BULLET_SPEED
        self.change_y = math.sin(angle) * config.BULLET_SPEED

    def update(self, delta_time: float = 1 / 60):
        super().update(delta_time)
