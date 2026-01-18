import arcade
import config
import database
from entities.entity import Entity
from weapons.pistol import Pistol


class Player(Entity):
    def __init__(self, x, y):
        # Загружаем скин по умолчанию (первый в списке)
        default_skin = config.SKINS_CONFIG[0]["image"]
        super().__init__(default_skin, config.SPRITE_SCALING, x, y)

        self.speed = config.PLAYER_SPEED
        self.max_hp = config.PLAYER_MAX_HP
        self.hp = self.max_hp

        # Данные из базы
        self.crystals = database.get_crystals()
        self.score = 0
        self.weapon = Pistol()

        # Текущий скин (индекс)
        self.current_skin_name = config.SKINS_CONFIG[0]["name"]

    def update_crystals_from_db(self):
        """Обновить локальное значение кристаллов из базы"""
        self.crystals = database.get_crystals()

    def equip_skin(self, skin_name):
        """Смена внешнего вида"""
        for skin_data in config.SKINS_CONFIG:
            if skin_data["name"] == skin_name:
                self.texture = arcade.load_texture(skin_data["image"])
                self.current_skin_name = skin_name
                break