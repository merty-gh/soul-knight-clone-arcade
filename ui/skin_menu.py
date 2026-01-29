import sys
import os

# Магия путей
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

import arcade
import config
import database


class SkinMenu:
    def __init__(self, player):
        self.player = player
        self.selected_index = 0
        self.skins = config.SKINS_CONFIG

        # Спрайты скинов
        self.preview_sprites = arcade.SpriteList()
        # Текстовые подписи для скинов (оптимизация)
        self.name_labels = []

        for i, skin_data in enumerate(self.skins):
            # Для меню используем маленькую иконку, если задана, иначе основное изображение
            icon_path = skin_data.get("icon", skin_data["image"])
            # Спрайт (иконка) — небольшой масштаб, чтобы не занимать весь экран
            sprite = arcade.Sprite(icon_path, scale=1.5)
            sprite.center_x = config.SCREEN_WIDTH // 2 + (i - 1.5) * 150
            sprite.center_y = config.SCREEN_HEIGHT // 2
            self.preview_sprites.append(sprite)

            # Текст имени (создаем один раз)
            text = arcade.Text(
                text=skin_data["name"],
                x=sprite.center_x,
                y=sprite.center_y - 80,
                color=arcade.color.WHITE,
                font_size=12,
                anchor_x="center"
            )
            self.name_labels.append(text)

        # Статичные заголовки
        self.title_text = arcade.Text("WARDROBE", config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT - 100,
                                      arcade.color.WHITE, 30, anchor_x="center", bold=True)

        # Динамические тексты (информация внизу)
        self.info_main_text = arcade.Text("", config.SCREEN_WIDTH // 2, 150, arcade.color.WHITE, 20, anchor_x="center")
        self.info_sub_text = arcade.Text("", config.SCREEN_WIDTH // 2, 180, arcade.color.GOLD, 20, anchor_x="center")
        self.balance_text = arcade.Text("", 50, config.SCREEN_HEIGHT - 50, arcade.color.CYAN, 20)

    def draw(self):
        # Фон
        arcade.draw_lrbt_rectangle_filled(0, config.SCREEN_WIDTH, 0, config.SCREEN_HEIGHT, (0, 0, 0, 220))

        # Заголовок
        self.title_text.draw()

        # Спрайты
        self.preview_sprites.draw()

        # Подписи к спрайтам и обводка
        for i, sprite in enumerate(self.preview_sprites):
            if i == self.selected_index:
                arcade.draw_circle_outline(sprite.center_x, sprite.center_y, 60, arcade.color.YELLOW, 3)
            # Рисуем заранее созданный текст
            self.name_labels[i].draw()

        # Логика отображения информации
        selected_skin = self.skins[self.selected_index]
        unlocked_list = database.get_unlocked_skins()
        is_unlocked = selected_skin["name"] in unlocked_list
        is_equipped = self.player.current_skin_name == selected_skin["name"]

        # Обновляем текст в объектах (это быстро)
        self.info_sub_text.text = ""  # Сброс

        if is_equipped:
            self.info_main_text.text = "EQUIPPED"
            self.info_main_text.color = arcade.color.GREEN
        elif is_unlocked:
            self.info_main_text.text = "Press [ENTER] to Equip"
            self.info_main_text.color = arcade.color.WHITE
        else:
            price = selected_skin["price"]
            self.info_sub_text.text = f"Price: {price} Crystals"
            self.info_sub_text.draw()

            self.info_main_text.text = "Press [ENTER] to Buy"
            if self.player.crystals >= price:
                self.info_main_text.color = arcade.color.YELLOW
            else:
                self.info_main_text.color = arcade.color.RED

        self.info_main_text.draw()

        # Баланс кристаллов
        self.balance_text.text = f"Your Crystals: {self.player.crystals}"
        self.balance_text.draw()

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
            self.player.equip_skin(name)
        else:
            if database.spend_crystals(selected_skin["price"]):
                database.unlock_skin(name)
                self.player.update_crystals_from_db()
                self.player.equip_skin(name)
            else:
                print("Not enough money")