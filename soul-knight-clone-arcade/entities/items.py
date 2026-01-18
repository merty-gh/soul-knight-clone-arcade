import arcade
import config
from entities.entity import Entity


class Item(Entity):
    def __init__(self, filename, x, y):
        super().__init__(filename, config.SPRITE_SCALING, x, y)

    def on_pickup(self, player):
        """Переопределяется в наследниках"""
        return False


class HealthPotion(Item):
    def __init__(self, x, y):
        super().__init__(":resources:images/items/gemRed.png", x, y)
        self.heal_amount = 20

    def on_pickup(self, player):
        if player.hp < player.max_hp:
            player.hp += self.heal_amount
            if player.hp > player.max_hp:
                player.hp = player.max_hp
            return True
        return False


class CrystalDrop(Item):
    def __init__(self, x, y, amount=5):
        super().__init__(":resources:images/items/gemBlue.png", x, y)
        self.amount = amount
        self.scale_change = 0.01

    def update(self, delta_time: float = 1 / 60):
        super().update(delta_time)

        # --- ИСПРАВЛЕНИЕ ДЛЯ ARCADE 3.0 ---
        # scale теперь кортеж (x, y). Берем текущее значение X.
        current_scale = self.scale[0]
        new_scale = current_scale + self.scale_change

        # Присваиваем новое значение (сеттер Arcade сам превратит число в кортеж)
        self.scale = new_scale

        if new_scale > 0.6 or new_scale < 0.4:
            self.scale_change *= -1

    def on_pickup(self, player):
        return True