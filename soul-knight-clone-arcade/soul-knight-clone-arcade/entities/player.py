import arcade
import math
import config
import database
from entities.entity import Entity
from weapons.weapons import Pistol, Blaster, Sword


class Player(Entity):
    def __init__(self, x, y):
        default_skin_path = config.SKINS_CONFIG[0]["image"]
        super().__init__(default_skin_path, config.SPRITE_SCALING, x, y)

        self.speed = config.PLAYER_SPEED
        self.max_hp = config.PLAYER_MAX_HP
        self.hp = self.max_hp
        self.armor = 0

        self.crystals = database.get_crystals()
        self.score = 0

        # ИЗМЕНЕНИЕ: Масштаб меча 0.05 (подберите под размер вашей картинки)
        self.weapon_sprite = arcade.Sprite(scale=0.03)
        self.weapon_list = arcade.SpriteList()
        self.weapon_list.append(self.weapon_sprite)

        self.mouse_angle = 0

        self.weapon = Sword()
        self.equip_weapon_visuals("Sword")

        self.current_skin_name = config.SKINS_CONFIG[0]["name"]

        # Направление взгляда (False = вправо, True = влево)
        self.facing_left = False

    def update_crystals_from_db(self):
        self.crystals = database.get_crystals()

    def equip_skin(self, skin_name):
        for skin_data in config.SKINS_CONFIG:
            if skin_data["name"] == skin_name:
                self.texture = arcade.load_texture(skin_data["image"])
                self.current_skin_name = skin_name
                break

    def equip_weapon_visuals(self, weapon_name):
        for w_data in config.WEAPONS_CONFIG:
            if w_data["class_name"] == weapon_name:
                # Загружаем текстуру. mech.png должен быть рядом с main.py
                self.weapon_sprite.texture = arcade.load_texture(w_data["image"])
                return

    def equip_weapon_by_name(self, class_name):
        if class_name == "Pistol":
            self.weapon = Pistol()
        elif class_name == "Blaster":
            self.weapon = Blaster()
        elif class_name == "Sword":
            self.weapon = Sword()

        self.equip_weapon_visuals(class_name)

    def take_damage(self, amount):
        if self.armor > 0:
            if self.armor >= amount:
                self.armor -= amount
                return
            else:
                amount -= self.armor
                self.armor = 0
        self.hp -= amount

    def update(self, delta_time: float = 1 / 60):
        if hasattr(self.weapon, 'update'):
            self.weapon.update(delta_time)

        # Определяем, куда смотрит игрок
        if self.change_x < 0:
            self.facing_left = True
        elif self.change_x > 0:
            self.facing_left = False

        distance = 20

        # Базовый размер меча. Если картинка большая, ставьте 0.03 или 0.05
        base_scale = 0.05

        if self.facing_left:
            # Смотрим влево
            self.weapon_sprite.center_x = self.center_x - distance
            self.weapon_sprite.scale_x = base_scale
            self.weapon_sprite.scale_y = base_scale
        else:
            # Смотрим вправо (отзеркаливаем по X)
            self.weapon_sprite.center_x = self.center_x + distance
            self.weapon_sprite.scale_x = -base_scale
            self.weapon_sprite.scale_y = base_scale

        # Чуть ниже центра игрока
        self.weapon_sprite.center_y = self.center_y - 10
        self.weapon_sprite.angle = 0

        super().update(delta_time)