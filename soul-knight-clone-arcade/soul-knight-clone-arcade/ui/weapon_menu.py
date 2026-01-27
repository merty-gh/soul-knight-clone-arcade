import arcade
import config
import database


class WeaponMenu:
    def __init__(self, player):
        self.player = player
        self.unlocked_weapons = database.get_unlocked_weapons()
        self.sprite_list = arcade.SpriteList()
        self.buttons = []

        # НОВОЕ: Индекс выбранного оружия для клавиатуры
        self.selected_index = 0

        self.setup_buttons()

    def setup_buttons(self):
        start_x = 150
        start_y = config.SCREEN_HEIGHT - 200
        padding = 150

        for i, weapon_data in enumerate(config.WEAPONS_CONFIG):
            name = weapon_data["name"]
            image_path = weapon_data["image"]
            price = weapon_data["price"]

            try:
                sprite = arcade.Sprite(image_path)
            except Exception:
                sprite = arcade.Sprite(":resources:images/items/gold_1.png")

            target_size = 64
            max_dimension = max(sprite.width, sprite.height)
            if max_dimension > 0:
                scale_factor = target_size / max_dimension
                sprite.scale = scale_factor

            sprite.center_x = start_x + (i % 3) * padding
            sprite.center_y = start_y - (i // 3) * padding

            self.sprite_list.append(sprite)

            is_unlocked = name in self.unlocked_weapons or price == 0
            is_equipped = (self.player.weapon.__class__.__name__ == weapon_data["class_name"])

            half_size = 40
            button_bounds = {
                "min_x": sprite.center_x - half_size,
                "max_x": sprite.center_x + half_size,
                "min_y": sprite.center_y - half_size,
                "max_y": sprite.center_y + half_size
            }

            self.buttons.append({
                "sprite": sprite,
                "data": weapon_data,
                "unlocked": is_unlocked,
                "equipped": is_equipped,
                "bounds": button_bounds
            })

    def draw(self):
        arcade.draw_lrbt_rectangle_filled(0, config.SCREEN_WIDTH, 0, config.SCREEN_HEIGHT, (0, 0, 0, 200))

        arcade.Text("ARMORY", config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT - 80,
                    arcade.color.WHITE, 40, anchor_x="center", bold=True).draw()

        self.sprite_list.draw()

        for idx, btn in enumerate(self.buttons):
            sprite = btn["sprite"]
            data = btn["data"]

            color = arcade.color.GRAY
            if btn["equipped"]:
                color = arcade.color.GREEN
            elif btn["unlocked"]:
                color = arcade.color.WHITE

            # Основная рамка
            rect = arcade.LBWH(sprite.center_x - 50, sprite.center_y - 50, 100, 100)
            arcade.draw_rect_outline(rect, color, 2)

            # --- НОВОЕ: Подсветка выбора клавиатурой (Голубая рамка) ---
            if idx == self.selected_index:
                select_rect = arcade.LBWH(sprite.center_x - 55, sprite.center_y - 55, 110, 110)
                arcade.draw_rect_outline(select_rect, arcade.color.CYAN, 4)

            text_str = f"{data['price']} G"
            text_color = arcade.color.YELLOW

            if btn["equipped"]:
                text_str = "EQUIPPED"
                text_color = arcade.color.GREEN
            elif btn["unlocked"]:
                text_str = "OWNED"
                text_color = arcade.color.WHITE

            arcade.Text(data["name"], sprite.center_x, sprite.center_y - 60,
                        arcade.color.WHITE, 12, anchor_x="center").draw()
            arcade.Text(text_str, sprite.center_x, sprite.center_y - 80,
                        text_color, 12, anchor_x="center").draw()

        arcade.Text("Arrows/WASD to Select, ENTER to Buy/Equip", config.SCREEN_WIDTH // 2, 50,
                    arcade.color.GRAY, 14, anchor_x="center").draw()

    def on_key_press(self, key):
        if key == arcade.key.ESCAPE:
            return "EXIT"

        # --- НОВОЕ: Управление стрелками и WASD ---
        if key == arcade.key.RIGHT or key == arcade.key.D:
            self.selected_index = (self.selected_index + 1) % len(self.buttons)

        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.selected_index = (self.selected_index - 1) % len(self.buttons)

        # Покупка/Экипировка по Enter или Пробелу
        elif key == arcade.key.ENTER or key == arcade.key.SPACE:
            self.handle_click(self.buttons[self.selected_index])

        return None

    def on_mouse_press(self, x, y):
        for i, btn in enumerate(self.buttons):
            b = btn["bounds"]
            if b["min_x"] <= x <= b["max_x"] and b["min_y"] <= y <= b["max_y"]:
                self.selected_index = i  # Также обновляем выбор при клике
                self.handle_click(btn)

    def handle_click(self, btn):
        data = btn["data"]

        if btn["equipped"]:
            return

        if btn["unlocked"]:
            self.player.equip_weapon_by_name(data["class_name"])
            self.refresh_state()
        else:
            if self.player.crystals >= data["price"]:
                if database.spend_crystals(data["price"]):
                    database.unlock_weapon(data["name"])
                    self.player.update_crystals_from_db()
                    self.player.equip_weapon_by_name(data["class_name"])
                    self.refresh_state()

    def refresh_state(self):
        self.unlocked_weapons = database.get_unlocked_weapons()
        for btn in self.buttons:
            weapon_class = btn["data"]["class_name"]
            btn["unlocked"] = btn["data"]["name"] in self.unlocked_weapons or btn["data"]["price"] == 0

            current_weapon_name = type(self.player.weapon).__name__
            btn["equipped"] = (current_weapon_name == weapon_class)