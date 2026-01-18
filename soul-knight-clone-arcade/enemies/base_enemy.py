import arcade
import math
import config
from entities.entity import Entity


class BaseEnemy(Entity):
    def __init__(self, filename, x, y, player_ref):
        super().__init__(filename, config.SPRITE_SCALING, x, y)
        self.player = player_ref
        self.hp = config.ENEMY_HP
        self.speed = config.ENEMY_SPEED
        self.damage = config.ENEMY_DAMAGE
        self.activation_distance = 500  # Радиус, при котором враг начинает преследовать

    def update_with_physics(self, delta_time, wall_list):
        # 1. Проверка расстояния
        # Если игрок слишком далеко, враг стоит на месте
        dist_x = self.player.center_x - self.center_x
        dist_y = self.player.center_y - self.center_y
        distance = math.sqrt(dist_x ** 2 + dist_y ** 2)

        if distance > self.activation_distance:
            return  # Выходим, не двигаясь

        # 2. Вычисляем угол и смещение
        angle = math.atan2(dist_y, dist_x)
        change_x = math.cos(angle) * self.speed
        change_y = math.sin(angle) * self.speed

        # 3. Движение по X с проверкой коллизий
        self.center_x += change_x
        # Проверяем, врезались ли мы в стену
        hit_list_x = arcade.check_for_collision_with_list(self, wall_list)
        if len(hit_list_x) > 0:
            # Если врезались, отменяем движение по X
            self.center_x -= change_x

        # 4. Движение по Y с проверкой коллизий
        self.center_y += change_y
        # Проверяем, врезались ли мы в стену
        hit_list_y = arcade.check_for_collision_with_list(self, wall_list)
        if len(hit_list_y) > 0:
            # Если врезались, отменяем движение по Y
            self.center_y -= change_y

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            self.kill()