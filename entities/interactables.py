import arcade
import config

class Interactable(arcade.Sprite):
    def __init__(self, filename, x, y, scale=1.0):
        super().__init__(filename, scale, center_x=x, center_y=y)
        self.text = "" # Текст, который появляется при подходе

    def on_interact(self, player, game_window):
        """Что происходит при нажатии E"""
        pass

class Portal(Interactable):
    def __init__(self, x, y):
        # Выглядит как синий портал (лестница или спираль)
        super().__init__(":resources:images/tiles/signExit.png", x, y, config.TILE_SCALING)
        self.text = "Press [E] to Start Run"

    def on_interact(self, player, game_window):
        # Запуск генерации подземелья
        game_window.start_dungeon_run()

class SkinChanger(Interactable):
    def __init__(self, x, y):
        # Выглядит как табличка
        super().__init__(":resources:images/tiles/signRight.png", x, y, config.TILE_SCALING)
        self.text = "Press [E] to Change Skin"

    def on_interact(self, player, game_window):
        player.change_skin()

class WeaponShopItem(Interactable):
    def __init__(self, x, y, weapon_class, price, sprite_path):
        super().__init__(sprite_path, x, y, 0.8) # Чуть меньше масштаб
        self.weapon_class = weapon_class
        self.price = price
        self.text = f"[E] Buy {price} Crystals"

    def on_interact(self, player, game_window):
        if player.crystals >= self.price:
            player.crystals -= self.price
            player.weapon = self.weapon_class() # Даем новое оружие
            print(f"Bought weapon for {self.price}")
            # Можно добавить звук покупки
        else:
            print("Not enough crystals!")