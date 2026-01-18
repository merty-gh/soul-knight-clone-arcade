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
        self.activation_distance = 500

        # --- ВЫЧИСЛЯЕМ ГРАНИЦЫ КОМНАТЫ ---
        # Определяем, в какой клетке родился враг
        gx = int(x // config.ROOM_WIDTH_PX)
        gy = int(y // config.ROOM_HEIGHT_PX)

        # Устанавливаем границы (min_x, max_x, min_y, max_y)
        # Добавляем отступ (grid_size), чтобы не застревали в стенах
        self.min_x = gx * config.ROOM_WIDTH_PX + 64
        self.max_x = (gx + 1) * config.ROOM_WIDTH_PX - 64
        self.min_y = gy * config.ROOM_HEIGHT_PX + 64
        self.max_y = (gy + 1) * config.ROOM_HEIGHT_PX - 64

    def update_with_physics(self, delta_time, wall_list):
        dist_x = self.player.center_x - self.center_x
        dist_y = self.player.center_y - self.center_y
        distance = math.sqrt(dist_x ** 2 + dist_y ** 2)

        if distance > self.activation_distance:
            return

        angle = math.atan2(dist_y, dist_x)
        change_x = math.cos(angle) * self.speed
        change_y = math.sin(angle) * self.speed

        # --- Движение по X ---
        new_x = self.center_x + change_x
        # Проверяем ГРАНИЦЫ КОМНАТЫ
        if self.min_x < new_x < self.max_x:
            self.center_x = new_x
            # Проверяем СТЕНЫ
            hit_list = arcade.check_for_collision_with_list(self, wall_list)
            if hit_list:
                self.center_x -= change_x

        # --- Движение по Y ---
        new_y = self.center_y + change_y
        # Проверяем ГРАНИЦЫ КОМНАТЫ
        if self.min_y < new_y < self.max_y:
            self.center_y = new_y
            # Проверяем СТЕНЫ
            hit_list = arcade.check_for_collision_with_list(self, wall_list)
            if hit_list:
                self.center_y -= change_y

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            self.kill()