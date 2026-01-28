import arcade
import math
import config
from .base_enemy import BaseEnemy


class Boss(BaseEnemy):
    def __init__(self, x, y, player, room_rect):
        # Босс большой и медленный
        super().__init__(x, y, player, room_rect)
        self.texture = arcade.load_texture("boss.webp")
        self.scale = 0.2  # Большой размер
        self.hp = 500  # Много жизней
        self.speed = 1.5
        self.damage = 25

        # Стрельба
        self.bullet_cooldown = 0.8
        self.bullet_timer = 0
        self.burst_count = 0  # Для стрельбы очередями

    def update(self, delta_time, walls):
        super().update(delta_time, walls)

        # Логика стрельбы (Стреляет веером)
        self.bullet_timer += delta_time
        if self.bullet_timer >= self.bullet_cooldown:
            self.bullet_timer = 0
            return self.shoot_spread()
        return None

    def shoot_spread(self):
        # Стреляет 5 пулями веером
        bullets = []
        start_x = self.center_x
        start_y = self.center_y
        dest_x = self.player.center_x
        dest_y = self.player.center_y

        angle_rad = math.atan2(dest_y - start_y, dest_x - start_x)

        # Углы разлета: -20, -10, 0, +10, +20 градусов
        offsets = [-0.3, -0.15, 0, 0.15, 0.3]

        for offset in offsets:
            bullet = arcade.Sprite(":resources:images/space_shooter/laserRed01.png", 0.8)
            bullet.center_x = start_x
            bullet.center_y = start_y
            bullet.angle = math.degrees(angle_rad + offset)
            bullet.change_x = math.cos(angle_rad + offset) * 5
            bullet.change_y = math.sin(angle_rad + offset) * 5
            bullet.damage = self.damage
            bullets.append(bullet)

        return bullets