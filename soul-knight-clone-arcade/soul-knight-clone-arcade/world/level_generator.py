import random
import arcade
import config
from world.tiles import Wall, Floor, DoorBlocker
from entities.items import Chest


class LevelGenerator:
    def __init__(self):
        self.wall_list = arcade.SpriteList()
        self.floor_list = arcade.SpriteList()
        self.door_list = arcade.SpriteList()
        self.item_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.rooms_data = {}

    def generate_level(self, player):
        # 1. ПЛАНИРОВАНИЕ
        existing_rooms = set()
        for x in range(-1, 2):
            for y in range(-1, 2):
                if x == 0 and y == 0:
                    existing_rooms.add((0, 0))
                else:
                    existing_rooms.add((x, y))

        # 2. СТРОИТЕЛЬСТВО
        for (gx, gy) in existing_rooms:
            is_start = (gx == 0 and gy == 0)

            has_top = (gx, gy + 1) in existing_rooms
            has_bottom = (gx, gy - 1) in existing_rooms
            has_left = (gx - 1, gy) in existing_rooms
            has_right = (gx + 1, gy) in existing_rooms

            self.create_room(gx, gy, is_start, has_top, has_bottom, has_left, has_right)

    def create_room(self, gx, gy, is_start, has_top, has_bottom, has_left, has_right):
        room_x = gx * config.ROOM_WIDTH_PX
        room_y = gy * config.ROOM_HEIGHT_PX

        # Пол
        temp_wall = Wall(0, 0)
        grid = int(temp_wall.width)
        for x in range(room_x, room_x + config.ROOM_WIDTH_PX, grid):
            for y in range(room_y, room_y + config.ROOM_HEIGHT_PX, grid):
                self.floor_list.append(Floor(x, y))

        # Стены и двери
        doors_objects = []
        mid_x = room_x + config.ROOM_WIDTH_PX // 2
        mid_y = room_y + config.ROOM_HEIGHT_PX // 2

        # Границы
        for x in range(room_x, room_x + config.ROOM_WIDTH_PX, grid):
            # НИЗ
            if has_bottom and abs(x - mid_x) < grid * 2:
                d = DoorBlocker(x, room_y)
                doors_objects.append(d)
                self.door_list.append(d)
            else:
                self.wall_list.append(Wall(x, room_y))
            # ВЕРХ
            top_y = room_y + config.ROOM_HEIGHT_PX - grid
            if has_top and abs(x - mid_x) < grid * 2:
                d = DoorBlocker(x, top_y)
                doors_objects.append(d)
                self.door_list.append(d)
            else:
                self.wall_list.append(Wall(x, top_y))

        for y in range(room_y, room_y + config.ROOM_HEIGHT_PX, grid):
            # ЛЕВО
            if has_left and abs(y - mid_y) < grid * 2:
                d = DoorBlocker(room_x, y)
                doors_objects.append(d)
                self.door_list.append(d)
            else:
                self.wall_list.append(Wall(room_x, y))
            # ПРАВО
            right_x = room_x + config.ROOM_WIDTH_PX - grid
            if has_right and abs(y - mid_y) < grid * 2:
                d = DoorBlocker(right_x, y)
                doors_objects.append(d)
                self.door_list.append(d)
            else:
                self.wall_list.append(Wall(right_x, y))

        # Данные комнаты
        distance = abs(gx) + abs(gy)
        max_waves = 1
        if distance > 0: max_waves = 2
        if distance > 2: max_waves = 3
        if is_start: max_waves = 0

        self.rooms_data[(gx, gy)] = {
            'doors': doors_objects,
            'current_wave': 0,
            'max_waves': max_waves,
            'cleared': (max_waves == 0),
            'spawned_enemies': []
        }

        # --- СПАВН СУНДУКОВ (ИСПРАВЛЕНО) ---
        # Если это не стартовая комната - гарантированно спавним 2 сундука
        if not is_start:
            # Спавним ровно 2 раза
            for i in range(2):
                cx = room_x + config.ROOM_WIDTH_PX // 2
                cy = room_y + config.ROOM_HEIGHT_PX // 2

                # Добавляем случайное смещение, чтобы сундуки не стояли друг в друге
                # Смещение от -100 до 100 пикселей от центра
                offset_x = random.randint(-100, 100)
                offset_y = random.randint(-100, 100)

                chest = Chest(cx + offset_x, cy + offset_y)
                self.item_list.append(chest)
                self.wall_list.append(chest)  # Сундук твердый