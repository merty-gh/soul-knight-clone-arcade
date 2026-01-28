import arcade
import math
import config


class BaseEnemy(arcade.Sprite):
    def __init__(self, x, y, player, room_rect):
        super().__init__(scale=config.ENEMY_SCALING)
        self.center_x = x
        self.center_y = y
        self.player = player
        self.room_rect = room_rect  # Границы комнаты
        self.hp = config.ENEMY_HP
        self.damage = config.ENEMY_DAMAGE
        self.speed = config.ENEMY_SPEED

    def update_with_physics(self, delta_time, walls):
        # Простое движение к игроку
        diff_x = self.player.center_x - self.center_x
        diff_y = self.player.center_y - self.center_y
        angle = math.atan2(diff_y, diff_x)

        self.change_x = math.cos(angle) * self.speed
        self.change_y = math.sin(angle) * self.speed

        # Обновление позиции
        self.center_x += self.change_x
        self.center_y += self.change_y

        # --- ВАЖНО: ОГРАНИЧЕНИЕ КОМНАТОЙ ---
        # Враг не может выйти за пределы комнаты (с небольшим отступом от стен)
        padding = 32  # Половина тайла
        if self.center_x < self.room_rect.left + padding: self.center_x = self.room_rect.left + padding
        if self.center_x > self.room_rect.right - padding: self.center_x = self.room_rect.right - padding
        if self.center_y < self.room_rect.bottom + padding: self.center_y = self.room_rect.bottom + padding
        if self.center_y > self.room_rect.top - padding: self.center_y = self.room_rect.top - padding

        return None  # Возвращает пулю, если выстрелил

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            self.kill()


# --- КЛАССЫ ВРАГОВ ---

class Zombie(BaseEnemy):
    def __init__(self, x, y, player, room_rect):
        super().__init__(x, y, player, room_rect)
        self.texture = arcade.load_texture(config.ZOMBIE_IMAGE)
        self.hp = config.ZOMBIE_HP
        self.speed = config.ZOMBIE_SPEED
        self.damage = config.ZOMBIE_DAMAGE


class Robot(BaseEnemy):
    def __init__(self, x, y, player, room_rect):
        super().__init__(x, y, player, room_rect)
        self.texture = arcade.load_texture(config.ROBOT_IMAGE)
        self.hp = config.ROBOT_HP
        self.speed = config.ROBOT_SPEED
        self.damage = config.ROBOT_DAMAGE
        self.cooldown = config.ROBOT_COOLDOWN
        self.timer = 0

    def update_with_physics(self, delta_time, walls):
        super().update_with_physics(delta_time, walls)
        self.timer += delta_time
        if self.timer >= self.cooldown:
            # Стрельба робота
            dist = math.dist((self.center_x, self.center_y), (self.player.center_x, self.player.center_y))
            if dist < config.ROBOT_ATTACK_RANGE:
                self.timer = 0
                bullet = arcade.Sprite(":resources:images/space_shooter/laserRed01.png", 1.0)
                bullet.center_x = self.center_x
                bullet.center_y = self.center_y

                diff_x = self.player.center_x - self.center_x
                diff_y = self.player.center_y - self.center_y
                angle = math.atan2(diff_y, diff_x)

                bullet.change_x = math.cos(angle) * 5
                bullet.change_y = math.sin(angle) * 5
                bullet.angle = math.degrees(angle)
                bullet.damage = self.damage
                return bullet  # Возвращаем ОДНУ пулю
        return None


class Slime(BaseEnemy):
    def __init__(self, x, y, player, room_rect):
        super().__init__(x, y, player, room_rect)
        self.texture = arcade.load_texture(config.SLIME_IMAGE)
        self.hp = config.SLIME_HP
        self.speed = config.SLIME_SPEED
        self.damage = config.SLIME_DAMAGE


class Bat(BaseEnemy):
    def __init__(self, x, y, player, room_rect):
        super().__init__(x, y, player, room_rect)
        self.texture = arcade.load_texture(config.BAT_IMAGE)
        self.hp = config.BAT_HP
        self.speed = config.BAT_SPEED
        self.damage = config.BAT_DAMAGE