import arcade

class Entity(arcade.Sprite):
    def __init__(self, filename, scale, x, y):
        super().__init__(filename, scale)
        self.center_x = x
        self.center_y = y
        self.hp = 0
        self.max_hp = 0
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
        if player.hp < player.max_hp:
            player.hp += self.heal_amount
            if player.hp > player.max_hp: player.hp = player.max_hp
            return True
        return False

# --- НОВЫЙ КЛАСС ---
class CrystalDrop(Item):
    def __init__(self, x, y, amount=5):
        # Используем синий камень
        super().__init__(":resources:images/items/gemBlue.png", x, y)
        self.amount = amount
        # Небольшая анимация пульсации (опционально)
        self.scale_change = 0.01

    def update(self, delta_time: float = 1/60):
        # Простая анимация увеличения/уменьшения
        self.scale += self.scale_change
        if self.scale > 0.6 or self.scale < 0.4:
            self.scale_change *= -1

    def on_pickup(self, player):
        # Логику добавления в БД сделаем в main.py, здесь просто вернем True
        return True