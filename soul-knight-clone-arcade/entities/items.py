import arcade
import config
from entities.entity import Entity

class Item(Entity):
    def __init__(self, filename, x, y):
        super().__init__(filename, config.SPRITE_SCALING, x, y)

    def on_pickup(self, player):
        pass

class HealthPotion(Item):
    def __init__(self, x, y):
        super().__init__(":resources:images/items/gemRed.png", x, y)
        self.heal_amount = 20

    def on_pickup(self, player):
        # Лечим игрока
        if player.hp < player.max_hp:
            player.hp += self.heal_amount
            if player.hp > player.max_hp:
                player.hp = player.max_hp
            return True # Предмет использован
        return False # Предмет не нужен (полное HP)