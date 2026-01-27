import time
from weapons.weapons import Weapon
from entities.projectiles import Projectile

class Pistol(Weapon):
    def __init__(self):
        # Урон 10, перезарядка 0.3 секунды
        super().__init__(damage=10, cooldown=0.3)

    def shoot(self, start_x, start_y, target_x, target_y):
        if self.can_shoot():
            self.last_shot_time = time.time()
            # Создаем и возвращаем пулю
            return Projectile(start_x, start_y, target_x, target_y, self.damage)
        return None