import arcade
import math
import random
import config
from entities.entity import Entity


# ВАЖНО: Здесь НЕ ДОЛЖНО БЫТЬ строки "from enemies.base_enemy import ..."

class BaseEnemy(Entity):
    def __init__(self, filename, x, y, player_ref):
        super().__init__(filename, config.ENEMY_SCALING, x, y)
        self.player = player_ref
        self.hp = 10
        self.speed = 0
        self.damage = 0
        self.change_x = 0.0
        self.change_y = 0.0

    def update_with_physics(self, delta_time, wall_list):
        pass

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            self.kill()


# --- 1. ЗОМБИ ---
class Zombie(BaseEnemy):
    def __init__(self, x, y, player_ref):
        super().__init__(config.ZOMBIE_IMAGE, x, y, player_ref)
        self.hp = config.ZOMBIE_HP
        self.speed = config.ZOMBIE_SPEED
        self.damage = config.ZOMBIE_DAMAGE
        self.color = (150, 255, 150)

    def update_with_physics(self, delta_time, wall_list):
        dist_x = self.player.center_x - self.center_x
        dist_y = self.player.center_y - self.center_y
        angle = math.atan2(dist_y, dist_x)

        self.change_x = math.cos(angle) * self.speed
        self.change_y = math.sin(angle) * self.speed

        self.center_x += self.change_x
        if arcade.check_for_collision_with_list(self, wall_list):
            self.center_x -= self.change_x
        self.center_y += self.change_y
        if arcade.check_for_collision_with_list(self, wall_list):
            self.center_y -= self.change_y
        return None


# --- 2. РОБОТ ---
class Robot(BaseEnemy):
    def __init__(self, x, y, player_ref):
        super().__init__(config.ROBOT_IMAGE, x, y, player_ref)
        self.hp = config.ROBOT_HP
        self.speed = config.ROBOT_SPEED
        self.damage = config.ROBOT_DAMAGE
        self.cooldown_timer = random.uniform(0, 1.0)
        self.color = (255, 100, 100)

    def update_with_physics(self, delta_time, wall_list):
        dist_x = self.player.center_x - self.center_x
        dist_y = self.player.center_y - self.center_y
        distance = math.sqrt(dist_x ** 2 + dist_y ** 2)
        angle = math.atan2(dist_y, dist_x)

        if distance > config.ROBOT_ATTACK_RANGE:
            self.change_x = math.cos(angle) * self.speed
            self.change_y = math.sin(angle) * self.speed
        else:
            self.change_x = 0
            self.change_y = 0

        self.center_x += self.change_x
        if arcade.check_for_collision_with_list(self, wall_list):
            self.center_x -= self.change_x
        self.center_y += self.change_y
        if arcade.check_for_collision_with_list(self, wall_list):
            self.center_y -= self.change_y

        self.cooldown_timer -= delta_time
        if self.cooldown_timer <= 0:
            self.cooldown_timer = config.ROBOT_COOLDOWN
            return self.shoot(angle)
        return None

    def shoot(self, angle):
        bullet = arcade.Sprite(":resources:images/space_shooter/laserRed01.png", 0.8)
        bullet.center_x = self.center_x
        bullet.center_y = self.center_y
        speed = 7
        bullet.change_x = math.cos(angle) * speed
        bullet.change_y = math.sin(angle) * speed
        bullet.angle = math.degrees(angle)
        return bullet


# --- 3. СЛИЗЕНЬ ---
class Slime(BaseEnemy):
    def __init__(self, x, y, player_ref):
        super().__init__(config.SLIME_IMAGE, x, y, player_ref)
        self.scale = 0.8
        self.hp = config.SLIME_HP
        self.speed = config.SLIME_SPEED
        self.damage = config.SLIME_DAMAGE

    def update_with_physics(self, delta_time, wall_list):
        dist_x = self.player.center_x - self.center_x
        dist_y = self.player.center_y - self.center_y
        angle = math.atan2(dist_y, dist_x)

        self.change_x = math.cos(angle) * self.speed
        self.change_y = math.sin(angle) * self.speed

        self.center_x += self.change_x
        if arcade.check_for_collision_with_list(self, wall_list):
            self.center_x -= self.change_x
        self.center_y += self.change_y
        if arcade.check_for_collision_with_list(self, wall_list):
            self.center_y -= self.change_y
        return None


# --- 4. ЛЕТУЧАЯ МЫШЬ ---
class Bat(BaseEnemy):
    def __init__(self, x, y, player_ref):
        super().__init__(config.BAT_IMAGE, x, y, player_ref)
        self.hp = config.BAT_HP
        self.speed = config.BAT_SPEED
        self.damage = config.BAT_DAMAGE
        self.wobble_timer = 0

    def update_with_physics(self, delta_time, wall_list):
        dist_x = self.player.center_x - self.center_x
        dist_y = self.player.center_y - self.center_y
        base_angle = math.atan2(dist_y, dist_x)

        self.wobble_timer += delta_time * 10
        wobble_offset = math.sin(self.wobble_timer) * 1.5

        final_angle = base_angle + wobble_offset

        self.change_x = math.cos(final_angle) * self.speed
        self.change_y = math.sin(final_angle) * self.speed

        self.center_x += self.change_x
        if arcade.check_for_collision_with_list(self, wall_list):
            self.center_x -= self.change_x
        self.center_y += self.change_y
        if arcade.check_for_collision_with_list(self, wall_list):
            self.center_y -= self.change_y

        return None