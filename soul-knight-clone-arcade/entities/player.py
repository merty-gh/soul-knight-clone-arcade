import arcade
import config
import database
from entities.entity import Entity
from weapons.pistol import Pistol


# --- ОПРЕДЕЛЯЕМ НОВЫЕ ОРУЖИЯ ЗДЕСЬ (или в отдельных файлах) ---
class Blaster(Pistol):
    def __init__(self):
        super().__init__()
        self.damage = 25  # Больше урона
        self.cooldown = 0.2  # Быстрее стрельба
        self.bullet_speed = 15  # Быстрее пуля

    def shoot(self, start_x, start_y, target_x, target_y):
        # Используем стандартный метод, но меняем картинку пули
        bullet = super().shoot(start_x, start_y, target_x, target_y)
        if bullet:
            # Меняем текстуру пули на красную
            bullet.texture = arcade.load_texture(":resources:images/space_shooter/laserRed01.png")
        return bullet


# -------------------------------------------------------------

class Player(Entity):
    def __init__(self, x, y):
        # 1. Скин
        default_skin_path = config.SKINS_CONFIG[0]["image"]

        super().__init__(default_skin_path, config.SPRITE_SCALING, x, y)

        # 3. Характеристики
        self.speed = config.PLAYER_SPEED
        self.max_hp = config.PLAYER_MAX_HP
        self.hp = self.max_hp

        # 4. БД и Оружие
        self.crystals = database.get_crystals()
        self.score = 0
        self.weapon = Pistol()  # Стартовое оружие

        self.current_skin_name = config.SKINS_CONFIG[0]["name"]

    def update_crystals_from_db(self):
        self.crystals = database.get_crystals()

    def equip_skin(self, skin_name):
        for skin_data in config.SKINS_CONFIG:
            if skin_data["name"] == skin_name:
                self.texture = arcade.load_texture(skin_data["image"])
                self.current_skin_name = skin_name
                break

    def equip_weapon_by_name(self, class_name):
        print(f"Equipping weapon: {class_name}")
        if class_name == "Pistol":
            self.weapon = Pistol()
        elif class_name == "Blaster":
            self.weapon = Blaster()
        else:
            print(f"Unknown weapon class: {class_name}")

    def update(self, delta_time: float = 1 / 60):
        super().update(delta_time)