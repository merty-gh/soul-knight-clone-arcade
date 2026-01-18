import arcade
import config
from entities.player import Player
from world.level_generator import LevelGenerator
from ui.hud import HUD
from ui.menus import MenuRenderer
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
        self.physics_engine = None
        self.bullet_list = None
        self.particle_system = None
        self.camera = None

        self.current_room_coords = None

        self.setup_game()

    def setup_game(self):
        self.player_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.camera = arcade.Camera2D()

        self.player = Player(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2)
        self.player_list.append(self.player)

        self.level_generator = LevelGenerator()
        self.level_generator.generate_level(self.player)

        self.particle_system = ParticleSystem()

        obstacles = arcade.SpriteList()
        obstacles.extend(self.level_generator.wall_list)
        obstacles.extend(self.level_generator.door_list)

        self.physics_engine = arcade.PhysicsEngineSimple(self.player, obstacles)
        self.hud = HUD()
        self.camera.position = (self.player.center_x, self.player.center_y)

        # Прячем все двери при старте
        for door in self.level_generator.door_list:
            door.center_x = -10000
            door.center_y = -10000

        self.current_room_coords = None

    def on_draw(self):
        self.clear()
        if self.camera:
            self.camera.use()

        if self.current_state in [GameState.PLAYING, GameState.PAUSED, GameState.GAME_OVER]:
            self.draw_game()

        self.default_camera.use()

        if self.current_state == GameState.PLAYING:
            self.hud.draw(self.player)
        elif self.current_state == GameState.MENU:
            self.menu_renderer.draw_main_menu()
        elif self.current_state == GameState.PAUSED:
            self.hud.draw(self.player)
            self.menu_renderer.draw_pause_menu()
        elif self.current_state == GameState.GAME_OVER:
            self.menu_renderer.draw_game_over(self.player.score)

    def draw_game(self):
        self.level_generator.floor_list.draw()
        self.level_generator.wall_list.draw()
        self.level_generator.door_list.draw()
        self.level_generator.item_list.draw()
        self.level_generator.enemy_list.draw()
        self.bullet_list.draw()
        self.player_list.draw()
        self.particle_system.draw()

    def on_update(self, delta_time):
        if self.current_state == GameState.PLAYING:
            self.update_game(delta_time)

    def update_game(self, delta_time):
        self.physics_engine.update()
        self.player_list.update(delta_time)
        self.bullet_list.update(delta_time)

        all_obstacles = arcade.SpriteList()
        all_obstacles.extend(self.level_generator.wall_list)
        all_obstacles.extend(self.level_generator.door_list)

        for enemy in self.level_generator.enemy_list:
            enemy.update_with_physics(delta_time, all_obstacles)

        self.particle_system.update()
        self.level_generator.item_list.update(delta_time)
        self.level_generator.door_list.update(delta_time)

        self.scroll_to_player()

        self.update_room_logic()  # <-- Исправленный метод здесь

        # Пули
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
                        self.player.score += 10
                        self.particle_system.add_hit_effect(enemy.center_x, enemy.center_y, arcade.color.DARK_RED)

        for enemy in self.level_generator.enemy_list:
            if arcade.check_for_collision(self.player, enemy):
                self.player.hp -= 0.5
                if self.player.hp <= 0:
                    self.player.hp = 0
                    self.current_state = GameState.GAME_OVER

        hit_items = arcade.check_for_collision_with_list(self.player, self.level_generator.item_list)
        for item in hit_items:
            if item.on_pickup(self.player):
                item.kill()

    def update_room_logic(self):
        px = self.player.center_x
        py = self.player.center_y

        # 1. Потенциальная комната (где сейчас центр игрока)
        gx = int(px // config.ROOM_WIDTH_PX)
        gy = int(py // config.ROOM_HEIGHT_PX)
        potential_room = (gx, gy)

        # 2. Проверяем, зашел ли игрок достаточно глубоко (Буферная зона)
        buffer = 100

        # Локальные координаты внутри комнаты
        local_x = px % config.ROOM_WIDTH_PX
        local_y = py % config.ROOM_HEIGHT_PX

        in_safe_zone_x = (buffer < local_x < config.ROOM_WIDTH_PX - buffer)
        in_safe_zone_y = (buffer < local_y < config.ROOM_HEIGHT_PX - buffer)

        # 3. Обновляем комнату ТОЛЬКО если игрок в безопасной зоне
        if in_safe_zone_x and in_safe_zone_y:
            if potential_room != self.current_room_coords:
                self.current_room_coords = potential_room
                self.on_enter_room(potential_room)

        # 4. Проверка зачистки текущей комнаты (если мы в какой-то комнате)
        if self.current_room_coords:
            self.check_room_cleared(self.current_room_coords)

    def on_enter_room(self, room_coords):
        room_data = self.level_generator.rooms_data.get(room_coords)
        if not room_data: return

        enemies = room_data['enemies']
        alive_count = 0
        for e in enemies:
            if e in self.level_generator.enemy_list:
                alive_count += 1

        if alive_count > 0:
            for door in room_data['doors']:
                door.center_x = door.initial_x
                door.center_y = door.initial_y

    def check_room_cleared(self, room_coords):
        room_data = self.level_generator.rooms_data.get(room_coords)
        if not room_data: return

        enemies = room_data['enemies']
        alive_count = 0
        for e in enemies:
            if e in self.level_generator.enemy_list:
                alive_count += 1

        if alive_count == 0:
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
        if key == arcade.key.ESCAPE: arcade.close_window()
        if self.current_state == GameState.MENU:
            if key == arcade.key.ENTER:
                self.setup_game()
                self.current_state = GameState.PLAYING
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
                self.setup_game()
                self.current_state = GameState.PLAYING

    def on_key_release(self, key, modifiers):
        if self.current_state == GameState.PLAYING:
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