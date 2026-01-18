import random
import math  # Не забудьте этот импорт
import arcade
import config
import database
from entities.player import Player
from entities.items import CrystalDrop
# Импортируем классы врагов
from enemies.base_enemy import Zombie, Robot
from world.level_generator import LevelGenerator
from world.lobby import Lobby
from ui.hud import HUD
from ui.menus import MenuRenderer
from ui.skin_menu import SkinMenu
from ui.weapon_menu import WeaponMenu
from engine.game_state import GameState
from utils.particle_system import ParticleSystem


class GameWindow(arcade.Window):
    def __init__(self):
        super().__init__(config.SCREEN_WIDTH, config.SCREEN_HEIGHT, config.SCREEN_TITLE)
        arcade.set_background_color(config.BG_COLOR)

        self.current_state = GameState.MENU
        self.menu_renderer = MenuRenderer()

        self.hud = None
        self.player_list = None
        self.player = None

        self.level_generator = None
        self.lobby = None

        self.skin_menu = None
        self.weapon_menu = None

        self.physics_engine = None
        self.bullet_list = None

        # НОВОЕ: Список пуль врагов
        self.enemy_bullet_list = None

        self.particle_system = ParticleSystem()
        self.camera = None

        self.interact_text = arcade.Text(
            text="", x=config.SCREEN_WIDTH // 2, y=config.SCREEN_HEIGHT // 2 + 50,
            color=arcade.color.WHITE, font_size=14, anchor_x="center"
        )
        self.lobby_crystal_text = arcade.Text(
            text="", x=20, y=config.SCREEN_HEIGHT - 40,
            color=arcade.color.CYAN, font_size=20
        )

        self.current_room_coords = None
        self.setup_system()

    def setup_system(self):
        self.player_list = arcade.SpriteList()
        self.camera = arcade.Camera2D()
        self.player = Player(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2)
        self.player_list.append(self.player)
        self.particle_system = ParticleSystem()
        self.hud = HUD()

    def enter_lobby(self):
        self.current_state = GameState.LOBBY
        self.lobby = Lobby()
        self.lobby.setup()
        self.player.center_x = config.SCREEN_WIDTH // 2
        self.player.center_y = 250
        obstacles = arcade.SpriteList()
        obstacles.extend(self.lobby.wall_list)
        self.physics_engine = arcade.PhysicsEngineSimple(self.player, obstacles)
        self.camera.position = (config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2)
        self.bullet_list = arcade.SpriteList()
        # Сброс пуль врагов
        self.enemy_bullet_list = arcade.SpriteList()

    def open_skin_menu(self):
        self.current_state = GameState.SKIN_SELECT
        self.skin_menu = SkinMenu(self.player)

    def open_weapon_menu(self):
        self.current_state = GameState.WEAPON_SELECT
        self.weapon_menu = WeaponMenu(self.player)

    def start_dungeon_run(self):
        self.current_state = GameState.PLAYING
        self.level_generator = LevelGenerator()
        self.level_generator.generate_level(self.player)

        obstacles = arcade.SpriteList()
        obstacles.extend(self.level_generator.wall_list)
        obstacles.extend(self.level_generator.door_list)

        self.physics_engine = arcade.PhysicsEngineSimple(self.player, obstacles)
        self.camera.position = (self.player.center_x, self.player.center_y)

        for door in self.level_generator.door_list:
            door.center_x = -10000
            door.center_y = -10000
        self.current_room_coords = None

        # Сброс пуль врагов при старте
        self.enemy_bullet_list = arcade.SpriteList()

    def on_draw(self):
        self.clear()
        if self.camera: self.camera.use()

        if self.current_state == GameState.LOBBY:
            self.lobby.floor_list.draw()
            self.lobby.wall_list.draw()
            self.lobby.decor_list.draw()
            self.lobby.interactable_list.draw()
            self.player_list.draw()
            self.interact_text.draw()

        elif self.current_state in [GameState.PLAYING, GameState.PAUSED, GameState.GAME_OVER]:
            self.draw_game()

        self.default_camera.use()

        if self.current_state == GameState.PLAYING:
            self.hud.draw(self.player)
        elif self.current_state == GameState.LOBBY:
            self.lobby_crystal_text.text = f"Crystals: {self.player.crystals}"
            self.lobby_crystal_text.draw()
        elif self.current_state == GameState.MENU:
            self.menu_renderer.draw_main_menu()
        elif self.current_state == GameState.PAUSED:
            self.hud.draw(self.player)
            self.menu_renderer.draw_pause_menu()
        elif self.current_state == GameState.GAME_OVER:
            self.menu_renderer.draw_game_over(self.player.score)
        elif self.current_state == GameState.SKIN_SELECT:
            self.skin_menu.draw()
        elif self.current_state == GameState.WEAPON_SELECT:
            self.weapon_menu.draw()

    def draw_game(self):
        self.level_generator.floor_list.draw()
        self.level_generator.wall_list.draw()
        self.level_generator.door_list.draw()
        self.level_generator.item_list.draw()
        self.level_generator.enemy_list.draw()
        self.bullet_list.draw()
        self.enemy_bullet_list.draw()  # Рисуем пули врагов
        self.player_list.draw()
        self.particle_system.draw()

    def on_update(self, delta_time):
        if self.current_state == GameState.LOBBY:
            self.update_lobby(delta_time)
        elif self.current_state == GameState.PLAYING:
            self.update_game(delta_time)

    def update_lobby(self, delta_time):
        self.physics_engine.update()
        self.player_list.update(delta_time)
        self.interact_text.value = ""
        closest_item = arcade.check_for_collision_with_list(self.player, self.lobby.interactable_list)
        if closest_item:
            item = closest_item[0]
            self.interact_text.value = item.text
            self.interact_text.x = self.player.center_x
            self.interact_text.y = self.player.center_y + 50

    def update_game(self, delta_time):
        self.physics_engine.update()
        self.player_list.update(delta_time)
        self.bullet_list.update(delta_time)
        self.enemy_bullet_list.update(delta_time)  # Обновляем пули врагов

        all_obstacles = arcade.SpriteList()
        all_obstacles.extend(self.level_generator.wall_list)
        all_obstacles.extend(self.level_generator.door_list)

        # --- ЛОГИКА ВРАГОВ ---
        for enemy in self.level_generator.enemy_list:
            # Вызываем обновление и проверяем, выстрелил ли враг
            bullet = enemy.update_with_physics(delta_time, all_obstacles)
            if bullet:
                self.enemy_bullet_list.append(bullet)  # Добавляем пулю в игру

        self.particle_system.update()
        self.level_generator.item_list.update(delta_time)
        self.level_generator.door_list.update(delta_time)

        self.scroll_to_player()
        self.update_room_logic()

        # --- КОЛЛИЗИИ ПУЛЬ ИГРОКА ---
        walls_and_doors = [self.level_generator.wall_list, self.level_generator.door_list]
        for bullet in self.bullet_list:
            hit_obstacles = arcade.check_for_collision_with_lists(bullet, walls_and_doors)
            if len(hit_obstacles) > 0:
                self.particle_system.add_hit_effect(bullet.center_x, bullet.center_y, arcade.color.GRAY)
                bullet.kill()
                continue

            hit_enemies = arcade.check_for_collision_with_list(bullet, self.level_generator.enemy_list)
            if len(hit_enemies) > 0:
                bullet.kill()
                for enemy in hit_enemies:
                    self.particle_system.add_hit_effect(enemy.center_x, enemy.center_y, arcade.color.RED)
                    enemy.take_damage(bullet.damage)
                    if enemy.hp <= 0:
                        crystal = CrystalDrop(enemy.center_x, enemy.center_y, amount=5)
                        self.level_generator.item_list.append(crystal)
                        self.player.score += 10
                        self.particle_system.add_hit_effect(enemy.center_x, enemy.center_y, arcade.color.DARK_RED)

        # --- КОЛЛИЗИИ ПУЛЬ ВРАГА ---
        for bullet in self.enemy_bullet_list:
            # Попадание в стены
            if arcade.check_for_collision_with_lists(bullet, walls_and_doors):
                bullet.kill()
                continue

            # Попадание в игрока
            if arcade.check_for_collision(self.player, bullet):
                bullet.kill()
                self.player.hp -= config.ROBOT_DAMAGE  # Урон от робота
                self.particle_system.add_hit_effect(self.player.center_x, self.player.center_y, arcade.color.RED)
                if self.player.hp <= 0:
                    self.player.hp = 0
                    self.current_state = GameState.GAME_OVER

        # --- УРОН ОТ ПРИКОСНОВЕНИЯ (ЗОМБИ) ---
        for enemy in self.level_generator.enemy_list:
            # Если это Зомби (проверяем класс), он бьет касанием
            if isinstance(enemy, Zombie):
                if arcade.check_for_collision(self.player, enemy):
                    self.player.hp -= 0.5  # Урон от касания
                    if self.player.hp <= 0:
                        self.player.hp = 0
                        self.current_state = GameState.GAME_OVER

        # --- ПОДБОР ПРЕДМЕТОВ ---
        hit_items = arcade.check_for_collision_with_list(self.player, self.level_generator.item_list)
        for item in hit_items:
            if isinstance(item, CrystalDrop):
                database.add_crystals(item.amount)
                self.player.update_crystals_from_db()
                item.kill()
            elif item.on_pickup(self.player):
                item.kill()

    def update_room_logic(self):
        px = self.player.center_x
        py = self.player.center_y
        gx = int(px // config.ROOM_WIDTH_PX)
        gy = int(py // config.ROOM_HEIGHT_PX)
        potential_room = (gx, gy)

        buffer = 100
        local_x = px % config.ROOM_WIDTH_PX
        local_y = py % config.ROOM_HEIGHT_PX
        in_safe_zone_x = (buffer < local_x < config.ROOM_WIDTH_PX - buffer)
        in_safe_zone_y = (buffer < local_y < config.ROOM_HEIGHT_PX - buffer)

        if in_safe_zone_x and in_safe_zone_y:
            if potential_room != self.current_room_coords:
                self.current_room_coords = potential_room
                self.on_enter_room(potential_room)

        if self.current_room_coords:
            self.check_room_cleared(self.current_room_coords)

    def on_enter_room(self, room_coords):
        room_data = self.level_generator.rooms_data.get(room_coords)
        if not room_data: return

        if room_data['cleared']:
            for door in room_data['doors']:
                door.center_x = -10000
            return

        if room_data['current_wave'] == 0:
            for door in room_data['doors']:
                door.center_x = door.initial_x
                door.center_y = door.initial_y
            self.start_next_wave(room_coords)

    def start_next_wave(self, room_coords):
        room_data = self.level_generator.rooms_data.get(room_coords)
        room_data['current_wave'] += 1
        wave_num = room_data['current_wave']

        print(f"Room {room_coords}: Wave {wave_num} started!")
        count = 1 + wave_num

        gx, gy = room_coords
        min_x = gx * config.ROOM_WIDTH_PX + 100
        max_x = (gx + 1) * config.ROOM_WIDTH_PX - 100
        min_y = gy * config.ROOM_HEIGHT_PX + 100
        max_y = (gy + 1) * config.ROOM_HEIGHT_PX - 100

        for _ in range(count):
            ex = random.randint(min_x, max_x)
            ey = random.randint(min_y, max_y)

            # --- СЛУЧАЙНЫЙ ВЫБОР ВРАГА ---
            # 70% шанс Зомби, 30% шанс Робот
            if random.random() < 0.7:
                enemy = Zombie(ex, ey, self.player)
            else:
                enemy = Robot(ex, ey, self.player)

            self.level_generator.enemy_list.append(enemy)
            room_data['spawned_enemies'].append(enemy)

    def check_room_cleared(self, room_coords):
        room_data = self.level_generator.rooms_data.get(room_coords)
        if not room_data or room_data['cleared']: return

        active_enemies = [e for e in room_data['spawned_enemies'] if e.hp > 0]

        if len(active_enemies) == 0:
            room_data['spawned_enemies'] = []
            if room_data['current_wave'] < room_data['max_waves']:
                self.start_next_wave(room_coords)
            else:
                room_data['cleared'] = True
                print(f"Room {room_coords} CLEARED!")
                for door in room_data['doors']:
                    door.center_x = -10000
                    door.center_y = -10000

    def scroll_to_player(self):
        cur_x, cur_y = self.camera.position
        dest_x, dest_y = self.player.center_x, self.player.center_y
        speed = 0.1
        new_x = cur_x + (dest_x - cur_x) * speed
        new_y = cur_y + (dest_y - cur_y) * speed
        self.camera.position = (new_x, new_y)

    def on_mouse_press(self, x, y, button, modifiers):
        if self.current_state == GameState.PLAYING:
            if button == arcade.MOUSE_BUTTON_LEFT:
                world_x, world_y, _ = self.camera.unproject((x, y))
                bullet = self.player.weapon.shoot(self.player.center_x, self.player.center_y, world_x, world_y)
                if bullet:
                    self.bullet_list.append(bullet)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            if self.current_state in [GameState.SKIN_SELECT, GameState.WEAPON_SELECT]:
                self.enter_lobby()
            else:
                arcade.close_window()

        if self.current_state == GameState.MENU:
            if key == arcade.key.ENTER:
                self.enter_lobby()

        elif self.current_state == GameState.LOBBY:
            if key == arcade.key.W or key == arcade.key.UP:
                self.player.change_y = config.PLAYER_SPEED
            elif key == arcade.key.S or key == arcade.key.DOWN:
                self.player.change_y = -config.PLAYER_SPEED
            elif key == arcade.key.A or key == arcade.key.LEFT:
                self.player.change_x = -config.PLAYER_SPEED
            elif key == arcade.key.D or key == arcade.key.RIGHT:
                self.player.change_x = config.PLAYER_SPEED

            if key == arcade.key.E:
                hit_list = arcade.check_for_collision_with_list(self.player, self.lobby.interactable_list)
                if hit_list:
                    item = hit_list[0]
                    item_type = str(type(item))
                    if "Skin" in item_type:
                        self.open_skin_menu()
                    elif "Weapon" in item_type:
                        self.open_weapon_menu()
                    else:
                        item.on_interact(self.player, self)

        elif self.current_state == GameState.SKIN_SELECT:
            result = self.skin_menu.on_key_press(key)
            if result == "EXIT": self.enter_lobby()

        elif self.current_state == GameState.WEAPON_SELECT:
            result = self.weapon_menu.on_key_press(key)
            if result == "EXIT": self.enter_lobby()

        elif self.current_state == GameState.PLAYING:
            if key == arcade.key.P: self.current_state = GameState.PAUSED
            if key == arcade.key.W or key == arcade.key.UP:
                self.player.change_y = config.PLAYER_SPEED
            elif key == arcade.key.S or key == arcade.key.DOWN:
                self.player.change_y = -config.PLAYER_SPEED
            elif key == arcade.key.A or key == arcade.key.LEFT:
                self.player.change_x = -config.PLAYER_SPEED
            elif key == arcade.key.D or key == arcade.key.RIGHT:
                self.player.change_x = config.PLAYER_SPEED

        elif self.current_state == GameState.PAUSED:
            if key == arcade.key.P: self.current_state = GameState.PLAYING

        elif self.current_state == GameState.GAME_OVER:
            if key == arcade.key.R:
                self.player.hp = self.player.max_hp
                self.enter_lobby()

    def on_key_release(self, key, modifiers):
        if self.current_state in [GameState.PLAYING, GameState.LOBBY]:
            if key == arcade.key.W or key == arcade.key.UP:
                if self.player.change_y > 0: self.player.change_y = 0
            elif key == arcade.key.S or key == arcade.key.DOWN:
                if self.player.change_y < 0: self.player.change_y = 0
            elif key == arcade.key.A or key == arcade.key.LEFT:
                if self.player.change_x < 0: self.player.change_x = 0
            elif key == arcade.key.D or key == arcade.key.RIGHT:
                if self.player.change_x > 0: self.player.change_x = 0


def main():
    window = GameWindow()
    arcade.run()


if __name__ == "__main__":
    main()