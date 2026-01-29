import arcade
import random
import config
from entities.items import Chest, WeaponDrop, CrystalDrop
from entities.items import Portal


# Дверь
class Door(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__(":resources:images/tiles/boxCrate.png", config.TILE_SCALING)
        self.center_x = x
        self.center_y = y
        self.initial_x = x
        self.initial_y = y


class LevelGenerator:
    def __init__(self):
        self.wall_list = arcade.SpriteList()
        self.floor_list = arcade.SpriteList()
        self.door_list = arcade.SpriteList()
        self.item_list = arcade.SpriteList()
        self.portal_list = arcade.SpriteList()

        self.enemy_list = arcade.SpriteList()  # Оставляем пустым при генерации!

        self.room_min_size = 6
        self.room_max_size = 12
        self.max_rooms = 2
        self.tile_size = 64
        self.rooms_data = {}
        self.floor_coords = set()

    def add_floor(self, x, y):
        if (x, y) in self.floor_coords:
            return
        floor = arcade.Sprite(":resources:images/tiles/stoneCenter.png", 0.5)
        floor.center_x = x * self.tile_size
        floor.center_y = y * self.tile_size
        self.floor_list.append(floor)
        self.floor_coords.add((x, y))

    def create_h_tunnel(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            for w in range(2):
                self.add_floor(x, y + w)

    def create_v_tunnel(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            for w in range(2):
                self.add_floor(x + w, y)

    def generate_walls_around_floor(self):
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        wall_coords = set()
        for gx, gy in self.floor_coords:
            for dx, dy in directions:
                nx, ny = gx + dx, gy + dy
                if (nx, ny) not in self.floor_coords:
                    wall_coords.add((nx, ny))
        for wx, wy in wall_coords:
            is_door = False
            for door in self.door_list:
                dx = int(door.initial_x // self.tile_size)
                dy = int(door.initial_y // self.tile_size)
                if dx == wx and dy == wy:
                    is_door = True
                    break
            if not is_door:
                wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", 0.5)
                wall.center_x = wx * self.tile_size
                wall.center_y = wy * self.tile_size
                self.wall_list.append(wall)

    def generate_level(self, player, level_num=1):
        # Очистка
        self.wall_list = arcade.SpriteList()
        self.floor_list = arcade.SpriteList()
        self.door_list = arcade.SpriteList()
        self.item_list = arcade.SpriteList()
        self.portal_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()  # Враги появляются динамически
        self.floor_coords = set()
        self.rooms_data = {}

        rooms = []

        # 1. КОМНАТЫ
        for _ in range(self.max_rooms):
            w = random.randint(self.room_min_size, self.room_max_size)
            h = random.randint(self.room_min_size, self.room_max_size)
            x = random.randint(0, 40)
            y = random.randint(0, 40)
            new_room = arcade.LBWH(x, y, w, h)
            failed = False
            for other in rooms:
                if (new_room.left <= other.right + 2 and new_room.right >= other.left - 2 and
                        new_room.bottom <= other.top + 2 and new_room.top >= other.bottom - 2):
                    failed = True;
                    break
            if not failed:
                rooms.append(new_room)
                for rx in range(int(new_room.left), int(new_room.right)):
                    for ry in range(int(new_room.bottom), int(new_room.top)):
                        self.add_floor(rx, ry)

        # 2. КОРИДОРЫ
        rooms.sort(key=lambda r: r.left)
        for i in range(len(rooms) - 1):
            r1 = rooms[i]
            r2 = rooms[i + 1]
            c1_x, c1_y = int(r1.left + r1.width / 2), int(r1.bottom + r1.height / 2)
            c2_x, c2_y = int(r2.left + r2.width / 2), int(r2.bottom + r2.height / 2)
            self.create_h_tunnel(c1_x, c2_x, c1_y)
            self.create_v_tunnel(c1_y, c2_y, c2_x)

        # 3. ДВЕРИ И НАСТРОЙКА ВОЛН
        for idx, room in enumerate(rooms):
            room_doors = []
            # ... (логика дверей, та же что и была) ...
            for y in range(int(room.bottom), int(room.top)):
                if (int(room.left) - 1, y) in self.floor_coords:
                    d = Door((int(room.left) - 1) * self.tile_size, y * self.tile_size);
                    self.door_list.append(d);
                    room_doors.append(d)
                if (int(room.right), y) in self.floor_coords:
                    d = Door(int(room.right) * self.tile_size, y * self.tile_size);
                    self.door_list.append(d);
                    room_doors.append(d)
            for x in range(int(room.left), int(room.right)):
                if (x, int(room.bottom) - 1) in self.floor_coords:
                    d = Door(x * self.tile_size, (int(room.bottom) - 1) * self.tile_size);
                    self.door_list.append(d);
                    room_doors.append(d)
                if (x, int(room.top)) in self.floor_coords:
                    d = Door(x * self.tile_size, int(room.top) * self.tile_size);
                    self.door_list.append(d);
                    room_doors.append(d)

            for d in room_doors:
                d.center_x = -10000  # Спрятаны изначально

            # НАСТРОЙКА ВОЛН
            # Стартовая комната (idx=0) без врагов
            if idx == 0:
                waves_count = 0
                is_boss = False
            elif idx == len(rooms) - 1 and level_num == 3:
                # ПОСЛЕДНЯЯ КОМНАТА НА 3 УРОВНЕ - БОСС
                waves_count = 1
                is_boss = True
            else:
                # Обычная комната - 2 или 3 волны
                waves_count = random.randint(2, 3)
                is_boss = False

            room_key = (int(room.left), int(room.bottom))
            self.rooms_data[room_key] = {
                'rect': room,
                'doors': room_doors,
                'cleared': (idx == 0),
                'active': False,
                'waves_total': waves_count,
                'waves_current': 0,
                'is_boss_room': is_boss
            }

            # Сундуки в обычных комнатах
            if idx > 0 and not is_boss and random.random() < 0.7:
                cx = (room.left + room.width / 2) * self.tile_size
                cy = (room.bottom + room.height / 2) * self.tile_size
                chest = Chest(cx, cy)
                self.item_list.append(chest)
                self.wall_list.append(chest)

        # 4. СТЕНЫ
        self.generate_walls_around_floor()

        # 5. ИГРОК
        start_room = rooms[0]
        player.center_x = (start_room.left + start_room.width / 2) * self.tile_size
        player.center_y = (start_room.bottom + start_room.height / 2) * self.tile_size

        # 6. ПОРТАЛ (Всегда в последней, невидимый)
        last_room = rooms[-1]
        px = (last_room.left + last_room.width / 2) * self.tile_size
        py = (last_room.bottom + last_room.height / 2) * self.tile_size
        portal = Portal(px, py)
        portal.alpha = 0
        self.portal_list.append(portal)