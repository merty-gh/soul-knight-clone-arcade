import arcade
import math


class Weapon:
    def __init__(self, damage, cooldown):
        self.damage = damage
        self.cooldown = cooldown
        self.timer = 0
        self.can_shoot = True

    def update(self, delta_time):
        self.timer += delta_time
        if self.timer >= self.cooldown:
            self.can_shoot = True


class RangedWeapon(Weapon):
    def __init__(self, damage, cooldown, bullet_image, bullet_speed=12):
        super().__init__(damage, cooldown)
        self.bullet_image = bullet_image
        self.bullet_speed = bullet_speed

    def attack(self, start_x, start_y, target_x, target_y):
        if not self.can_shoot:
            return None

        self.can_shoot = False
        self.timer = 0

        diff_x = target_x - start_x
        diff_y = target_y - start_y
        angle = math.atan2(diff_y, diff_x)

        # Создаем пулю
        bullet = arcade.Sprite(self.bullet_image, 1.0)
        bullet.center_x = start_x
        bullet.center_y = start_y
        bullet.change_x = math.cos(angle) * self.bullet_speed
        bullet.change_y = math.sin(angle) * self.bullet_speed
        bullet.angle = math.degrees(angle)
        bullet.damage = self.damage

        return bullet


class MeleeWeapon(Weapon):
    def __init__(self, damage, cooldown, reach=60):
        super().__init__(damage, cooldown)
        self.reach = reach

    def attack(self, player_sprite, enemy_list):
        if not self.can_shoot:
            return None

        self.can_shoot = False
        self.timer = 0

        hit_enemies = []
        for enemy in enemy_list:
            dist = arcade.get_distance_between_sprites(player_sprite, enemy)
            if dist <= self.reach:
                hit_enemies.append(enemy)

        return hit_enemies


# --- КОНКРЕТНЫЕ ОРУЖИЯ ---

class Blaster(RangedWeapon):
    def __init__(self):
        # Используем ТОЧКУ (маленький метеорит)
        super().__init__(
            damage=5,
            cooldown=0.1,
            bullet_image=":resources:images/space_shooter/meteorGrey_tiny1.png",
            bullet_speed=15
        )


class Sword(MeleeWeapon):
    def __init__(self):
        super().__init__(damage=15, cooldown=0.4, reach=70)