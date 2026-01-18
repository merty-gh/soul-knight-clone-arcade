import sys
import os

# --- МАГИЯ ДЛЯ ИСПРАВЛЕНИЯ ПУТЕЙ ---
# Получаем путь к папке, где лежит этот файл (ui), и берем папку выше (main)
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
# -----------------------------------

import arcade
import config
import database


class SkinMenu:
    def __init__(self, player):
        self.player = player
        self.selected_index = 0
        self.skins = config.SKINS_CONFIG

        # Используем SpriteList для отрисовки
        self.preview_sprites = arcade.SpriteList()

        for i, skin_data in enumerate(self.skins):
            # Загружаем текстуру
            sprite = arcade.Sprite(skin_data["image"], scale=1.5)
            # Расставляем их в ряд
            sprite.center_x = config.SCREEN_WIDTH // 2 + (i - 1.5) * 150
            sprite.center_y = config.SCREEN_HEIGHT // 2
            self.preview_sprites.append(sprite)

    def draw(self):
        # 1. Затемнение фона
        arcade.draw_lrbt_rectangle_filled(0, config.SCREEN_WIDTH, 0, config.SCREEN_HEIGHT, (0, 0, 0, 220))

        # 2. Заголовок
        arcade.draw_text("WARDROBE", config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT - 100,
                         arcade.color.WHITE, 30, anchor_x="center", bold=True)

        # 3. Рисуем СПРАЙТЫ
        self.preview_sprites.draw()

        # 4. Рисуем обводку и текст
        for i, sprite in enumerate(self.preview_sprites):
            # Подсветка выбранного
            if i == self.selected_index:
                arcade.draw_circle_outline(sprite.center_x, sprite.center_y, 60, arcade.color.YELLOW, 3)

            # Имя скина
            arcade.draw_text(self.skins[i]["name"], sprite.center_x, sprite.center_y - 80,
                             arcade.color.WHITE, 12, anchor_x="center")

        # 5. Информация о выбранном скине
        selected_skin = self.skins[self.selected_index]
        unlocked_list = database.get_unlocked_skins()
        is_unlocked = selected_skin["name"] in unlocked_list
        is_equipped = self.player.current_skin_name == selected_skin["name"]

        info_y = 150
        if is_equipped:
            arcade.draw_text("EQUIPPED", config.SCREEN_WIDTH // 2, info_y, arcade.color.GREEN, 20, anchor_x="center")
        elif is_unlocked:
            arcade.draw_text("Press [ENTER] to Equip", config.SCREEN_WIDTH // 2, info_y, arcade.color.WHITE, 20,
                             anchor_x="center")
        else:
            price = selected_skin["price"]
            color = arcade.color.YELLOW if self.player.crystals >= price else arcade.color.RED
            arcade.draw_text(f"Price: {price} Crystals", config.SCREEN_WIDTH // 2, info_y + 30, arcade.color.GOLD, 20,
                             anchor_x="center")
            arcade.draw_text("Press [ENTER] to Buy", config.SCREEN_WIDTH // 2, info_y, color, 16, anchor_x="center")

        # Баланс
        arcade.draw_text(f"Your Crystals: {self.player.crystals}", 50, config.SCREEN_HEIGHT - 50, arcade.color.CYAN, 20)

    def on_key_press(self, key):
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.selected_index = (self.selected_index - 1) % len(self.skins)
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.selected_index = (self.selected_index + 1) % len(self.skins)
        elif key == arcade.key.ENTER:
            self.try_action()
        elif key == arcade.key.ESCAPE:
            return "EXIT"
        return None

    def try_action(self):
        selected_skin = self.skins[self.selected_index]
        unlocked_list = database.get_unlocked_skins()
        name = selected_skin["name"]

        if name in unlocked_list:
            # Надеть
            self.player.equip_skin(name)
        else:
            # Купить
            if database.spend_crystals(selected_skin["price"]):
                database.unlock_skin(name)
                self.player.update_crystals_from_db()
                self.player.equip_skin(name)
            else:
                print("Not enough money")