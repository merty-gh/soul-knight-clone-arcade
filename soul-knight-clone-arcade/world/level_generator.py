import random
import arcade
import config
from world.tiles import Wall, Floor, DoorBlocker


class LevelGenerator:
    def __init__(self):
        self.wall_list = arcade.SpriteList()
        self.floor_list = arcade.SpriteList()
        self.door_list = arcade.SpriteList()
        self.item_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.rooms_data = {}

    def generate_level(self, player):
        # 1. ПЛАНИРОВАНИЕ: Определяем, какие комнаты существуют
        # Создаем сетку 3x3 (от -1 до 1)
        existing_rooms = set()
        for x in range(-1, 2):
            for y in range(-1, 2):
                if x == 0 and y == 0:
                    existing_rooms.add((0, 0))  # Старт всегда есть
                else:
                    # Можно добавить шанс появления, чтобы карта была разной
                    # if random.random() > 0.3:
                    existing_rooms.add((x, y))

        # 2. СТРОИТЕЛЬСТВО: Генерируем каждую комнату с учетом соседей
        for (gx, gy) in existing_rooms:
            is_start = (gx == 0 and gy == 0)

            # Проверяем соседей (чтобы понять, нужны ли двери)
            has_top = (gx, gy + 1) in existing_rooms
            has_bottom = (gx, gy - 1) in existing_rooms
            has_left = (gx - 1, gy) in existing_rooms
            has_right = (gx + 1, gy) in existing_rooms

            self.create_room(gx, gy, is_start, has_top, has_bottom, has_left, has_right)

    def create_room(self, gx, gy, is_start, has_top, has_bottom, has_left, has_right):
        room_x = gx * config.ROOM_WIDTH_PX
        room_y = gy * config.ROOM_HEIGHT_PX

        # 1. Пол
        temp_wall = Wall(0, 0)
        grid = int(temp_wall.width)

        # Заполняем полом
        for x in range(room_x, room_x + config.ROOM_WIDTH_PX, grid):
            for y in range(room_y, room_y + config.ROOM_HEIGHT_PX, grid):
                self.floor_list.append(Floor(x, y))

        # 2. Стены и двери
        doors_objects = []

        # Определяем центр стен для дверей
        mid_x = room_x + config.ROOM_WIDTH_PX // 2
        mid_y = room_y + config.ROOM_HEIGHT_PX // 2

        # --- ВЕРХНЯЯ И НИЖНЯЯ ГРАНИЦЫ ---
        for x in range(room_x, room_x + config.ROOM_WIDTH_PX, grid):
            # НИЗ (y = room_y)
            # Если есть сосед снизу И мы находимся по центру -> Дверь. Иначе -> Стена.
            if has_bottom and abs(x - mid_x) < grid * 2:
                d = DoorBlocker(x, room_y)
                doors_objects.append(d)
                self.door_list.append(d)
            else:
                self.wall_list.append(Wall(x, room_y))

            # ВЕРХ (y = room_y + height - grid)
            top_y = room_y + config.ROOM_HEIGHT_PX - grid
            if has_top and abs(x - mid_x) < grid * 2:
                d = DoorBlocker(x, top_y)
                doors_objects.append(d)
                self.door_list.append(d)
            else:
                self.wall_list.append(Wall(x, top_y))

        # --- ЛЕВАЯ И ПРАВАЯ ГРАНИЦЫ ---
        for y in range(room_y, room_y + config.ROOM_HEIGHT_PX, grid):
            # ЛЕВО (x = room_x)
            if has_left and abs(y - mid_y) < grid * 2:
                d = DoorBlocker(room_x, y)
                doors_objects.append(d)
                self.door_list.append(d)
            else:
                self.wall_list.append(Wall(room_x, y))

            # ПРАВО (x = room_x + width - grid)
            right_x = room_x + config.ROOM_WIDTH_PX - grid
            if has_right and abs(y - mid_y) < grid * 2:
                d = DoorBlocker(right_x, y)
                doors_objects.append(d)
                self.door_list.append(d)
            else:
                self.wall_list.append(Wall(right_x, y))

        # 3. Настройка волн
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