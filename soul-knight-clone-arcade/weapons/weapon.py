import time

class Weapon:
    def __init__(self, damage, cooldown):
        self.damage = damage
        self.cooldown = cooldown  # Время в секундах между выстрелами
        self.last_shot_time = 0   # Время последнего выстрела

    def can_shoot(self):
        current_time = time.time()
        if current_time - self.last_shot_time >= self.cooldown:
            return True
        return False

    def shoot(self, start_x, start_y, target_x, target_y):
        raise NotImplementedError