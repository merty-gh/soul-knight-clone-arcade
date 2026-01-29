import arcade
import random
import config
from world.tiles import Wall, Floor, DoorBlocker
from enemies.melee_enemy import MeleeEnemy
from entities.items import HealthPotion

class Room:
    def __init__(self):
        self.wall_list = arcade.SpriteList()
        self.floor_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.item_list = arcade.SpriteList()
        # Новый список для дверей
        self.door_list = arcade.SpriteList()

    def setup(self, player, offset_x, offset_y, doors):
        self.wall_list.clear()
        self.floor_list.clear()
        self.enemy_list.clear()
        self.item_list.clear()
        self.door_list.clear()

        temp_wall = Wall(0, 0)
        grid_size = int(temp_wall.width)

        start_x = offset_x
        end_x = offset_x + config.ROOM_WIDTH_PX
        start_y = offset_y
        end_y = offset_y + config.ROOM_HEIGHT_PX

        # 1. Пол
        for x in range(start_x, end_x + grid_size, grid_size):
            for y in range(start_y, end_y + grid_size, grid_size):
                self.floor_list.append(Floor(x, y))

        # 2. Стены и Двери
        def is_doorway(val, min_val, max_val):
            center = (min_val + max_val) / 2
            return abs(val - center) < grid_size * 2

        def add_boundary(x, y, is_vertical_door, is_horizontal_door):
            is_door_location = False
            if is_vertical_door and is_doorway(x, start_x, end_x):
                is_door_location = True
            elif is_horizontal_door and is_doorway(y, start_y, end_y):
                is_door_location = True

            if is_door_location:
                self.door_list.append(DoorBlocker(x, y))
            else:
                self.wall_list.append(Wall(x, y))

        # Генерация стен по периметру (как было)
        for x in range(start_x, end_x + grid_size, grid_size):
            add_boundary(x, start_y, doors[2], False)
        for x in range(start_x, end_x + grid_size, grid_size):
            add_boundary(x, end_y, doors[0], False)
        for y in range(start_y, end_y + grid_size, grid_size):
            add_boundary(start_x, y, False, doors[3])
        for y in range(start_y, end_y + grid_size, grid_size):
            add_boundary(end_x, y, False, doors[1])


        for _ in range(4):  # 4 ящика на комнату
            bx = random.randint(start_x + 100, end_x - 100)
            by = random.randint(start_y + 100, end_y - 100)
            # Создаем стену
            crate = Wall(bx, by)
            crate.texture = arcade.load_texture(":resources:images/tiles/boxCrate_single.png")
            self.wall_list.append(crate)

        # 3. Враги
        for _ in range(3):
            ex = random.randint(start_x + 100, end_x - 100)
            ey = random.randint(start_y + 100, end_y - 100)
            self.enemy_list.append(MeleeEnemy(ex, ey, player))

        # 4. Предметы
        if random.random() < 0.5:
            ix = random.randint(start_x + 100, end_x - 100)
            iy = random.randint(start_y + 100, end_y - 100)
            self.item_list.append(HealthPotion(ix, iy))