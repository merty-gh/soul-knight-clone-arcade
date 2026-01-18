import arcade

# --- Настройки окна ---
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
SCREEN_TITLE = "Soul Knight Clone (Arcade)"

# --- Настройки игры ---
SPRITE_SCALING = 0.5
TILE_SCALING = 0.5
PLAYER_SPEED = 3.5
PLAYER_MAX_HP = 100
BULLET_SPEED = 12

# --- Настройки уровня ---
ROOM_WIDTH_PX = 1024
ROOM_HEIGHT_PX = 768

# --- Настройки врагов ---
ENEMY_SPEED = 2
ENEMY_HP = 30
ENEMY_DAMAGE = 10

# --- Цвета ---
BG_COLOR = arcade.color.BLACK

# --- Настройки UI ---
UI_FONT_SIZE = 20
UI_BAR_WIDTH = 200
UI_BAR_HEIGHT = 20
UI_HEALTH_COLOR = arcade.color.RED
UI_BG_COLOR = arcade.color.DARK_GRAY

# --- Пути ---
ASSET_PATH = "assets/"

# --- СПИСОК СКИНОВ ---
SKINS_CONFIG = [
    {
        "name": "Adventurer",
        "price": 0,
        "image": ":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png"
    },
    {
        "name": "Knight",
        "price": 50,
        "image": ":resources:images/animated_characters/male_person/malePerson_idle.png"
    },
    {
        "name": "Robot",
        "price": 100,
        "image": ":resources:images/animated_characters/robot/robot_idle.png"
    },
    {
        "name": "Zombie",
        "price": 200,
        "image": ":resources:images/animated_characters/zombie/zombie_idle.png"
    }
]

# --- СПИСОК ОРУЖИЯ ---
WEAPONS_CONFIG = [
    {
        "name": "Pistol",
        "price": 0,
        "class_name": "Pistol",
        "image": ":resources:images/space_shooter/laserBlue01.png"
    },
    {
        "name": "Blaster",
        "price": 50,
        "class_name": "Blaster",
        "image": ":resources:images/space_shooter/laserRed01.png"
    }
]