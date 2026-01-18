import arcade
import config
from world.room import Room


class LevelGenerator:
    def __init__(self):
        self.wall_list = arcade.SpriteList()
        self.floor_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.item_list = arcade.SpriteList()
        # Список всех дверей уровня
        self.door_list = arcade.SpriteList()

        self.rooms_data = {}

    def generate_level(self, player):
        self.wall_list = arcade.SpriteList()
        self.floor_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.item_list = arcade.SpriteList()
        self.door_list = arcade.SpriteList()
        self.rooms_data = {}

        grid_width = 2
        grid_height = 2

        room_builder = Room()

        for gy in range(grid_height):
            for gx in range(grid_width):
                offset_x = gx * config.ROOM_WIDTH_PX
                offset_y = gy * config.ROOM_HEIGHT_PX

                has_top = (gy < grid_height - 1)
                has_right = (gx < grid_width - 1)
                has_bottom = (gy > 0)
                has_left = (gx > 0)

                doors = [has_top, has_right, has_bottom, has_left]

                room_builder.setup(player, offset_x, offset_y, doors)

                current_room_enemies = []
                for e in room_builder.enemy_list:
                    current_room_enemies.append(e)

                current_room_doors = []
                for d in room_builder.door_list:
                    current_room_doors.append(d)

                # Записываем в словарь
                self.rooms_data[(gx, gy)] = {
                    "enemies": current_room_enemies,
                    "doors": current_room_doors
                }

                self.wall_list.extend(room_builder.wall_list)
                self.floor_list.extend(room_builder.floor_list)
                self.enemy_list.extend(room_builder.enemy_list)
                self.item_list.extend(room_builder.item_list)
                self.door_list.extend(room_builder.door_list)