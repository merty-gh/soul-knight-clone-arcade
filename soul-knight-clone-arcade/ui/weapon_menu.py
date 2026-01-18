import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

import arcade
import config
import database


class WeaponMenu:
    def __init__(self, player):
        self.player = player
        self.selected_index = 0
        self.weapons = config.WEAPONS_CONFIG

        self.preview_sprites = arcade.SpriteList()
        self.name_labels = []

        for i, w_data in enumerate(self.weapons):
            sprite = arcade.Sprite(w_data["image"], scale=1.5)
            sprite.center_x = config.SCREEN_WIDTH // 2 + (i - 1.5) * 150
            sprite.center_y = config.SCREEN_HEIGHT // 2
            self.preview_sprites.append(sprite)

            text = arcade.Text(
                text=w_data["name"],
                x=sprite.center_x,
                y=sprite.center_y - 80,
                color=arcade.color.WHITE,
                font_size=12,
                anchor_x="center"
            )
            self.name_labels.append(text)

        self.title_text = arcade.Text("ARMORY", config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT - 100,
                                      arcade.color.WHITE, 30, anchor_x="center", bold=True)

        self.info_main_text = arcade.Text("", config.SCREEN_WIDTH // 2, 150, arcade.color.WHITE, 20, anchor_x="center")
        self.info_sub_text = arcade.Text("", config.SCREEN_WIDTH // 2, 180, arcade.color.GOLD, 20, anchor_x="center")
        self.balance_text = arcade.Text("", 50, config.SCREEN_HEIGHT - 50, arcade.color.CYAN, 20)

    def draw(self):
        arcade.draw_lrbt_rectangle_filled(0, config.SCREEN_WIDTH, 0, config.SCREEN_HEIGHT, (0, 0, 0, 220))
        self.title_text.draw()
        self.preview_sprites.draw()

        for i, sprite in enumerate(self.preview_sprites):
            if i == self.selected_index:
                arcade.draw_circle_outline(sprite.center_x, sprite.center_y, 60, arcade.color.YELLOW, 3)
            self.name_labels[i].draw()

        selected_w = self.weapons[self.selected_index]
        unlocked_list = database.get_unlocked_weapons()
        is_unlocked = selected_w["name"] in unlocked_list
        current_weapon_class = self.player.weapon.__class__.__name__
        is_equipped = current_weapon_class == selected_w["class_name"]

        self.info_sub_text.text = ""

        if is_equipped:
            self.info_main_text.text = "EQUIPPED"
            self.info_main_text.color = arcade.color.GREEN
        elif is_unlocked:
            self.info_main_text.text = "Press [ENTER] to Equip"
            self.info_main_text.color = arcade.color.WHITE
        else:
            price = selected_w["price"]
            self.info_sub_text.text = f"Price: {price} Crystals"
            self.info_sub_text.draw()

            self.info_main_text.text = "Press [ENTER] to Buy"
            if self.player.crystals >= price:
                self.info_main_text.color = arcade.color.YELLOW
            else:
                self.info_main_text.color = arcade.color.RED

        self.info_main_text.draw()

        self.balance_text.text = f"Your Crystals: {self.player.crystals}"
        self.balance_text.draw()

    def on_key_press(self, key):
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.selected_index = (self.selected_index - 1) % len(self.weapons)
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.selected_index = (self.selected_index + 1) % len(self.weapons)
        elif key == arcade.key.ENTER:
            self.try_action()
        elif key == arcade.key.ESCAPE:
            return "EXIT"
        return None

    def try_action(self):
        selected_w = self.weapons[self.selected_index]
        unlocked_list = database.get_unlocked_weapons()
        name = selected_w["name"]

        if name in unlocked_list:
            self.player.equip_weapon_by_name(selected_w["class_name"])
        else:
            if database.spend_crystals(selected_w["price"]):
                database.unlock_weapon(name)
                self.player.update_crystals_from_db()
                self.player.equip_weapon_by_name(selected_w["class_name"])
            else:
                print("Not enough money")